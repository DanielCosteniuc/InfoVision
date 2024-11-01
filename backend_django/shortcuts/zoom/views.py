import base64
import json
import os
import requests
import logging
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
import subprocess
import win32gui

logger = logging.getLogger(__name__)

# Datele de autentificare Zoom
CLIENT_ID = 'JacbvTZjQli0J7Mlm2P8Pw'
CLIENT_SECRET = 's8t5IREvQ3qpbId0KvUjOnov335MOM35'
REDIRECT_URI = 'http://localhost:8000/shortcuts/zoom/oauth/callback'

# Fișier pentru stocarea tokenurilor
TOKEN_FILE_PATH = 'zoom_tokens.json'

# Funcție pentru a salva tokenurile într-un fișier JSON
def save_tokens_to_file(access_token, refresh_token):
    tokens = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    with open(TOKEN_FILE_PATH, 'w') as token_file:
        json.dump(tokens, token_file)

# Funcție pentru a citi tokenurile din fișierul JSON
def read_tokens_from_file():
    if os.path.exists(TOKEN_FILE_PATH):
        with open(TOKEN_FILE_PATH, 'r') as token_file:
            tokens = json.load(token_file)
            return tokens.get('access_token'), tokens.get('refresh_token')
    return None, None

# URL de autorizare OAuth
@csrf_exempt
def zoom_login(request):
    scopes = "team_chat:read:list_contacts"  # Permisiunile necesare
    encoded_scopes = urllib.parse.quote(scopes)  # Codificăm corect permisiunile

    authorization_url = (
        f'https://zoom.us/oauth/authorize?response_type=code&client_id={CLIENT_ID}'
        f'&redirect_uri={REDIRECT_URI}'
        f'&scope={encoded_scopes}'
    )
    logger.info(f"URL de autorizare generat: {authorization_url}")
    return redirect(authorization_url)


@csrf_exempt
def zoom_logout(request):
    if os.path.exists(TOKEN_FILE_PATH):
        os.remove(TOKEN_FILE_PATH)
        logger.info("Tokenurile au fost șterse.")
        return JsonResponse({'success': True, 'message': 'Deconectat cu succes'})
    else:
        return JsonResponse({'success': False, 'message': 'Fișierul de tokenuri nu există'}, status=404)


# Funcție pentru a obține un token de acces de la Zoom
def get_zoom_access_token(authorization_code=None, refresh_token=None):
    url = 'https://zoom.us/oauth/token'
    auth_header = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'grant_type': 'authorization_code' if authorization_code else 'refresh_token',
        'code': authorization_code if authorization_code else None,
        'refresh_token': refresh_token if refresh_token else None,
        'redirect_uri': REDIRECT_URI
    }
    
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        logger.info("Access token successfully retrieved")
        return response.json()
    else:
        logger.error(f"Failed to retrieve access token: {response.status_code} - {response.text}")
        return None

# Callback pentru autorizare OAuth (după ce Zoom redirecționează utilizatorul)
@csrf_exempt
def zoom_oauth_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Lipsește codul de autorizare'}, status=400)

    token_data = get_zoom_access_token(authorization_code=code)
    if token_data:
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']

        # Salvează token-urile într-un fișier sau într-o bază de date
        with open('zoom_tokens.json', 'w') as token_file:
            json.dump({'access_token': access_token, 'refresh_token': refresh_token}, token_file)

        # Redirecționează utilizatorul către componenta frontend după autentificare
        return redirect('http://localhost:3000/shortcuts/zoom')
    else:
        return JsonResponse({'error': 'Eșec la obținerea token-ului de acces'}, status=400)

# Funcție pentru a verifica dacă utilizatorul este autentificat
@csrf_exempt
def check_auth(request):
    access_token, _ = read_tokens_from_file()  # Citim tokenul de acces din fișier
    logger.info(f"Verificare acces token: {access_token}")
    if access_token:
        return JsonResponse({'authenticated': True, 'access_token': access_token})
    else:
        return JsonResponse({'authenticated': False})

# Verifică tokenul și, dacă este expirat, folosește refresh_token
def get_valid_access_token():
    try:
        with open('zoom_tokens.json', 'r') as token_file:
            tokens = json.load(token_file)
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')

        # Verificăm dacă access_token este valid (poți adăuga o verificare de timp sau face o cerere test)
        response = requests.get('https://api.zoom.us/v2/users/me', headers={'Authorization': f'Bearer {access_token}'})
        if response.status_code == 401:  # Dacă access_token a expirat
            token_data = get_zoom_access_token(refresh_token=refresh_token)
            if token_data:
                access_token = token_data['access_token']
                refresh_token = token_data['refresh_token']

                # Actualizează fișierul de tokenuri
                with open('zoom_tokens.json', 'w') as token_file:
                    json.dump({'access_token': access_token, 'refresh_token': refresh_token}, token_file)
        return access_token
    except FileNotFoundError:
        return None

