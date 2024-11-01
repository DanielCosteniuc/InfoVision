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
    try:

        if check_excel_open():
            return activate_excel(request)

        excel_exe_path = get_excel_path()
        if excel_exe_path and os.path.exists(excel_exe_path):
            result = subprocess.run(
                [excel_exe_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            return JsonResponse({'success': True, 'output': result.stdout.decode()})
        else:
            return JsonResponse({'success': False, 'message': 'Microsoft Excel executable not found.'}, status=404)
    except subprocess.CalledProcessError as e:
        return JsonResponse({'success': False, 'message': e.stderr.decode()}, status=500)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)




@csrf_exempt
def add_sheet(request):
    def try_add_sheet():
        try:
            pythoncom.CoInitialize()

            if not check_excel_open():
                return JsonResponse({'success': False, 'message': 'Niciun document Excel deschis'}, status=404)

            excel_app = win32com.client.Dispatch("Excel.Application")
            excel_app.Visible = True
            time.sleep(0.5)

            workbook = excel_app.ActiveWorkbook
            workbook.Sheets.Add()

            return JsonResponse({'success': True, 'message': 'Foaia nouă a fost adăugată cu succes.'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            pythoncom.CoUninitialize()

    response = try_add_sheet()

    if response.status_code != 200 :
        pyautogui.press('enter')
        time.sleep(0.5) 
        response = try_add_sheet()

    if response.status_code != 200:
        minimize_and_maximize_excel()
        response = try_add_sheet()
    return response


@csrf_exempt
def next_sheet(request):
    
    def try_next_sheet():
        try:
            pythoncom.CoInitialize()

            excel_app = win32com.client.Dispatch("Excel.Application")
            if not excel_app.Workbooks.Count:
                return JsonResponse({'success': False, 'message': 'No workbooks are open'}, status=404)

            workbook = excel_app.ActiveWorkbook
            current_sheet = excel_app.ActiveSheet
            sheets = workbook.Sheets
            current_index = current_sheet.Index

            if current_index < sheets.Count:
                sheets(current_index + 1).Activate()
                return JsonResponse({'success': True, 'message': 'Moved to the next sheet.'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Already on the last sheet.'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            pythoncom.CoUninitialize()

    response = try_next_sheet()

    if response.status_code != 200:
        pyautogui.press('enter')
        time.sleep(0.5)
        response = try_next_sheet()

    if response.status_code != 200:
        minimize_and_maximize_excel()
        response = try_next_sheet()

    return response



@csrf_exempt
def prev_sheet(request):
    def try_prev_sheet():
        try:
            pythoncom.CoInitialize()

            if not check_excel_open():
                return JsonResponse({'success': False, 'message': 'Niciun document Excel deschis'}, status=404)

            excel_app = win32com.client.Dispatch("Excel.Application")
            workbook = excel_app.ActiveWorkbook
            current_sheet = excel_app.ActiveSheet
            sheets = workbook.Sheets
            current_index = current_sheet.Index

            if current_index > 1:
                sheets(current_index - 1).Activate()
                return JsonResponse({'success': True, 'message': 'Moved to the previous sheet.'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Already on the first sheet.'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            pythoncom.CoUninitialize()

    response = try_prev_sheet()

    if response.status_code != 200 :
        pyautogui.press('enter')
        time.sleep(0.5) 
        response = try_prev_sheet()
    
    if response.status_code != 200:
        minimize_and_maximize_excel()
        response = try_prev_sheet()

    return response

@csrf_exempt
def delete_active_sheet(request):
    def try_delete_sheet():
        try:
            pythoncom.CoInitialize()

            if not check_excel_open():
                return JsonResponse({'success': False, 'message': 'Niciun document Excel deschis'}, status=404)

            excel_app = win32com.client.Dispatch("Excel.Application")
            excel_app.Visible = True
            time.sleep(0.5)

            active_sheet = excel_app.ActiveSheet
            sheet_name = active_sheet.Name
            active_sheet.Delete()

            return JsonResponse({'success': True, 'message': f'Sheet {sheet_name} deleted successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            pythoncom.CoUninitialize()

    response = try_delete_sheet()

    if response.status_code != 200 :
        pyautogui.press('enter')
        time.sleep(0.5) 
        response = try_delete_sheet()
        
    if response.status_code != 200:
        minimize_and_maximize_excel()
        response = try_delete_sheet()

    return response


@csrf_exempt
def save_excel(request):
    def try_save_excel():
        try:
            pythoncom.CoInitialize()

            excel_app = win32com.client.Dispatch("Excel.Application")
            if excel_app.Workbooks.Count == 0:
                return JsonResponse({'success': False, 'message': 'Niciun fișier Excel deschis'}, status=40)

            workbook = excel_app.ActiveWorkbook
            workbook.Save()

            return JsonResponse({'success': True, 'message': 'Fișier Excel salvat cu succes.'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            pythoncom.CoUninitialize()

    response = try_save_excel()
    
    if response.status_code != 200  :
        pyautogui.press('enter')
        time.sleep(0.5)
        response = try_save_excel()
        
    if response.status_code != 200:
        minimize_and_maximize_excel()
        response = try_save_sheet()

    return response


@csrf_exempt
def activate_excel(request):
    try:
        pythoncom.CoInitialize()
        logger.info("COM model initialized")

        if not check_excel_open():
            logger.info("Nici un document Excel deschis")
            return JsonResponse({'success': False, 'message': 'Nici un document Excel deschis'}, status=404)

        excel_app = win32com.client.Dispatch("Excel.Application")
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
    try:
        subprocess.run(["taskkill", "/F", "/IM", "EXCEL.EXE"], check=True)
        
        return JsonResponse({'success': True, 'message': 'Excel closed successfully.'}, status=200)
    except subprocess.CalledProcessError as e:
        return JsonResponse({'success': False, 'message': 'Failed to close Excel.'}, status=500)



@csrf_exempt
def scroll_up(request):
    def try_scroll_up():
        try:
            pythoncom.CoInitialize()

            if not check_excel_open():
                return JsonResponse({'success': False, 'message': 'Niciun document Excel deschis'}, status=404)

            pyautogui.scroll(500)  
            return JsonResponse({'success': True, 'message': 'Scrolled up'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            pythoncom.CoUninitialize()

    response = try_scroll_up()

    if response.status_code != 200:
        pyautogui.press('enter')
        time.sleep(0.5)
        response = try_scroll_up()

    if response.status_code != 200:
        minimize_and_maximize_excel()
        response = try_scroll_up()

    return response


@csrf_exempt
def scroll_down(request):
    def try_scroll_down():
        try:
            pythoncom.CoInitialize()

            if not check_excel_open():
                return JsonResponse({'success': False, 'message': 'Niciun document Excel deschis'}, status=404)

            pyautogui.scroll(-500)  
            return JsonResponse({'success': True, 'message': 'Scrolled down'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            pythoncom.CoUninitialize()

    response = try_scroll_down()

    if response.status_code != 200:
        pyautogui.press('enter')
        time.sleep(0.5)
        response = try_scroll_down()

    if response.status_code != 200:
        minimize_and_maximize_excel()
        response = try_scroll_down()

    return response


@csrf_exempt
def scroll_left(request):
    def try_scroll_left():
        try:
            pythoncom.CoInitialize()

            if not check_excel_open():
                return JsonResponse({'success': False, 'message': 'Niciun document Excel deschis'}, status=404)
            for i in range(5):
                pyautogui.press('left') 
            return JsonResponse({'success': True, 'message': 'Scrolled left successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            pythoncom.CoUninitialize()

    response = try_scroll_left()

    if response.status_code != 200:
        pyautogui.press('enter')
        time.sleep(0.5)
        response = try_scroll_left()

    if response.status_code != 200:
        minimize_and_maximize_excel()
        response = try_scroll_left()

    return response


@csrf_exempt
def scroll_right(request):
    def try_scroll_right():
        try:
            pythoncom.CoInitialize()

            if not check_excel_open():
                return JsonResponse({'success': False, 'message': 'Niciun document Excel deschis'}, status=404)
            for i in range(5):
                pyautogui.press('right')  
            return JsonResponse({'success': True, 'message': 'Scrolled right successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            pythoncom.CoUninitialize()

    response = try_scroll_right()

    if response.status_code != 200:
        pyautogui.press('enter')
        time.sleep(0.5)
        response = try_scroll_right()

    if response.status_code != 200:
        minimize_and_maximize_excel()
        response = try_scroll_right()

    return response
