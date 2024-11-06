import os
import winreg
import subprocess
import logging
import pythoncom
import win32com.client
import time
import win32gui
import win32con
import win32api
import pyautogui
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

def get_word_path():
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\winword.exe") as key:
            word_path, _ = winreg.QueryValueEx(key, "")
            return word_path
    except Exception as e:
        logger.error(f"Could not find Word path in the registry: {str(e)}")
        return None

def is_word_running():
    try:
        word_app = win32com.client.GetActiveObject("Word.Application")
        return True if word_app.Documents.Count > 0 else False
    except Exception as e:
        logger.info(f"Word is not running: {str(e)}")
        return False

def check_word_open():
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return len(windows) > 0

def initialize_word():
    try:
        pythoncom.CoInitialize()
        try:
            word_app = win32com.client.GetObject(None, "Word.Application")
            logger.info("Found an existing instance of Word.")
        except Exception as e:
            logger.warning(f"Could not find an active Word instance: {str(e)}")
            return None, JsonResponse({'success': False, 'message': 'Nu s-a găsit o instanță activă de Microsoft Word.'}, status=404)
        
        return word_app, None
    except Exception as e:
        logger.error(f"Error initializing Word: {str(e)}")
        return None, JsonResponse({'success': False, 'message': 'Nu s-a putut inițializa Microsoft Word.'}, status=500)


def minimize_and_restore_window(hwnd):
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        logger.info(f"Minimized window with hwnd: {hwnd}")
        time.sleep(0.5)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        logger.info(f"Restored window with hwnd: {hwnd}")
    except Exception as e:
        logger.error(f"Could not minimize/restore window with hwnd: {hwnd}. Error: {e}")

def minimize_and_maximize_word():
    pyautogui.hotkey('win', 'd') 
    time.sleep(0.1)  
    pyautogui.hotkey('win', 'd')  
    time.sleep(0.1)

def enum_windows_callback(hwnd, results):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        window_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        logger.info(f"Fereastră activă detectată: hwnd={hwnd}, text='{window_text}', class_name='{class_name}'")

        if class_name == "OpusApp":
            logger.info(f"OpusApp window detected with hwnd={hwnd}, text='{window_text}'")
            minimize_and_restore_window(hwnd)

        results.append((hwnd, window_text, class_name))

def maximize_window_if_not_maximized(hwnd):
    placement = win32gui.GetWindowPlacement(hwnd)
    if placement[1] != win32con.SW_MAXIMIZE:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        logger.info("Fereastra a fost maximizată.")
    else:
        logger.info("Fereastra este deja maximizată.")

