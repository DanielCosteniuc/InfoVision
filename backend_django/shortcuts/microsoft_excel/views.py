import os
import subprocess
import logging
import pythoncom
import win32com.client
import time
import win32gui
import win32con
import winreg
import win32api
import pyautogui
import pygetwindow as gw
import xlwings as xw
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

def enum_windows_callback(hwnd, results):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        window_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        if "Microsoft Excel" in window_text or class_name == "XLMAIN":
            results.append((hwnd, window_text, class_name))

'''def check_excel_open():
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return len(windows) > 0'''


def check_excel_open():
    try:
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if not windows:
            logging.debug('Nu s-au găsit ferontele Excel deschise.')
            return False
        
        for hwnd, window_text, class_name in windows:
            logging.debug(f'Fereastra Excel găsită - Handle: {hwnd}, Titlu: "{window_text}", Clasa: "{class_name}"')
        
        return True
    except Exception as e:
        logging.error(f'Error checking Excel open: {e}')
        return False

def maximize_window_if_not_maximized(hwnd):
    placement = win32gui.GetWindowPlacement(hwnd)
    if placement[1] != win32con.SW_MAXIMIZE:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        logger.info("Excel window maximized.")
    else:
        
        logger.info("Excel window already maximized.")

def get_excel_path():
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\excel.exe") as key:
            excel_path, _ = winreg.QueryValueEx(key, "")
            return excel_path
    except Exception as e:
        logger.error(f"Could not find Excel path in the registry: {str(e)}")
        return None
    
def minimize_and_maximize_excel():
    pyautogui.hotkey('win', 'd') 
    time.sleep(0.1)  
    pyautogui.hotkey('win', 'd')  
    time.sleep(0.1)  
    