# Funcție pentru a obține lista de contacte de la Zoom
@csrf_exempt
def get_zoom_chat_contacts(request):
    access_token = get_valid_access_token()  # Recuperează tokenul valid

    if not access_token:
        return JsonResponse({'error': 'Utilizatorul nu este autentificat'}, status=401)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    contact_names = []

    # URL pentru a obține lista completă de contacte (inclusiv externe)
    contacts_url = 'https://api.zoom.us/v2/chat/users/me/contacts'
    
    # Facem o cerere pentru a obține lista de contacte
    contacts_response = requests.get(contacts_url, headers=headers)

    # Verificăm dacă cererea a avut succes
    if contacts_response.status_code == 200:
        # Debugging - vezi structura completă a datelor primite
        contacts_data = contacts_response.json()
        print("Răspunsul complet de la API-ul Zoom:", contacts_data)  # Pentru debugging

        # Extragem lista de contacte
        contacts = contacts_data.get('contacts', [])

        # Parcurgem lista de contacte și extragem numele utilizatorilor
        for contact in contacts:
            first_name = contact.get('first_name', '')
            last_name = contact.get('last_name', '')
            user_name = contact.get('email', '')  # Dacă numele lipsește, folosim emailul

            # Preferăm să folosim numele complet dacă există, altfel email-ul
            if first_name or last_name:
                contact_name = f"{first_name} {last_name}".strip()
            else:
                contact_name = user_name

            # Adăugăm numele la lista de contacte dacă nu există deja
            if contact_name and contact_name not in contact_names:
                contact_names.append(contact_name)

    else:
        # Dacă răspunsul API-ului este negativ, afișăm codul de eroare pentru debugging
        print(f"Eroare API Zoom: {contacts_response.status_code} - {contacts_response.text}")
        return JsonResponse({'error': 'Nu s-au putut obține contactele'}, status=contacts_response.status_code)

    # Returnăm lista de nume de contacte extrase
    return JsonResponse({'success': True, 'contact_names': contact_names})





@csrf_exempt
def get_zoom_chat_messages(request):
    access_token = get_valid_access_token()  # Recuperează token-ul valid

    if not access_token:
        return JsonResponse({'error': 'Utilizatorul nu este autentificat'}, status=401)

    # URL-ul pentru obținerea mesajelor de chat
    url = 'https://api.zoom.us/v2/chat/users/me/messages'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Trimitem cererea pentru a obține mesajele
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        messages = response.json()
        return JsonResponse({'success': True, 'messages': messages})
    else:
        logger.error(f"Failed to retrieve messages: {response.status_code} - {response.text}")
        return JsonResponse({'error': f'Eșec la obținerea mesajelor: {response.text}'}, status=response.status_code)



# Funcție pentru deschiderea și maximizarea ferestrei Zoom
def maximize_window_if_not_maximized(hwnd):
    placement = win32gui.GetWindowPlacement(hwnd)
    if placement[1] != win32con.SW_MAXIMIZE:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        logger.info("Fereastra a fost maximizată.")
    else:
        logger.info("Fereastra este deja maximizată.")

def enum_windows_callback(hwnd, results):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        window_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        if "Zoom" in window_text or "ZPContentViewWndClass" in class_name:
            results.append(hwnd)

# Funcție pentru a deschide Zoom
@csrf_exempt
def open_zoom(request):
    try:
        zoom_path = r"C:\Users\Top G\AppData\Roaming\Zoom\bin\Zoom.exe"

        if os.path.exists(zoom_path):
            logger.info(f"Found Zoom executable at {zoom_path}, attempting to open")
            subprocess.Popen(
                [zoom_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            
            # Găsește și maximizează fereastra Zoom
            zoom_windows = []
            win32gui.EnumWindows(enum_windows_callback, zoom_windows)
            if zoom_windows:
                for hwnd in zoom_windows:
                    maximize_window_if_not_maximized(hwnd)
            else:
                logger.warning("Zoom was opened, but no Zoom window was found to maximize.")

            return JsonResponse({'success': True, 'message': 'Zoom opened and maximized successfully.'})
        else:
            logger.error("Zoom executable not found.")
            return JsonResponse({'success': False, 'message': 'Zoom executable not found.'}, status=404)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while opening Zoom: {e.stderr.decode()}")
        return JsonResponse({'success': False, 'message': e.stderr.decode()}, status=500)
    except Exception as e:
        logger.error(f"Exception while opening Zoom: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

'''# Funcție pentru a închide Zoom
@csrf_exempt
def close_zoom(request):
    try:
        zoom_windows = []
        win32gui.EnumWindows(enum_windows_callback, zoom_windows)

        if zoom_windows:
            for hwnd in zoom_windows:
                try:
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    logger.info(f"Zoom window with hwnd {hwnd} has been closed gracefully.")
                except Exception as e:
                    logger.error(f"Failed to close Zoom window with hwnd {hwnd}: {str(e)}")
            return JsonResponse({'success': True, 'message': 'Zoom has been closed gracefully.'})
        else:
            logger.info("No Zoom windows found to close.")
            return JsonResponse({'success': True, 'message': 'No Zoom windows were open.'})

    except Exception as e:
        logger.error(f"Exception while closing Zoom: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)'''
