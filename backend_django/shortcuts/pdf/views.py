import os
import subprocess
import logging
import time
import pythoncom
import win32gui
import win32con
import win32com.client
from pywinauto import Application
import ctypes
from ctypes import wintypes
import winreg
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import pyautogui
import time

logger = logging.getLogger(__name__)

def enum_windows_callback(hwnd, results):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        window_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        if "Adobe Acrobat" in window_text or "Acrobat" in class_name:
            results.append((hwnd, window_text, class_name))

def find_acrobat_window():
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    for hwnd, window_text, class_name in windows:
        if class_name == "AcrobatSDIWindow" and "Adobe Acrobat" in window_text:
            return hwnd
    return None

def maximize_window_if_not_maximized(hwnd):
    placement = win32gui.GetWindowPlacement(hwnd)
    if placement[1] != win32con.SW_MAXIMIZE:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        logger.info("Fereastra a fost maximizată.")
    else:
        logger.info("Fereastra este deja maximizată.")

def get_acrobat_path():
    potential_paths = [
        r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
        r"C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
        os.path.expanduser(r"~\AppData\Local\Adobe\Acrobat DC\Acrobat\Acrobat.exe")
    ]
    
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Acrobat.exe") as key:
            acrobat_path, _ = winreg.QueryValueEx(key, "")
            return acrobat_path
    except Exception as e:
        logger.error(f"Could not find Acrobat path in the registry: {str(e)}")

    for path in potential_paths:
        if os.path.exists(path):
            return path

    return None