@csrf_exempt
def open_excel(request):
    """
    Deschide Excel sau activează o instanță existentă.
    """
    try:
        app = xw.apps.active
        if app:
            return JsonResponse({'success': True, 'message': 'Instanța activă de Excel este deja deschisă.'}, status=200)

        # Dacă nu există instanță activă, deschide Excel
        app = xw.App(visible=True)
        return JsonResponse({'success': True, 'message': 'Excel deschis cu succes.'}, status=200)
    except Exception as e:
        logger.error(f'Eroare la deschiderea Excel: {e}')
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def add_sheet(request):
    """
    Adaugă o foaie nouă în workbook-ul activ.
    """
    try:
        app = xw.apps.active
        if app is None:
            return JsonResponse({'success': False, 'message': 'Nicio instanță activă de Excel.'}, status=404)
        
        workbook = app.books.active
        workbook.sheets.add()
        
        return JsonResponse({'success': True, 'message': 'Foaie nouă adăugată cu succes.'}, status=200)
    except Exception as e:
        logger.error(f'Eroare la adăugarea foii: {e}')
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def next_sheet(request):
    """
    Trecerea la foaia următoare din workbook-ul activ.
    """
    try:
        app = xw.apps.active
        if app is None:
            return JsonResponse({'success': False, 'message': 'Nicio instanță activă de Excel.'}, status=404)
        
        workbook = app.books.active
        sheet = workbook.sheets.active
        current_index = sheet.index

        if current_index < len(workbook.sheets) :
            next_sheet = workbook.sheets[current_index ]
            next_sheet.activate()
            return JsonResponse({'success': True, 'message': f'Trecut la următorul sheet: {next_sheet.name}'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Deja pe ultimul sheet.'}, status=200)
    except Exception as e:
        logger.error(f'Eroare la schimbarea foii: {e}')
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def prev_sheet(request):
    """
    Trecerea la foaia anterioară din workbook-ul activ.
    """
    try:
        app = xw.apps.active
        if app is None:
            return JsonResponse({'success': False, 'message': 'Nicio instanță activă de Excel.'}, status=404)

        workbook = app.books.active
        sheet = workbook.sheets.active
        current_index = sheet.index
        if current_index > 1:
            prev_sheet = workbook.sheets[current_index - 2]
            prev_sheet.activate()
            return JsonResponse({'success': True, 'message': f'Trecut la foaia anterioară: {prev_sheet.name}'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Deja pe prima foaie.'}, status=200)
    except Exception as e:
        logger.error(f'Eroare la trecerea la foaia anterioară: {e}')
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def delete_active_sheet(request):
    """
    Șterge foaia activă din workbook-ul deschis.
    """
    try:
        app = xw.apps.active
        if app is None:
            logger.error("Nicio instanță activă de Excel. Deschideți Excel și încercați din nou.")
            return JsonResponse({'success': False, 'message': 'Niciun document Excel deschis'}, status=404)
        
        workbook = app.books.active
        active_sheet = workbook.sheets.active
        sheet_name = active_sheet.name
        
        # Verificăm dacă este ultima foaie din workbook
        if len(workbook.sheets) <= 1:
            logger.warning("Nu se poate șterge ultima foaie.")
            return JsonResponse({'success': False, 'message': 'Nu se poate șterge ultima foaie din document.'}, status=400)
        
        # Ștergem foaia activă
        active_sheet.delete()
        logger.info(f"Foaia {sheet_name} a fost ștearsă cu succes.")
        
        return JsonResponse({'success': True, 'message': f'Sheet {sheet_name} deleted successfully.'}, status=200)
    except Exception as e:
        logger.error(f"Eroare la ștergerea foii active: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def save_excel(request):
    """
    Salvează workbook-ul activ.
    """
    try:
        app = xw.apps.active
        if app is None:
            return JsonResponse({'success': False, 'message': 'Nicio instanță activă de Excel.'}, status=404)
        
        workbook = app.books.active
        workbook.save()
        
        return JsonResponse({'success': True, 'message': 'Fișier Excel salvat cu succes.'}, status=200)
    except Exception as e:
        logger.error(f'Eroare la salvarea fișierului: {e}')
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def activate_excel(request):
    try:
        pythoncom.CoInitialize()
        logger.info("COM model initialized")

        if not check_excel_open():
            logger.info("Nici un document Excel deschis")
            return JsonResponse({'success': False, 'message': 'Nici un document Excel deschis'}, status=404)

        excel_app = win32com.client.GetActiveObject("Excel.Application")
        excel_app.Visible = True
        logger.info("Excel application instance created and made visible")

        time.sleep(0.5)
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        response = JsonResponse({'success': True, 'message': 'Success'}, status=200)

        if windows:
            excel_hwnd = None
            for hwnd, window_text, class_name in windows:
                if class_name == "XLMAIN" and "Excel" in window_text:
                    excel_hwnd = hwnd
                    logger.info(f"Using Excel window handle: {excel_hwnd}")
                    break

            if excel_hwnd:
                maximize_window_if_not_maximized(excel_hwnd)

                try:
                    win32gui.BringWindowToTop(excel_hwnd)
                    win32gui.SetForegroundWindow(excel_hwnd)
                    logger.info("Excel window brought to foreground successfully.")
                except Exception as e:
                    logger.error(f"SetForegroundWindow failed: {str(e)}")
                    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_TAB, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP, 0)
                    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
                    logger.info("Used Alt+Tab as a fallback to bring window to foreground.")

                response = JsonResponse({'success': True, 'message': 'Fereastra Microsoft Excel a fost activată cu succes.'}, status=200)
            else:
                logger.error("Fereastra Microsoft Excel nu a fost găsită")
                response = JsonResponse({'success': False, 'message': 'Fereastra Microsoft Excel nu a fost găsită.'}, status=404)
        else:
            logger.error("Nu s-a găsit nicio fereastră deschisă")
            response = JsonResponse({'success': False, 'message': 'Nu s-a găsit nicio fereastră deschisă.'}, status=404)
    
    except Exception as e:
        logger.error(f"Exception in activate_excel: {str(e)}")
        response = JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    finally:
        pythoncom.CoUninitialize()
        logger.info("COM model uninitialized")

    if response.status_code != 200:
        return JsonResponse({'success': False, 'message': 'Adu manual Excel-ul în față.'}, status=response.status_code)
    
    return response


@csrf_exempt

def close_excel_window(request):
    """
    Închide instanța activă de Excel.
    """
    try:
        # Verificăm dacă există o instanță activă de Excel
        if xw.apps.count == 0:
            return JsonResponse({'success': False, 'message': 'Nicio instanță activă de Excel.'}, status=404)

        # Accesăm și închidem instanța activă de Excel
        app = xw.apps.active
        app.quit()
        logger.info("Instanța Excel a fost închisă cu succes.")
        
        return JsonResponse({'success': True, 'message': 'Excel a fost închis cu succes.'}, status=200)

    except Exception as e:
        logger.error(f"Eroare la închiderea Excel: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def scroll_up(request):
    """
    Face scroll în sus în Excel.
    """
    try:
        app = xw.apps.active
        if app is None:
            return JsonResponse({'success': False, 'message': 'Nicio instanță activă de Excel.'}, status=404)

        pyautogui.scroll(500)  
        return JsonResponse({'success': True, 'message': 'Scrolled up'}, status=200)
    except Exception as e:
        logger.error(f'Eroare la scroll up: {e}')
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def scroll_down(request):
    """
    Face scroll în jos în Excel.
    """
    try:
        app = xw.apps.active
        if app is None:
            return JsonResponse({'success': False, 'message': 'Nicio instanță activă de Excel.'}, status=404)

        pyautogui.scroll(-500)  
        return JsonResponse({'success': True, 'message': 'Scrolled down'}, status=200)
    except Exception as e:
        logger.error(f'Eroare la scroll down: {e}')
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def scroll_left(request):
    """
    Face scroll la stânga în Excel.
    """
    try:
        app = xw.apps.active
        if app is None:
            return JsonResponse({'success': False, 'message': 'Nicio instanță activă de Excel.'}, status=404)
        for _ in range(5):
            pyautogui.press('left') 
        return JsonResponse({'success': True, 'message': 'Scrolled left'}, status=200)
    except Exception as e:
        logger.error(f'Eroare la scroll left: {e}')
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def scroll_right(request):
    """
    Face scroll la dreapta în Excel.
    """
    try:
        app = xw.apps.active
        if app is None:
            return JsonResponse({'success': False, 'message': 'Nicio instanță activă de Excel.'}, status=404)
        for _ in range(5):
            pyautogui.press('right')  
        return JsonResponse({'success': True, 'message': 'Scrolled right'}, status=200)
    except Exception as e:
        logger.error(f'Eroare la scroll right: {e}')
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    
@csrf_exempt
def list_open_excel_files(request):
    """
    Returnează o listă de documente Excel deschise cu numele și calea completă.
    """
    try:
        app = xw.apps.active
        if app is None:
            return JsonResponse({'success': False, 'message': 'Nicio instanță activă de Excel.'}, status=404)

        open_files = [{'name': wb.name, 'path': wb.fullname} for wb in app.books]
        return JsonResponse({'success': True, 'files': open_files}, status=200)
    except Exception as e:
        logger.error(f'Eroare la listarea fișierelor: {e}')
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def activate_excel_file(request):
    file_path = request.GET.get('filePath')

    if not file_path:
        return JsonResponse({'success': False, 'message': 'No file path provided.'}, status=400)

    try:
        # Accesăm instanța activă a aplicației Excel
        excel_app = xw.apps.active
        if not excel_app:
            return JsonResponse({'success': False, 'message': 'No active Excel instance found.'}, status=404)
        
        found = False
        for wb in excel_app.books:
            if wb.fullname == file_path:
                found = True
                wb.activate()  # Activăm workbook-ul dorit

                # Maximizăm fereastra Excel dacă nu este deja maximizată
                excel_app.api.WindowState = xw.constants.WindowState.xlMaximized

                break  # Oprim căutarea după ce am găsit și activat workbook-ul

        if not found:
            return JsonResponse({'success': False, 'message': 'Document not found.'}, status=404)

        return JsonResponse({'success': True, 'message': f'{file_path} activated and maximized if not already.'}, status=200)

    except Exception as e:
        logger.error(f"Eroare la activarea fișierului Excel: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)