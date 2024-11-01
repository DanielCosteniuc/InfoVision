import os
import subprocess
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
from django.conf import settings
from pathlib import Path

# Lista de restrictii
RESTRICTED_PATHS = [
    r'C:\Windows',
    r'C:\$Recycle.Bin',
    r'C:\Program Files',
    r'C:\$WinREAgent',
    #alte restrictii aici
]

def is_restricted_path(path):

    path = os.path.normpath(path)
    for restricted_path in RESTRICTED_PATHS:
        if path.startswith(os.path.normpath(restricted_path)):
            return True
    return False

@csrf_exempt
def list_partitions(request):
    partitions = [f"{chr(drive)}:\\" for drive in range(65, 91) if os.path.exists(f"{chr(drive)}:\\")]
    return JsonResponse({'partitions': partitions})

@csrf_exempt
def list_files(request):
    path = request.GET.get('path', '')
    if not os.path.isabs(path) or not os.path.exists(path):
        return JsonResponse({'error': 'Path not found or is not an absolute path'}, status=404)

    if is_restricted_path(path):
        return JsonResponse({'error': 'Access to this path is restricted'}, status=403)

    files = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        files.append({
            'name': item,
            'is_dir': os.path.isdir(item_path)
        })

    return JsonResponse({'files': files}, status=200)

@csrf_exempt
def download_file(request):
    file_path = request.GET.get('filePath', '')

    if not file_path:
        return JsonResponse({'error': 'No file path provided'}, status=400)

    file_path = urllib.parse.unquote(file_path)
    file_path = os.path.normpath(file_path)

    if not os.path.isabs(file_path) or is_restricted_path(file_path):
        return JsonResponse({'error': 'Invalid or restricted file path'}, status=400)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'File not found or is not a file'}, status=404)
    
# Lista extensiilor permise
ALLOWED_EXTENSIONS = ['.doc', '.docx', '.ppt', '.pptx', '.pdf', '.xls', '.xlsx']

def is_allowed_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension.lower() in ALLOWED_EXTENSIONS

@csrf_exempt
def server_action(request):
    file_path = request.GET.get('filePath', '')

    if not file_path:
        return JsonResponse({'success': False, 'message': 'No file path provided.'}, status=400)

    file_path = os.path.normpath(file_path)

    if is_restricted_path(file_path):
        return JsonResponse({'success': False, 'message': 'Access to this path is restricted.'}, status=403)

    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            subprocess.run(['explorer', file_path], shell=True)
            return JsonResponse({'success': True}, status=200)
        elif is_allowed_extension(file_path):
            subprocess.run(['start', '', file_path], shell=True)
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'File type not allowed.'}, status=403)
    else:
        return JsonResponse({'success': False, 'message': 'File not found.'}, status=404)
