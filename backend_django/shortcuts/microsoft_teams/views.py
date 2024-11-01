import os
import time
import pyautogui
import logging
import psutil
import win32gui
import win32con
import pythoncom
import win32com.client
from pywinauto import findwindows
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def bring_teams_to_foreground():
    try:
        # Verifică dacă Microsoft Teams este în execuție
        for process in psutil.process_iter(['name']):
            if process.info['name'] and 'Teams' in process.info['name']:
                # Găsește fereastra Microsoft Teams folosind titlul ferestrei
                windows = findwindows.find_windows(title_re=".*Microsoft Teams.*")
                
                if windows:
                    hwnd = windows[0]
                    
                    # Verifică dacă fereastra este deja în prim-plan
                    if win32gui.GetForegroundWindow() != hwnd:
                        # Aduce Microsoft Teams în prim-plan
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restabilește fereastra dacă este minimizată
                        win32gui.SetForegroundWindow(hwnd)  # Setează fereastra în prim-plan
                        return True  # Echivalent cu faptul că Teams a fost adus în prim-plan
                    
                return False  # Teams este deja în prim-plan
        return False  # Microsoft Teams nu este pornit
    except Exception as e:
        logger.error(f"Error bringing Teams to foreground: {e}")
        return False


@csrf_exempt
def open_microsoft_teams(request):
    try:
        os.startfile("msteams:")
        
        return JsonResponse({'success': True, 'message': 'Microsoft Teams opened successfully'})
    
    except Exception as e:
        logger.error(f"Failed to open Microsoft Teams: {e}")
        return JsonResponse({'success': False, 'message': f"Failed to open Microsoft Teams: {str(e)}"}, status=500)

@csrf_exempt
def close_microsoft_teams(request):
    try:
        windows = findwindows.find_windows(title_re=".*Microsoft Teams.*")
        
        if windows:
            for hwnd in windows:
                window_title = win32gui.GetWindowText(hwnd)
                if "Microsoft Teams" in window_title:
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    logger.info("Microsoft Teams a fost închis.")
                    return JsonResponse({'success': True, 'message': 'Microsoft Teams a fost închis cu succes.'})
            
            logger.warning("Fereastra Microsoft Teams nu a fost găsită.")
            return JsonResponse({'success': False, 'message': 'Microsoft Teams nu este deschis sau nu a fost găsit.'}, status=400)
        
        else:
            logger.warning("Nu s-au găsit ferestre pentru Microsoft Teams.")
            return JsonResponse({'success': False, 'message': 'Microsoft Teams nu este deschis sau nu a fost găsit.'}, status=400)
    
    except Exception as e:
        logger.error(f"Failed to close Microsoft Teams: {e}")
        return JsonResponse({'success': False, 'message': f"Failed to close Microsoft Teams: {str(e)}"}, status=500)


@csrf_exempt
def maximize_active_window(request):  # Adaugă argumentul `request`
    try:
        # Obține handle-ul ferestrei active
        #bring_teams_to_foreground()
        hwnd = win32gui.GetForegroundWindow()
        
        if hwnd:
            # Maximizează fereastra activă
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            return JsonResponse({'success': True, 'message': 'Fereastra activă a fost maximizată.'})
        else:
            return JsonResponse({'success': False, 'message': 'Nu a fost găsită nicio fereastră activă.'}, status=400)
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare la maximizarea ferestrei: {str(e)}"}, status=500)
    
def press_ctrl_and_number(number):
    try:
        if not bring_teams_to_foreground():
            os.startfile("msteams:")
            time.sleep(0.5)
        pyautogui.hotkey('ctrl', str(number))
        return True
    except Exception as e:
        logger.error(f"Failed to press Ctrl + {number}: {e}")
        return False

@csrf_exempt
def navigate_activity(request):
    
    if press_ctrl_and_number(1):
        return JsonResponse({'success': True, 'message': 'Navigated to Activity'})
    return JsonResponse({'success': False, 'message': 'Failed to navigate to Activity'}, status=500)

@csrf_exempt
def navigate_chat(request):
    
    if press_ctrl_and_number(2):
        return JsonResponse({'success': True, 'message': 'Navigated to Chat'})
    return JsonResponse({'success': False, 'message': 'Failed to navigate to Chat'}, status=500)

