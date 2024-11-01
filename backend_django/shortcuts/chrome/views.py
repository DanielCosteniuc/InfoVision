import os
import subprocess
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
import pythoncom
import win32gui
import win32con
import time
import win32com.client
import psutil
import json
import asyncio
import websockets
import winreg
import pyautogui
import win32process
from pywinauto import findwindows

logger = logging.getLogger(__name__)

def find_chrome_path():
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe") as key:
            chrome_path, _ = winreg.QueryValueEx(key, "")
            return chrome_path
    except Exception as e:
        logger.error(f"Could not find Chrome path in the registry: {str(e)}")
        return None

def is_chrome_running():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] and 'chrome' in process.info['name'].lower():
            return True
    return False

def maximize_window_if_not_maximized(hwnd):
    placement = win32gui.GetWindowPlacement(hwnd)
    if placement[1] != win32con.SW_MAXIMIZE:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        logger.info("Chrome window maximized.")
    else:
        logger.info("Chrome window already maximized.")

def enum_windows_callback(hwnd, results):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        window_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        
        # Găsește ferestrele care aparțin clasei corecte și care rulează în procesul Chrome
        _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Obține PID-ul ferestrei
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['pid'] == pid and proc.info['name'] == 'chrome.exe':
                results.append((hwnd, window_text, class_name))
                break


def open_chrome_with_url(url):
    try:
        chrome_exe_path = find_chrome_path()
        if chrome_exe_path and os.path.exists(chrome_exe_path):
            result = subprocess.run(
                [chrome_exe_path, '--new-tab', url],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            return JsonResponse({'success': True, 'output': result.stdout.decode()})
        else:
            return JsonResponse({'success': False, 'message': 'Google Chrome executable not found.'}, status=404)
    except subprocess.CalledProcessError as e:
        return JsonResponse({'success': False, 'message': e.stderr.decode()}, status=500)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def open_chrome(request):
    try:
        if is_chrome_running():
            return activate_chrome(request)

        chrome_exe_path = find_chrome_path()
        if chrome_exe_path and os.path.exists(chrome_exe_path):
            result = subprocess.run(
                [chrome_exe_path, '--remote-debugging-port=9222', '--remote-allow-origins=*'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            return JsonResponse({'success': True, 'output': result.stdout.decode()})
        else:
            return JsonResponse({'success': False, 'message': 'Google Chrome executable not found.'}, status=404)
    except subprocess.CalledProcessError as e:
        return JsonResponse({'success': False, 'message': e.stderr.decode()}, status=500)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def activate_chrome(request):
    try:
        pythoncom.CoInitialize()
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)

        chrome_hwnd = None
        for hwnd, window_text, class_name in windows:
            if class_name == "Chrome_WidgetWin_1" and "Chrome" in window_text:
                chrome_hwnd = hwnd
                break

        if chrome_hwnd:
            #maximize_window_if_not_maximized(chrome_hwnd)
            #win32gui.ShowWindow(chrome_hwnd, win32con.SW_MINIMIZE)
            #time.sleep(0.5)
            win32gui.ShowWindow(chrome_hwnd, win32con.SW_MAXIMIZE)
            win32gui.SetForegroundWindow(chrome_hwnd)
            return JsonResponse({'success': True, 'message': 'Chrome window activated successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Chrome window not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    finally:
        pythoncom.CoUninitialize()
        
@csrf_exempt
def close_current_tab(request):
    try:
        activate_chrome(request)
        pyautogui.hotkey('ctrl', 'w')  
        return JsonResponse({'success': True, 'message': 'Close tab'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)

@csrf_exempt
def next_tab(request):
    try:
        activate_chrome(request)
        pyautogui.hotkey('ctrl', 'tab')  
        return JsonResponse({'success': True, 'message': 'Next tab'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)

@csrf_exempt
def previous_tab(request):
    try:
        activate_chrome(request)
        pyautogui.hotkey('ctrl','shift' ,'tab')  
        return JsonResponse({'success': True, 'message': 'Previous tab'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)


@csrf_exempt
def open_gmail(request):
    activate_chrome(request)
    return open_chrome_with_url('https://mail.google.com/')


@csrf_exempt
def open_youtube(request):
    activate_chrome(request)
    return open_chrome_with_url('https://youtube.com/')
    
@csrf_exempt
def open_chrome_new_tab(request):
    activate_chrome(request)
    return open_chrome_with_url('https://google.com/')

@csrf_exempt
def open_drive(request):
    activate_chrome(request)
    return open_chrome_with_url('https://drive.google.com/')

@csrf_exempt
def open_calendar(request):
    activate_chrome(request)
    return open_chrome_with_url('https://calendar.google.com/')



@csrf_exempt
def scroll_down_chrome(request):
    try:
        activate_chrome(request)
        pyautogui.scroll(-500) 
        
        return JsonResponse({'success': True, 'message': 'Scroll down successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)

@csrf_exempt
def scroll_up_chrome(request):
    try:
        activate_chrome(request)
        pyautogui.scroll(500) 
        
        return JsonResponse({'success': True, 'message': 'Scroll up successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)

