import os
import pyautogui
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import psutil

@csrf_exempt
def open_skype(request):
    try:
        os.startfile("skype:")
        return JsonResponse({'success': True, 'message': 'Skype opened successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to open Skype: {str(e)}'}, status=500)




@csrf_exempt
def close_skype(request):
    try:
        for process in psutil.process_iter(['name']):
            if process.info['name'] and 'skype' in process.info['name'].lower():
                process.terminate()  
                process.wait(timeout=1) 
        
        return JsonResponse({'success': True, 'message': 'Skype closed successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to close Skype: {str(e)}'}, status=500)


@csrf_exempt
def open_chats(request):
    try:
        pyautogui.hotkey('alt', '1')
        return JsonResponse({'success': True, 'message': 'Opened chats successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to open chats: {str(e)}'}, status=500)

@csrf_exempt
def open_contacts(request):
    try:
        pyautogui.hotkey('alt', '2')
        time.sleep(0.1)
        pyautogui.hotkey('tab')
        time.sleep(0.1)
        pyautogui.hotkey('tab')
        time.sleep(0.1)
        pyautogui.hotkey('tab')
        
        
        return JsonResponse({'success': True, 'message': 'Opened contacts successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to open contacts: {str(e)}'}, status=500)

@csrf_exempt
def next_conversation(request):
    try:
        pyautogui.hotkey('ctrl', 'tab')
        return JsonResponse({'success': True, 'message': 'Moved to next conversation'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to move to next conversation: {str(e)}'}, status=500)

@csrf_exempt
def previous_conversation(request):
    try:
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        return JsonResponse({'success': True, 'message': 'Moved to previous conversation'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to move to previous conversation: {str(e)}'}, status=500)

@csrf_exempt
def start_video_call(request):
    try:
        pyautogui.hotkey('ctrl', 'shift', 'k')
        return JsonResponse({'success': True, 'message': 'Started video call'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to start video call: {str(e)}'}, status=500)

@csrf_exempt
def start_audio_call(request):
    try:
        pyautogui.hotkey('ctrl', 'shift', 'p')
        return JsonResponse({'success': True, 'message': 'Started audio call'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to start audio call: {str(e)}'}, status=500)

@csrf_exempt
def toggle_mute(request):
    try:
        pyautogui.hotkey('ctrl', 'm')
        return JsonResponse({'success': True, 'message': 'Toggled mute'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to toggle mute: {str(e)}'}, status=500)

@csrf_exempt
def toggle_camera(request):
    try:
        pyautogui.hotkey('ctrl', 'shift', 'k')
        return JsonResponse({'success': True, 'message': 'Toggled camera'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to toggle camera: {str(e)}'}, status=500)

@csrf_exempt
def add_people_to_call(request):
    try:
        pyautogui.hotkey('ctrl', 'shift', 'a')
        return JsonResponse({'success': True, 'message': 'Added people to call'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to add people to call: {str(e)}'}, status=500)
    
@csrf_exempt
def navigate_up(request):
    try:
        pyautogui.press('up')
        return JsonResponse({'success': True, 'message': 'Navigated up successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to navigate up: {str(e)}'}, status=500)

@csrf_exempt
def navigate_down(request):
    try:
        pyautogui.press('down')
        return JsonResponse({'success': True, 'message': 'Navigated down successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to navigate down: {str(e)}'}, status=500)

@csrf_exempt
def hang_up(request):
    try:
        pyautogui.hotkey('ctrl', 'shift', 'h')
        return JsonResponse({'success': True, 'message': 'Call hung up successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to hang up: {str(e)}'}, status=500)

@csrf_exempt
def answer_call(request):
    try:
        pyautogui.hotkey('ctrl', 'shift', 'p')
        return JsonResponse({'success': True, 'message': 'Call answered successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to answer call: {str(e)}'}, status=500)
    
@csrf_exempt
def open_contact(request):
    try:
        pyautogui.hotkey('enter')
        return JsonResponse({'success': True, 'message': 'Call answered successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to answer call: {str(e)}'}, status=500)
