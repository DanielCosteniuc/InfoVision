from django.http import JsonResponse
import subprocess
import os
import logging
import pythoncom
import win32com.client
import time
import win32gui
import win32con
import win32api
import winreg
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def maximize_window_if_not_maximized(hwnd):
    placement = win32gui.GetWindowPlacement(hwnd)
    if placement[1] != win32con.SW_MAXIMIZE:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        logger.info("Fereastra a fost maximizată.")
    else:
        logger.info("Fereastra este deja maximizată.")
        
def is_powerpoint_running():
    try:
        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        return True if powerpoint_app.Presentations.Count > 0 else False
    except Exception as e:
        logger.info(f"PowerPoint is not running: {str(e)}")
        return False

def check_powerpoint_open():
    try:
        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        presentations = powerpoint_app.Presentations
        return presentations.Count > 0
    except:
        return False

def enum_windows_callback(hwnd, results):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        window_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        if "PowerPoint" in window_text and class_name == "PPTFrameClass":
            results.append(hwnd)

def get_powerpoint_path():
    potential_paths = [
        r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
        r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE"
    ]
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\powerpnt.exe") as key:
            powerpoint_path, _ = winreg.QueryValueEx(key, "")
            return powerpoint_path
    except Exception as e:
        logger.error(f"Could not find PowerPoint path in the registry: {str(e)}")

    for path in potential_paths:
        if os.path.exists(path):
            return path

    return None