@csrf_exempt
def open_word(request):
    
    try:
        logger.info("Received request to open Microsoft Word")
        
        if is_word_running():
            logger.info("Microsoft Word is already running")
            return activate_word(request)

        word_exe_path = get_word_path()
        if word_exe_path:
            logger.info(f"Found Word executable at: {word_exe_path}")
            result = subprocess.run(
                [word_exe_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            logger.info("Microsoft Word opened successfully")
            return JsonResponse({'success': True, 'output': result.stdout.decode()})
        else:
            logger.error("Microsoft Word executable not found")
            return JsonResponse({'success': False, 'message': 'Microsoft Word executable not found in registry.'}, status=404)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while opening Microsoft Word: {e.stderr.decode()}")
        return JsonResponse({'success': False, 'message': e.stderr.decode()}, status=500)
    except Exception as e:
        logger.error(f"Exception while opening Microsoft Word: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def activate_word(request):
    def try_activate_word():
        try:
            pythoncom.CoInitialize()
            logger.info("COM model initialized")

            try:
                word_app = win32com.client.GetObject(None, "Word.Application")
                logger.info("Found an existing instance of Word.")
            except Exception as e:
                logger.error(f"Could not find an active Word instance: {str(e)}")
                return JsonResponse({'success': False, 'message': 'Nici un document Word deschis.'}, status=404)

            word_app.Visible = True
            logger.info("Word application instance made visible")
            time.sleep(0.5)

            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)

            if windows:
                word_hwnd = None
                for hwnd, window_text, class_name in windows:
                    if class_name == "OpusApp" and "Word" in window_text:
                        word_hwnd = hwnd
                        logger.info(f"Using Word window handle: {word_hwnd}")
                        break

                if word_hwnd:
                    maximize_window_if_not_maximized(word_hwnd)
                    try:
                        win32gui.ShowWindow(word_hwnd, win32con.SW_MINIMIZE)
                        logger.info("Minimized Word window")
                        time.sleep(0.5)
                        win32gui.ShowWindow(word_hwnd, win32con.SW_RESTORE)
                        logger.info("Restored Word window")
                        win32gui.SetForegroundWindow(word_hwnd)
                        logger.info("Brought Word window to foreground")
                    except Exception as e:
                        logger.error(f"SetForegroundWindow failed: {str(e)}")
                        win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)  
                        win32api.keybd_event(win32con.VK_TAB, 0, 0, 0)   
                        win32api.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP, 0)  
                        win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)  
                        logger.info("Used Alt+Tab to bring Word window to foreground")

                    return JsonResponse({'success': True, 'message': 'Fereastra Microsoft Word a fost activată cu succes.'}, status=200)
                else:
                    logger.error("Fereastra Microsoft Word nu a fost găsită")
                    return JsonResponse({'success': False, 'message': 'Fereastra Microsoft Word nu a fost găsită.'}, status=404)
            else:
                logger.error("Nu s-a găsit nicio fereastră deschisă")
                return JsonResponse({'success': False, 'message': 'Nu s-a găsit nicio fereastră deschisă.'}, status=404)
        except Exception as e:
            logger.error(f"Exception in activate_word: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            pythoncom.CoUninitialize()
            logger.info("COM model uninitialized")

    response = try_activate_word()

    if response.status_code != 200:
        logger.info("Attempting to minimize and maximize windows, then retry Word activation.")
        minimize_and_maximize_word()
        response = try_activate_word()

    return response

@csrf_exempt
def go_to_end(request):
    def try_go_to_end():
        try:
            logger.info("Received request to go to end of the document")
            word_app, error_response = initialize_word()
            if error_response:
                return error_response

            if word_app.Documents.Count == 0:
                logger.error("No active documents found in Word.")
                return JsonResponse({'success': False, 'message': 'Nu există documente active deschise în Word.'}, status=404)

            selection = word_app.Selection
            selection.EndKey(Unit=6)

            logger.info("Moved to the end of the document successfully")
            return JsonResponse({'success': True, 'message': 'Moved to the end of the document successfully.'})
        finally:
            pythoncom.CoUninitialize()

    response = try_go_to_end()
    if response.status_code != 200:
        minimize_and_maximize_word()
        response = try_go_to_end()

    return response

@csrf_exempt
def go_to_start(request):
    def try_go_to_start():
        try:
            logger.info("Received request to go to start of the document")
            word_app, error_response = initialize_word()
            if error_response:
                return error_response

            if word_app.Documents.Count == 0:
                logger.error("No active documents found in Word.")
                return JsonResponse({'success': False, 'message': 'Nu există documente active deschise în Word.'}, status=404)

            selection = word_app.Selection
            selection.HomeKey(Unit=6)

            logger.info("Moved to the start of the document successfully")
            return JsonResponse({'success': True, 'message': 'Moved to the start of the document successfully.'})
        finally:
            pythoncom.CoUninitialize()

    response = try_go_to_start()
    if response.status_code != 200:
        minimize_and_maximize_word()
        response = try_go_to_start()

    return response

@csrf_exempt
def page_down(request):
    def try_page_down():
        try:
            logger.info("Received request to go to next page")
            word_app, error_response = initialize_word()
            if error_response:
                return error_response

            selection = word_app.Selection
            selection.GoTo(What=1, Which=2)

            logger.info("Moved to the next page successfully")
            return JsonResponse({'success': True, 'message': 'Moved to the next page successfully.'})
        finally:
            pythoncom.CoUninitialize()

    response = try_page_down()
    if response.status_code != 200:
        minimize_and_maximize_word()
        response = try_page_down()

    return response

@csrf_exempt
def page_up(request):
    def try_page_up():
        try:
            logger.info("Received request to go to previous page")
            word_app, error_response = initialize_word()
            if error_response:
                return error_response

            selection = word_app.Selection
            selection.GoTo(What=1, Which=3)

            logger.info("Moved to the previous page successfully")
            return JsonResponse({'success': True, 'message': 'Moved to the previous page successfully.'})
        finally:
            pythoncom.CoUninitialize()

    response = try_page_up()
    if response.status_code != 200:
        minimize_and_maximize_word()
        response = try_page_up()

    return response

@csrf_exempt
def save_as(request):
    def try_save_as():
        try:
            logger.info("Received request to save document in Microsoft Word")
            word_app, error_response = initialize_word()
            if error_response:
                return error_response

            if word_app.Documents.Count == 0:
                logger.error("No active documents found in Word.")
                return JsonResponse({'success': False, 'message': 'Nu există documente active deschise în Word.'}, status=404)

            doc = word_app.ActiveDocument
            save_path = os.path.join(os.path.expanduser("~"), "Documents", "SavedDocument.docx")
            doc.SaveAs2(save_path)

            logger.info(f"Document saved successfully to {save_path}")
            return JsonResponse({'success': True, 'message': f'Document saved successfully to {save_path}.'})
        finally:
            pythoncom.CoUninitialize()

    response = try_save_as()
    if response.status_code != 200:
        minimize_and_maximize_word()
        response = try_save_as()

    return response

@csrf_exempt
def zoom_in(request):
    def try_zoom_in():
        try:
            logger.info("Received request to zoom in")
            word_app, error_response = initialize_word()
            if error_response:
                return error_response

            doc = word_app.Documents.Item(1)
            view = doc.ActiveWindow.View

            if view.ReadingLayout:
                logger.info("Exiting Read Mode to apply zoom")
                view.ReadingLayout = False

            current_zoom = view.Zoom.Percentage
            new_zoom = min(current_zoom + 10, 500)
            view.Zoom.Percentage = new_zoom

            logger.info("Zoomed in successfully")
            return JsonResponse({'success': True, 'message': f'Zoomed in successfully to {new_zoom}%.'})
        finally:
            pythoncom.CoUninitialize()

    response = try_zoom_in()
    if response.status_code != 200:
        minimize_and_maximize_word()
        response = try_zoom_in()

    return response

@csrf_exempt
def zoom_out(request):
    def try_zoom_out():
        try:
            logger.info("Received request to zoom out")
            word_app, error_response = initialize_word()
            if error_response:
                return error_response

            if word_app.Documents.Count == 0:
                logger.error("No active documents found in Word.")
                return JsonResponse({'success': False, 'message': 'Nu există documente active deschise în Word.'}, status=404)

            doc = word_app.ActiveDocument
            view = doc.ActiveWindow.View

            if view.ReadingLayout:
                logger.info("Exiting Read Mode to apply zoom")
                view.ReadingLayout = False

            current_zoom = view.Zoom.Percentage
            new_zoom = max(current_zoom - 10, 10)
            view.Zoom.Percentage = new_zoom

            logger.info("Zoomed out successfully")
            return JsonResponse({'success': True, 'message': f'Zoomed out successfully to {new_zoom}%.'})
        finally:
            pythoncom.CoUninitialize()

    response = try_zoom_out()
    if response.status_code != 200:
        minimize_and_maximize_word()
        response = try_zoom_out()

    return response

@csrf_exempt
def read_mode(request):
    def try_read_mode():
        try:
            logger.info("Received request to activate Read Mode in Microsoft Word")
            word_app, error_response = initialize_word()
            if error_response:
                return error_response

            doc = word_app.Documents.Item(1)
            doc.ActiveWindow.View.ReadingLayout = True

            logger.info("Read Mode activated successfully")
            return JsonResponse({'success': True, 'message': 'Read Mode activated successfully.'})
        finally:
            pythoncom.CoUninitialize()

    response = try_read_mode()
    if response.status_code != 200:
        minimize_and_maximize_word()
        response = try_read_mode()

    return response

@csrf_exempt
def read_mode_next_page(request):
    def try_read_mode_next_page():
        try:
            logger.info("Received request to go to next page in Read Mode")
            word_app, error_response = initialize_word()
            if error_response:
                return error_response

            view = word_app.ActiveWindow.View
            if view.ReadingLayout:
                word_app.ActiveWindow.SmallScroll(Down=1)

            logger.info("Moved to the next page in Read Mode successfully")
            return JsonResponse({'success': True, 'message': 'Moved to the next page in Read Mode successfully.'})
        finally:
            pythoncom.CoUninitialize()

    response = try_read_mode_next_page()
    if response.status_code != 200:
        minimize_and_maximize_word()
        response = try_read_mode_next_page()

    return response

@csrf_exempt
def read_mode_previous_page(request):
    def try_read_mode_previous_page():
        try:
            logger.info("Received request to go to previous page in Read Mode")
            word_app, error_response = initialize_word()
            if error_response:
                return error_response

            view = word_app.ActiveWindow.View
            if view.ReadingLayout:
                word_app.ActiveWindow.SmallScroll(Down=-1)

            logger.info("Moved to the previous page in Read Mode successfully")
            return JsonResponse({'success': True, 'message': 'Moved to the previous page in Read Mode successfully.'})
        finally:
            pythoncom.CoUninitialize()

    response = try_read_mode_previous_page()
    if response.status_code != 200:
        minimize_and_maximize_word()
        response = try_read_mode_previous_page()

    return response

@csrf_exempt
def exit_read_mode(request):
    def try_exit_read_mode():
        try:
            logger.info("Received request to deactivate Read Mode in Microsoft Word")
            word_app, error_response = initialize_word()
            if error_response:
                return error_response

            doc = word_app.Documents.Item(1)
            doc.ActiveWindow.View.ReadingLayout = False

            logger.info("Read Mode deactivated successfully")
            return JsonResponse({'success': True, 'message': 'Read Mode deactivated successfully.'})
        finally:
            pythoncom.CoUninitialize()

    response = try_exit_read_mode()
    if response.status_code != 200:
        minimize_and_maximize_word()
        response = try_exit_read_mode()

    return response

@csrf_exempt
def close_word(request):
    def try_close_word():
        try:
            pythoncom.CoInitialize()

            word = win32com.client.GetObject(None, "Word.Application")
            word.Quit()

            return JsonResponse({'success': True, 'message': 'Microsoft Word a fost închis cu succes.'}, status=200)
        except Exception as e:
            logger.error(f"Exception while closing Microsoft Word: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            pythoncom.CoUninitialize()

    response = try_close_word()
    if response.status_code != 200:
        logger.info("Attempting to minimize and maximize windows, then retry closing Word.")
        minimize_and_maximize_word()
        response = try_close_word()

    return response


# Funcție pentru a obține lista fișierelor Word deschise
@csrf_exempt
def list_open_word_files(request):
    try:
        pythoncom.CoInitialize()  # Inițializează COM pentru interacțiunea cu Word
        word_app = win32com.client.GetActiveObject("Word.Application")
        if word_app.Documents.Count == 0:
            return JsonResponse({'success': True, 'files': []})

        # Obținem lista de fișiere deschise
        open_files = [{'name': doc.Name, 'path': doc.FullName} for doc in word_app.Documents]
        
        return JsonResponse({'success': True, 'files': open_files}, status=200)
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    finally:
        pythoncom.CoUninitialize()  # Dezactivează COM
        
@csrf_exempt
def activate_word_file(request):
    file_path = request.GET.get('filePath')

    if not file_path:
        return JsonResponse({'success': False, 'message': 'No file path provided.'}, status=400)

    try:
        pythoncom.CoInitialize()
        word_app = win32com.client.GetActiveObject("Word.Application")

        # Verificăm toate documentele deschise și activăm cel cu calea potrivită
        for doc in word_app.Documents:
            if doc.FullName == file_path:
                doc.Activate()  # Activăm documentul
                return JsonResponse({'success': True, 'message': f'{doc.Name} activated.'}, status=200)

        return JsonResponse({'success': False, 'message': 'Document not found.'}, status=404)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def list_open_word_files(request):
    """
    Returnează o listă de documente Word deschise cu numele și calea completă.
    """
    try:
        pythoncom.CoInitialize()  # Inițializează COM pentru interacțiunea cu Word
        word_app = win32com.client.GetActiveObject("Word.Application")
        
        # Verifică dacă există documente deschise
        if word_app.Documents.Count == 0:
            return JsonResponse({'success': True, 'files': []})

        # Obținem lista de fișiere deschise
        open_files = [{'name': doc.Name, 'path': doc.FullName} for doc in word_app.Documents]
        
        return JsonResponse({'success': True, 'files': open_files}, status=200)
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    finally:
        pythoncom.CoUninitialize()  # Dezactivează COM
        
@csrf_exempt
def activate_word_file(request):
    """
    Activează un document Word deschis, identificat prin calea completă.
    """
    file_path = request.GET.get('filePath')

    if not file_path:
        return JsonResponse({'success': False, 'message': 'No file path provided.'}, status=400)

    try:
        pythoncom.CoInitialize()  # Inițializează COM
        word_app = win32com.client.GetActiveObject("Word.Application")

        # Căutăm documentul deschis cu calea specificată și îl activăm
        for doc in word_app.Documents:
            if doc.FullName == file_path:
                doc.Activate()  # Activăm documentul
                return JsonResponse({'success': True, 'message': f'{doc.Name} activated.'}, status=200)

        return JsonResponse({'success': False, 'message': 'Document not found.'}, status=404)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    finally:
        pythoncom.CoUninitialize()  # Dezactivează COM

