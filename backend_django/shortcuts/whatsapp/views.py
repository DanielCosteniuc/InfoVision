import os
import time
import pyautogui
import threading
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import pygetwindow as gw
from pywinauto import Application, findwindows
import logging
import win32gui
import win32con
from PIL import ImageGrab, ImageChops

logger = logging.getLogger(__name__)


def log_active_windows():
    try:
        windows = findwindows.find_windows()
        logger.info("Ferestrele active în acest moment:")
        for hwnd in windows:
            try:
                window_text = win32gui.GetWindowText(hwnd)
                if window_text:
                    logger.info(f"HWND: {hwnd}, Titlu: {window_text}")
            except Exception as e:
                logger.error(f"Eroare la obținerea titlului ferestrei {hwnd}: {e}")
    except Exception as e:
        logger.error(f"Eroare la obținerea ferestrelor active: {e}")


def maximize_window_if_not_maximized(hwnd):
    try:
        placement = win32gui.GetWindowPlacement(hwnd)
        if placement[1] != win32con.SW_MAXIMIZE:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            logger.info("Fereastra a fost maximizată.")
        else:
            logger.info("Fereastra este deja maximizată.")
    except Exception as e:
        logger.error(f"Failed to maximize window: {e}")

def bring_whatsapp_to_front():
    try:
        logger.info("Funcția 'bring_whatsapp_to_front' a fost apelată.")
        log_active_windows()  

        windows = findwindows.find_windows(title_re=".*WhatsApp.*")
        if windows:
            hwnd = windows[0]
            logger.info(f"Fereastra WhatsApp găsită, HWND: {hwnd}")
            app = Application().connect(handle=hwnd)
            app_dialog = app.top_window()
            app_dialog.set_focus()  

            maximize_window_if_not_maximized(hwnd)
            return True
        else:
            logger.warning("Fereastra WhatsApp nu a fost găsită.")
            return False
    except Exception as e:
        logger.error(f"Error bringing WhatsApp to front: {e}")
        return False




