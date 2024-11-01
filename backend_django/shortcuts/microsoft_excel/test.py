import win32gui
import logging

# Configurare logare
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Callback pentru enumera ferontele
def enum_windows_callback(hwnd, results):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        window_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        results.append((hwnd, window_text, class_name))

# Funcția pentru logarea ferontelelor deschise
def log_open_windows():
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)

    if not windows:
        logging.debug('Nu s-au găsit ferontele deschise.')
    else:
        logging.debug('Feronsle deschise:')
        for hwnd, window_text, class_name in windows:
            logging.debug(f'Handle: {hwnd}, Titlu: "{window_text}", Clasa: "{class_name}"')

# Testare funcționalitate
if __name__ == "__main__":
    log_open_windows()