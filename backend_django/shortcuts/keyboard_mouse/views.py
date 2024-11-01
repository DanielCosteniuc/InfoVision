import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pyautogui

# Mută cursorul relativ față de poziția sa curentă
#pt ecran dublu dar cu eroare
'''def move_mouse_relative(dx, dy):
    try:
        # Obține poziția curentă a cursorului
        current_x, current_y = pyautogui.position()  
        # Calculează noua poziție a cursorului
        new_x = current_x + dx
        new_y = current_y + dy
        # Mută cursorul la noua poziție
        pyautogui.moveTo(new_x, new_y)
        return True
    except Exception as e:
        print(f"Error moving mouse: {e}")
        return False'''

# Mută cursorul relativ față de poziția sa curentă cu limitare pt ecran simplu, mergee bine
def move_mouse_relative(dx, dy):
    try:
        # Obține dimensiunea ecranului
        screen_width, screen_height = pyautogui.size()

        # Obține poziția curentă a cursorului
        current_x, current_y = pyautogui.position()

        # Calculează noua poziție a cursorului
        new_x = current_x + dx
        new_y = current_y + dy

        # Limitează noua poziție astfel încât să nu ajungă în colțurile ecranului
        safe_x = max(5, min(new_x, screen_width - 5))  # Păstrăm cursorul la cel puțin 5px de margini
        safe_y = max(5, min(new_y, screen_height - 5))

        # Mută cursorul la noua poziție sigură
        pyautogui.moveTo(safe_x, safe_y)
        return True
    except Exception as e:
        print(f"Error moving mouse: {e}")
        return False

# Funcția care gestionează click-urile mouse-ului
def click_mouse(button='left', double=False):
    try:
        if double:
            pyautogui.doubleClick()
        else:
            if button == 'left':
                pyautogui.click()
            elif button == 'right':
                pyautogui.rightClick()
        return True
    except Exception as e:
        print(f"Error clicking mouse: {e}")
        return False

# Endpoint care gestionează mișcarea și click-urile mouse-ului
@csrf_exempt
def move_mouse_view(request):
    if request.method == 'POST':
        try:
            # Parsează datele JSON primite
            data = json.loads(request.body)
            action = data.get('action', 'move')  # 'move' sau 'click'

            if action == 'move':
                # Obținem mișcările relative pe axele X și Y
                delta_x = int(data.get('x', 0))  # Mișcarea relativă pe axa X
                delta_y = int(data.get('y', 0))  # Mișcarea relativă pe axa Y

                # Mutăm cursorul relativ față de poziția sa curentă
                if move_mouse_relative(delta_x, delta_y):
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Could not move mouse'})

            elif action == 'click':
                button = data.get('button', 'left')  # 'left' sau 'right'
                double = data.get('double', False)  # Click dublu dacă este True

                # Efectuează click-ul
                if click_mouse(button=button, double=double):
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Could not click mouse'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'invalid request method'}, status=400)




@csrf_exempt
def keyboard_input_view(request):
    if request.method == 'POST':
        try:
            # Parsează datele primite
            data = json.loads(request.body)
            key = data.get('key', '')

            if key:
                # Verificăm dacă tasta este una specială (ex: 'enter', 'delete', 'backspace')
                special_keys = {
                    'Enter': 'enter',
                    #'Backspace': 'backspace',
                    'Delete': 'delete',  # Dacă primești "Delete" de la alte dispozitive
                    'Tab': 'tab',
                    'Shift': 'shift',
                    'Ctrl': 'ctrl',
                    'Alt': 'alt',
                    'Space': 'space'
                }
                
                # Dacă este o tastă specială, folosim denumirea corectă din pyautogui
                if key in special_keys:
                    pyautogui.press(special_keys[key])
                else:
                    # Altfel, simulăm apăsarea tăstei așa cum a fost primită
                    pyautogui.press(key)

                print(f"Key received and pressed: {key}")
            
            return JsonResponse({'status': 'success', 'received_key': key})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'invalid request method'}, status=400)