@csrf_exempt
def open_whatsapp(request):
    try:

        os.startfile("whatsapp:")
        
        time.sleep(2)
        pyautogui.hotkey('ctrl', '1')
        if bring_whatsapp_to_front():
            return JsonResponse({'success': True, 'message': 'WhatsApp Desktop opened and maximized successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'WhatsApp is not open or not found'}, status=500)
    except Exception as e:
        logger.error(f"Failed to open WhatsApp: {e}")
        return JsonResponse({'success': False, 'message': f"Failed to open WhatsApp Desktop: {str(e)}"}, status=500)
    
@csrf_exempt
def activate_whatsapp(request):
    try:

        os.startfile("whatsapp:")
        if bring_whatsapp_to_front():
            return JsonResponse({'success': True, 'message': 'WhatsApp Desktop opened and maximized successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'WhatsApp is not open or not found'}, status=500)
    except Exception as e:
        logger.error(f"Failed to open WhatsApp: {e}")
        return JsonResponse({'success': False, 'message': f"Failed to open WhatsApp Desktop: {str(e)}"}, status=500)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def delete_file_after_delay(file_path, delay):
    def delete_file():
        if os.path.exists(file_path):
            os.remove(file_path)
    timer = threading.Timer(delay, delete_file)
    timer.start()


def is_qr_code_present(image_path):
    image = cv2.imread(image_path)
    qr_code_detector = cv2.QRCodeDetector()

    data, bbox, _ = qr_code_detector.detectAndDecode(image)

    return bool(data)

@csrf_exempt
def capture_qr_whatsapp(request):
    try:
        max_attempts = 2  
        attempt = 0

        qr_code_found = False

        while attempt < max_attempts and not qr_code_found:
            time.sleep(1)  

            screenshot = pyautogui.screenshot()  

            qr_code_path = os.path.join(BASE_DIR, 'static', 'screenshot.png')

            os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)

            screenshot.save(qr_code_path)

            image = Image.open(qr_code_path)
            width, height = image.size

            padding = 200
            padding2 = 300

            cropped_image = image.crop((padding, padding, width - padding, height - padding2))
            cropped_image.save(qr_code_path)

            qr_code_found = is_qr_code_present(qr_code_path)

            if qr_code_found:
                delete_file_after_delay(qr_code_path, 60)  

                relative_qr_code_path = '/static/screenshot.png'
                return JsonResponse({'success': True, 'qr_code_path': relative_qr_code_path})

            else:
                pyautogui.press('enter')  
                time.sleep(2)  
                attempt += 1

        delete_file_after_delay(qr_code_path, 1)  
        if qr_code_found:
            return JsonResponse({'success': True, 'qr_code_path': '/static/screenshot.png'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to detect QR code after multiple attempts.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Failed to capture screenshot: {str(e)}"}, status=500)
    
    
@csrf_exempt
def next_chat(request):
    try:
        if bring_whatsapp_to_front():

            pyautogui.hotkey('ctrl', 'shift', ']')  
            logger.info("S-a trecut la următorul chat.")
            return JsonResponse({'success': True, 'message': 'Switched to next chat'})
        else:
            return JsonResponse({'success': False, 'message': 'WhatsApp is not open or not found'}, status=500)
    except Exception as e:
        logger.error(f"Failed to switch to next chat: {e}")
        return JsonResponse({'success': False, 'message': f"Failed to switch to next chat: {str(e)}"}, status=500)

@csrf_exempt
def previous_chat(request):
    try:
        if bring_whatsapp_to_front():

            pyautogui.hotkey('ctrl', 'shift', '[')  
            logger.info("S-a trecut la chat-ul anterior.")
            return JsonResponse({'success': True, 'message': 'Switched to previous chat'})
        else:
            return JsonResponse({'success': False, 'message': 'WhatsApp is not open or not found'}, status=500)
    except Exception as e:
        logger.error(f"Failed to switch to previous chat: {e}")
        return JsonResponse({'success': False, 'message': f"Failed to switch to previous chat: {str(e)}"}, status=500)
    
    
@csrf_exempt
def open_chat(request):
    """Deschide primul chat cu Ctrl + 1."""
    try:
        pyautogui.hotkey('ctrl', '1')  
        return JsonResponse({'success': True, 'message': 'First chat opened successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Failed to open first chat: {str(e)}"}, status=500)

@csrf_exempt
def close_chat(request):
    """Închide chat-ul curent cu Ctrl + W."""
    try:
        pyautogui.hotkey('ctrl', 'w')  
        return JsonResponse({'success': True, 'message': 'Chat closed successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Failed to close chat: {str(e)}"}, status=500)
    
@csrf_exempt
def start_audio_call(request):
    try:
        audio_image_path = os.path.join(BASE_DIR, 'static', 'images', '1.png')
        logger.info(f"Verificăm existența fișierului: {audio_image_path}")

        if not os.path.exists(audio_image_path):
            logger.error(f"Imaginea audio call nu a fost găsită la calea: {audio_image_path}")
            return JsonResponse({'success': False, 'message': 'Audio call image not found'}, status=500)

        logger.info("Căutăm iconița pentru apel audio pe ecran...")
        audio_button_location = pyautogui.locateCenterOnScreen(audio_image_path, confidence=0.8)

        if audio_button_location:
            logger.info(f"Iconița audio a fost găsită la coordonatele: {audio_button_location}")
            pyautogui.moveTo(audio_button_location)
            pyautogui.click()
            return JsonResponse({'success': True, 'message': 'Audio call started successfully'})
        else:
            logger.warning("Nu s-a găsit iconița pentru apel audio pe ecran.")
            return JsonResponse({'success': False, 'message': 'Audio call button not found on screen'}, status=500)

    except Exception as e:
        logger.error(f"Eroare la inițierea apelului audio: {str(e)}")
        return JsonResponse({'success': False, 'message': f"Failed to start audio call: {str(e)}"}, status=500)


@csrf_exempt
def start_video_call(request):
    try:
        video_image_path = os.path.join(BASE_DIR, 'static', 'images', '2.png')
        logger.info(f"Verificăm existența fișierului: {video_image_path}")

        if not os.path.exists(video_image_path):
            logger.error(f"Imaginea video call nu a fost găsită la calea: {video_image_path}")
            return JsonResponse({'success': False, 'message': 'Video call image not found'}, status=500)

        logger.info("Căutăm iconița pentru apel video pe ecran...")
        video_button_location = pyautogui.locateCenterOnScreen(video_image_path, confidence=0.8)

        if video_button_location:
            logger.info(f"Iconița video a fost găsită la coordonatele: {video_button_location}")
            pyautogui.moveTo(video_button_location)
            pyautogui.click()
            return JsonResponse({'success': True, 'message': 'Video call started successfully'})
        else:
            logger.warning("Nu s-a găsit iconița pentru apel video pe ecran.")
            return JsonResponse({'success': False, 'message': 'Video call button not found on screen'}, status=500)

    except Exception as e:
        logger.error(f"Eroare la inițierea apelului video: {str(e)}")
        return JsonResponse({'success': False, 'message': f"Failed to start video call: {str(e)}"}, status=500)
    
@csrf_exempt
def close_call(request):
    try:
        end_call_image_path = os.path.join(BASE_DIR, 'static', 'images', 'end-call.png')
        logger.info(f"Verificăm existența fișierului: {end_call_image_path}")

        if not os.path.exists(end_call_image_path):
            logger.error(f"Imaginea butonului de închidere apel nu a fost găsită la calea: {end_call_image_path}")
            return JsonResponse({'success': False, 'message': 'End call image not found'}, status=500)

        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        pyautogui.moveTo(center_x, center_y, duration=0.01)  
        pyautogui.hotkey('tab')
        logger.info("Căutăm iconița pentru închiderea apelului pe ecran...")
        end_call_button_location = pyautogui.locateCenterOnScreen(end_call_image_path, confidence=0.8)

        if end_call_button_location:
            logger.info(f"Iconița de închidere a apelului a fost găsită la coordonatele: {end_call_button_location}")
            pyautogui.moveTo(end_call_button_location, duration=0.3)  
            pyautogui.click()
            return JsonResponse({'success': True, 'message': 'Call ended successfully'})
        else:
            logger.warning("Nu s-a găsit iconița pentru închiderea apelului pe ecran.")
            return JsonResponse({'success': False, 'message': 'End call button not found on screen'}, status=500)

    except Exception as e:
        logger.error(f"Eroare la încercarea de a închide apelul: {str(e)}")
        return JsonResponse({'success': False, 'message': f"Failed to end call: {str(e)}"}, status=500)
    
def click_icon(image_name, confidence=0.8, description=""):
    try:
        image_path = os.path.join(BASE_DIR, 'static', 'images', image_name)
        logger.info(f"Checking existence of image: {image_path}")

        if not os.path.exists(image_path):
            logger.error(f"Image not found: {image_path}")
            return JsonResponse({'success': False, 'message': f'{description} image not found'}, status=500)

        logger.info(f"Looking for {description} icon on screen...")
        button_location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)

        if button_location:
            logger.info(f"{description} icon found at coordinates: {button_location}")
            pyautogui.moveTo(button_location)
            pyautogui.click()
            return True
        else:
            logger.warning(f"{description} icon not found on screen.")
            return False
    except Exception as e:
        logger.error(f"Error clicking {description}: {str(e)}")
        return False


@csrf_exempt
def logout_whatsapp(request):
    try:
        # Step 1: Click on the Settings icon
        if not click_icon('settings.png', description="Settings"):
            return JsonResponse({'success': False, 'message': 'Failed to find Settings icon'}, status=500)
        time.sleep(1)

        # Step 2: Click on the Profile icon
        if not click_icon('profile.png', description="Profile"):
            return JsonResponse({'success': False, 'message': 'Failed to find Profile icon'}, status=500)
        time.sleep(1)

        # Step 3: Click on the Logout button
        if not click_icon('log_out.png', description="Logout"):
            return JsonResponse({'success': False, 'message': 'Failed to find Logout button'}, status=500)
        time.sleep(1)

        # Step 4: Confirm Logout by clicking on Yes button
        if not click_icon('da.png', description="Confirm Yes"):
            return JsonResponse({'success': False, 'message': 'Failed to confirm logout'}, status=500)
        time.sleep(10)

        # Step 5: Close WhatsApp window
        if not click_icon('close.png', description="Close"):
            return JsonResponse({'success': False, 'message': 'Failed to close WhatsApp window'}, status=500)

        logger.info("Logout and close successful.")
        return JsonResponse({'success': True, 'message': 'Logout and close successfully'})
    except Exception as e:
        logger.error(f"Failed to logout: {str(e)}")
        return JsonResponse({'success': False, 'message': f"Failed to logout: {str(e)}"}, status=500)
    
@csrf_exempt
def close_whatsapp(request):
    try:
        windows = findwindows.find_windows(title_re=".*WhatsApp.*")
        if windows:
            hwnd = windows[0]
            
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            logger.info("WhatsApp a fost închis.")
            return JsonResponse({'success': True, 'message': 'WhatsApp has been closed successfully'})
        else:
            logger.warning("Fereastra WhatsApp nu a fost găsită.")
            return JsonResponse({'success': False, 'message': 'WhatsApp is not open or not found'}, status=500)
    except Exception as e:
        logger.error(f"Failed to close WhatsApp: {e}")
        return JsonResponse({'success': False, 'message': f"Failed to close WhatsApp: {str(e)}"}, status=500)