@csrf_exempt
def open_powerpoint(request):
    try:
        logger.info("Received request to open Microsoft PowerPoint")
        
        if is_powerpoint_running():
            logger.info("Microsoft PowerPoint is already running")
            return activate_powerpoint(request)

        powerpoint_exe_path = get_powerpoint_path()
        if not powerpoint_exe_path:
            return JsonResponse({'success': False, 'message': 'Microsoft PowerPoint executable not found.'}, status=404)
        
        logger.info(f"Checking if PowerPoint executable exists at: {powerpoint_exe_path}")
        if os.path.exists(powerpoint_exe_path):
            result = subprocess.Popen(
                [powerpoint_exe_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            logger.info("Microsoft PowerPoint opened successfully")

            time.sleep(1) 

            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)

            if windows:
                hwnd = windows[0]
                maximize_window_if_not_maximized(hwnd)

                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

                logger.info("Microsoft PowerPoint window maximized and brought to foreground")
            else:
                logger.error("Microsoft PowerPoint window not found after opening")

            return JsonResponse({'success': True, 'message': 'Microsoft PowerPoint opened and maximized successfully.'}, status=200)
        else:
            logger.error("Microsoft PowerPoint executable not found")
            return JsonResponse({'success': False, 'message': 'Microsoft PowerPoint executable not found.'}, status=404)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while opening Microsoft PowerPoint: {e.stderr.decode()}")
        return JsonResponse({'success': False, 'message': e.stderr.decode()}, status=500)
    except Exception as e:
        logger.error(f"Exception while opening Microsoft PowerPoint: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def add_slide(request):
    try:
        pythoncom.CoInitialize()
        if not check_powerpoint_open():
            return JsonResponse({'success': False, 'message': 'Nici o prezentare PowerPoint deschisă'}, status=404)

        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        presentation = powerpoint_app.ActivePresentation
        slides = presentation.Slides
        slides.Add(slides.Count + 1, 1)

        return JsonResponse({'success': True, 'message': 'Slide adăugat cu succes.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def save_presentation(request):
    try:
        pythoncom.CoInitialize()
        if not check_powerpoint_open():
            return JsonResponse({'success': False, 'message': 'Nici o prezentare PowerPoint deschisă'}, status=404)

        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        presentation = powerpoint_app.ActivePresentation
        presentation.Save()

        return JsonResponse({'success': True, 'message': 'Prezentare salvată cu succes.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def delete_slide(request):
    try:
        pythoncom.CoInitialize()
        if not check_powerpoint_open():
            return JsonResponse({'success': False, 'message': 'Nici o prezentare PowerPoint deschisă'}, status=404)

        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        presentation = powerpoint_app.ActivePresentation
        slides = presentation.Slides
        if slides.Count > 0:
            slides(slides.Count).Delete()

        return JsonResponse({'success': True, 'message': 'Slide șters cu succes.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def start_presentation(request):
    try:
        pythoncom.CoInitialize()
        if not check_powerpoint_open():
            return JsonResponse({'success': False, 'message': 'Nici o prezentare PowerPoint deschisă'}, status=404)

        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        presentation = powerpoint_app.ActivePresentation
        presentation.SlideShowSettings.Run()

        return JsonResponse({'success': True, 'message': 'Prezentare pornită cu succes.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def next_slide(request):
    try:
        pythoncom.CoInitialize()
        if not check_powerpoint_open():
            return JsonResponse({'success': False, 'message': 'Nici o prezentare PowerPoint deschisă'}, status=404)

        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        presentation = powerpoint_app.ActivePresentation
        presentation.SlideShowWindow.View.Next()

        return JsonResponse({'success': True, 'message': 'Slide următor.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def previous_slide(request):
    try:
        pythoncom.CoInitialize()
        if not check_powerpoint_open():
            return JsonResponse({'success': False, 'message': 'Nici o prezentare PowerPoint deschisă'}, status=404)

        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        presentation = powerpoint_app.ActivePresentation
        presentation.SlideShowWindow.View.Previous()

        return JsonResponse({'success': True, 'message': 'Slide anterior.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def increase_volume(request):
    try:
       
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys(chr(175))

        return JsonResponse({'success': True, 'message': 'Volum mărit.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def decrease_volume(request):
    try:

        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys(chr(174))

        return JsonResponse({'success': True, 'message': 'Volum micșorat.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def stop_presentation(request):
    try:
        pythoncom.CoInitialize()

        if not check_powerpoint_open():
            return JsonResponse({'success': False, 'message': 'Nici o prezentare PowerPoint deschisă'}, status=404)

        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        presentation = powerpoint_app.ActivePresentation
        presentation.SlideShowWindow.View.Exit()

        return JsonResponse({'success': True, 'message': 'Prezentare oprită cu succes.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def go_to_first_slide(request):
    try:
        pythoncom.CoInitialize()

        if not check_powerpoint_open():
            return JsonResponse({'success': False, 'message': 'Nici o prezentare PowerPoint deschisă'}, status=404)

        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        presentation = powerpoint_app.ActivePresentation
        presentation.Slides(1).Select()

        return JsonResponse({'success': True, 'message': 'Mers la primul slide cu succes.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def go_to_last_slide(request):
    try:
        pythoncom.CoInitialize()

        if not check_powerpoint_open():
            return JsonResponse({'success': False, 'message': 'Nici o prezentare PowerPoint deschisă'}, status=404)

        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        presentation = powerpoint_app.ActivePresentation
        slide_count = presentation.Slides.Count
        presentation.Slides(slide_count).Select()

        return JsonResponse({'success': True, 'message': 'Mers la ultimul slide cu succes.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def activate_powerpoint(request):
    try:
        pythoncom.CoInitialize()
        logger.info("COM model initialized")

        if not check_powerpoint_open():
            logger.info("Nici o prezentare PowerPoint deschisă")
            return JsonResponse({'success': False, 'message': 'Nici o prezentare PowerPoint deschisă'}, status=404)

        powerpoint_app = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint_app.Visible = True
        logger.info("PowerPoint application instance created and made visible")

        time.sleep(0.5)
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)

        if windows:
            ppt_hwnd = windows[-1]
            logger.info(f"Using PowerPoint window handle: {ppt_hwnd}")

            maximize_window_if_not_maximized(ppt_hwnd)

            try:
                win32gui.BringWindowToTop(ppt_hwnd)
                win32gui.SetForegroundWindow(ppt_hwnd)
                logger.info("PowerPoint window brought to foreground successfully.")
            except Exception as e:
                logger.error(f"SetForegroundWindow failed: {str(e)}")
                win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
                win32api.keybd_event(win32con.VK_TAB, 0, 0, 0)
                win32api.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
                logger.info("Used Alt+Tab as a fallback to bring window to foreground.")

            return JsonResponse({'success': True, 'message': 'Fereastra Microsoft PowerPoint a fost activată cu succes.'}, status=200)
        else:
            logger.error("Fereastra Microsoft PowerPoint nu a fost găsită")
            return JsonResponse({'success': False, 'message': 'Fereastra Microsoft PowerPoint nu a fost găsită.'}, status=404)
    except Exception as e:
        logger.error(f"Exception in activate_powerpoint: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()
        logger.info("COM model uninitialized")


@csrf_exempt
def close_powerpoint(request):
    try:
        pythoncom.CoInitialize()

        powerpoint = win32com.client.GetObject(None, "PowerPoint.Application")

        powerpoint.Quit()

        pythoncom.CoUninitialize()

        return JsonResponse({'success': True, 'message': 'Microsoft PowerPoint a fost închis cu succes.'}, status=200)
    except Exception as e:
        logger.error(f"Exception while closing Microsoft PowerPoint: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)