@csrf_exempt
def navigate_teams(request):
    
    if press_ctrl_and_number(3):
        return JsonResponse({'success': True, 'message': 'Navigated to Teams'})
    return JsonResponse({'success': False, 'message': 'Failed to navigate to Teams'}, status=500)

@csrf_exempt
def navigate_assignments(request):
    
    if press_ctrl_and_number(4):
        return JsonResponse({'success': True, 'message': 'Navigated to Assignments'})
    return JsonResponse({'success': False, 'message': 'Failed to navigate to Assignments'}, status=500)

@csrf_exempt
def navigate_calendar(request):
    
    if press_ctrl_and_number(5):
        return JsonResponse({'success': True, 'message': 'Navigated to Calendar'})
    return JsonResponse({'success': False, 'message': 'Failed to navigate to Calendar'}, status=500)

@csrf_exempt
def navigate_calls(request):
    
    if press_ctrl_and_number(6):
        return JsonResponse({'success': True, 'message': 'Navigated to Calls'})
    return JsonResponse({'success': False, 'message': 'Failed to navigate to Calls'}, status=500)

@csrf_exempt
def navigate_onedrive(request):
    
    if press_ctrl_and_number(7):
        return JsonResponse({'success': True, 'message': 'Navigated to OneDrive'})
    return JsonResponse({'success': False, 'message': 'Failed to navigate to OneDrive'}, status=500)

@csrf_exempt
def arrow_up(request):
    try:
        
        pyautogui.press('up')  # Apasă săgeata în sus
        return JsonResponse({'success': True, 'message': 'Săgeata în sus apăsată'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)

@csrf_exempt
def arrow_down(request):
    try:
        
        pyautogui.press('down')  # Apasă săgeata în jos
        return JsonResponse({'success': True, 'message': 'Săgeata în jos apăsată'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)
    
@csrf_exempt
def start_audio_call(request):
    try:
        if not bring_teams_to_foreground():
            os.startfile("msteams:")
            time.sleep(0.5)
        pyautogui.hotkey('alt', 'shift', 'a')  # Apasă ctrl+Shift+A
        return JsonResponse({'success': True, 'message': 'Apel audio pornit'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)

@csrf_exempt
def start_video_call(request):
    try:
        if not bring_teams_to_foreground():
            os.startfile("msteams:")
            time.sleep(0.5)
        pyautogui.hotkey('alt', 'shift', 'v')  # Apasă Alt+Shift+V
        return JsonResponse({'success': True, 'message': 'Apel video pornit'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)

@csrf_exempt
def end_call(request):
    try:
         
        return JsonResponse({'success': True, 'message': 'Apel încheiat'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)

@csrf_exempt
def mute_microphone(request):
    try:
        
        pyautogui.hotkey('ctrl', 'shift', 'm')  # Apasă ctrl+Shift+M
        return JsonResponse({'success': True, 'message': 'Microfon mutat'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)    
    
@csrf_exempt
def toggle_camera(request):
    try:
        
        pyautogui.hotkey('ctrl', 'shift', 'o')  # Apasă Ctrl + Shift + O
        return JsonResponse({'success': True, 'message': 'Cameră pornită/oprită'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)
    
@csrf_exempt
def increase_volume(request):
    try:
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys(chr(175))  # Codul pentru volum în sus

        return JsonResponse({'success': True, 'message': 'Volum mărit.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def decrease_volume(request):
    try:
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys(chr(174))  

        return JsonResponse({'success': True, 'message': 'Volum micșorat.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
def mute_volume(request):
    try:
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys(chr(173))  

        return JsonResponse({'success': True, 'message': 'Volum oprit.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
@csrf_exempt
def accept_video  (request):
    try:
        
        pyautogui.hotkey('ctrl', 'shift', 'v')  
        return JsonResponse({'success': True, 'message': 'Apel video acceptat'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)

@csrf_exempt
def accept_audio  (request):
    try:
        
        pyautogui.hotkey('ctrl', 'shift', 'a')  
        return JsonResponse({'success': True, 'message': 'Apel audio acceptat'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)
    
@csrf_exempt
def reject_call(request):
    try:
        
        pyautogui.hotkey('ctrl', 'shift', 'd')  
        pyautogui.hotkey('ctrl', 'shift', 'h')
        return JsonResponse({'success': True, 'message': 'Apel respins'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Eroare: {str(e)}"}, status=500)