from django.http import JsonResponse
import socket

def server_info(request):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    port = 8000  # Dacă ai un port specific, altfel îl poți omite
    return JsonResponse({'ip': ip_address, 'port': port})