@csrf_exempt
def open_acrobat(request):
    try:
        logger.info("Received request to open Adobe Acrobat DC")
        
        acrobat_exe_path = get_acrobat_path()
        if not acrobat_exe_path:
            return JsonResponse({'success': False, 'message': 'Adobe Acrobat DC executable not found.'}, status=404)
        
        logger.info(f"Checking if Acrobat executable exists at: {acrobat_exe_path}")
        if os.path.exists(acrobat_exe_path):
            process = subprocess.Popen(
                [acrobat_exe_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            logger.info("Adobe Acrobat DC opened successfully")
            return JsonResponse({'success': True, 'message': 'Adobe Acrobat DC opened successfully.'}, status=200)
        else:
            logger.error("Adobe Acrobat DC executable not found")
            return JsonResponse({'success': False, 'message': 'Adobe Acrobat DC executable not found.'}, status=404)
    except Exception as e:
        logger.error(f"Exception while opening Adobe Acrobat DC: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def activate_acrobat(request):
    try:
        pythoncom.CoInitialize()

        acrobat_hwnd = find_acrobat_window()

        if acrobat_hwnd:

            win32gui.ShowWindow(acrobat_hwnd, win32con.SW_MINIMIZE)
            time.sleep(0.5)
            win32gui.ShowWindow(acrobat_hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(acrobat_hwnd)
            maximize_window_if_not_maximized(acrobat_hwnd)
            logger.info(f"Fereastra Adobe Acrobat găsită: hwnd={acrobat_hwnd}, text={win32gui.GetWindowText(acrobat_hwnd)}")
            return JsonResponse({'success': True, 'message': 'Fereastra Adobe Acrobat a fost activată cu succes.'}, status=200)
        else:
            logger.error("Fereastra Adobe Acrobat nu a fost găsită.")
            return JsonResponse({'success': False, 'message': 'Fereastra Adobe Acrobat nu a fost găsită.'}, status=404)
    except Exception as e:
        logger.error(f"Exception while activating Adobe Acrobat: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

def perform_action(action):
    try:
        pythoncom.CoInitialize()
        acrobat_hwnd = find_acrobat_window()
        if acrobat_hwnd:
            action(acrobat_hwnd)
            return JsonResponse({'success': True, 'message': 'Action performed successfully.'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Adobe Acrobat window not found.'}, status=404)
    except Exception as e:
        logger.error(f"Exception while performing action: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def next_page(request):
    def action(hwnd):
        app = Application().connect(handle=hwnd)
        window = app.window(handle=hwnd)
        window.send_keystrokes('{PGDN}')
    return perform_action(action)

@csrf_exempt
def previous_page(request):
    def action(hwnd):
        app = Application().connect(handle=hwnd)
        window = app.window(handle=hwnd)
        window.send_keystrokes('{PGUP}')
    return perform_action(action)

@csrf_exempt
def zoom_in(request):
    try:
        pythoncom.CoInitialize()

        acrobat_hwnd = find_acrobat_window()

        if acrobat_hwnd:
            logger.info(f"Fereastra activă înainte de zoom in: handle={acrobat_hwnd}")

            app = Application().connect(handle=acrobat_hwnd)
            window = app.window(handle=acrobat_hwnd)
            window.send_keystrokes('^=')

            logger.info("Zoom in executat cu succes")
            return JsonResponse({'success': True, 'message': 'Zoom in successful.'}, status=200)
        else:
            logger.error("Fereastra Adobe Acrobat nu a fost găsită.")
            return JsonResponse({'success': False, 'message': 'Fereastra Adobe Acrobat nu a fost găsită.'}, status=404)
    except Exception as e:
        logger.error(f"Exception while zooming in: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def zoom_out(request):
    try:
        pythoncom.CoInitialize()

        acrobat_hwnd = find_acrobat_window()

        if acrobat_hwnd:
            logger.info(f"Fereastra activă înainte de zoom out: handle={acrobat_hwnd}")

            app = Application().connect(handle=acrobat_hwnd)
            window = app.window(handle=acrobat_hwnd)

            window.send_keystrokes('^-')

            logger.info("Zoom out executat cu succes")
            return JsonResponse({'success': True, 'message': 'Zoom out successful.'}, status=200)
        else:
            logger.error("Fereastra Adobe Acrobat nu a fost găsită.")
            return JsonResponse({'success': False, 'message': 'Fereastra Adobe Acrobat nu a fost găsită.'}, status=404)
    except Exception as e:
        logger.error(f"Exception while zooming out: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def read_mode(request):
    try:
        pythoncom.CoInitialize()

        acrobat_hwnd = find_acrobat_window()

        if acrobat_hwnd:
            logger.info(f"Fereastra activă înainte de activarea modului de citire: handle={acrobat_hwnd}")

            app = Application().connect(handle=acrobat_hwnd)
            window = app.window(handle=acrobat_hwnd)

            window.send_keystrokes('^h')

            logger.info("Modul de citire activat cu succes")
            return JsonResponse({'success': True, 'message': 'Modul de citire activat cu succes.'}, status=200)
        else:
            logger.error("Fereastra Adobe Acrobat nu a fost găsită.")
            return JsonResponse({'success': False, 'message': 'Fereastra Adobe Acrobat nu a fost găsită.'}, status=404)
    except Exception as e:
        logger.error(f"Exception while activating read mode: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def print_pdf(request):
    try:
        pythoncom.CoInitialize()

        acrobat_hwnd = find_acrobat_window()

        if acrobat_hwnd:
            logger.info(f"Fereastra activă înainte de printare: handle={acrobat_hwnd}")

            app = Application().connect(handle=acrobat_hwnd)
            window = app.window(handle=acrobat_hwnd)

            window.send_keystrokes('^p')

            logger.info("Dialogul de printare deschis cu succes")
            return JsonResponse({'success': True, 'message': 'Dialogul de printare deschis cu succes.'}, status=200)
        else:
            logger.error("Fereastra Adobe Acrobat nu a fost găsită.")
            return JsonResponse({'success': False, 'message': 'Fereastra Adobe Acrobat nu a fost găsită.'}, status=404)
    except Exception as e:
        logger.error(f"Exception while printing: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()


@csrf_exempt
def close_acrobat(request):
    try:
        acrobat_exe_names = ['Acrobat.exe', 'AcroRd32.exe']

        for exe_name in acrobat_exe_names:
            exit_code = os.system(f"taskkill /F /IM {exe_name}")

            if exit_code == 0:
                logger.info(f"{exe_name} a fost închis cu succes.")
                return JsonResponse({'success': True, 'message': f'{exe_name} a fost închis cu succes.'}, status=200)
            else:
                logger.warning(f"Nu s-a reușit închiderea {exe_name}. Cod de ieșire: {exit_code}")

        return JsonResponse({'success': False, 'message': 'Nu s-a reușit închiderea niciunui proces Adobe Acrobat.'}, status=500)

    except Exception as e:
        logger.error(f"Excepție la închiderea Adobe Acrobat: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    
@csrf_exempt
def switch_to_next_tab(request):
    """Schimbă la următorul tab deschis în Adobe Acrobat."""
    try:
        pyautogui.hotkey('ctrl', 'tab')
        time.sleep(0.1)  # Mică întârziere pentru a permite comutarea
        return JsonResponse({'success': True, 'message': 'Switched to next tab.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def switch_to_previous_tab(request):
    """Schimbă la tab-ul anterior deschis în Adobe Acrobat."""
    try:
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        time.sleep(0.1)  # Mică întârziere pentru a permite comutarea
        return JsonResponse({'success': True, 'message': 'Switched to previous tab.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)