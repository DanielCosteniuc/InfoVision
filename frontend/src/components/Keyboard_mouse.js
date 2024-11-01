import React, { useState, useRef, useEffect } from 'react';
import '../assets/styles/Keyboard_mouse.css'; // Importăm fișierul CSS separat
import KeyboardIcon from '@mui/icons-material/Keyboard';
import SwipeIcon from '@mui/icons-material/Swipe';

const Keyboard_mouse = () => {
  const [startTouch, setStartTouch] = useState(null);  // Punctul de început al atingerii
  const [isClick, setIsClick] = useState(true);  // Stare pentru a detecta dacă e un click simplu sau mișcare
  const [inputText, setInputText] = useState('');  // Textul tastat
  const [isKeyboardOpen, setIsKeyboardOpen] = useState(false);  // Stare pentru tastatura deschisă sau închisă
  const sensitivity = 2.7;  // Factorul de sensibilitate pentru mișcarea cursorului
  const inputRef = useRef(null);  // Referință pentru câmpul de input

  let dynamicThrottleLimit = 100; // Inițial throttle-ul este setat la 100ms, dar îl vom ajusta dinamic

  // Funcție de throttling pentru a limita cât de des trimitem date la server
  const throttle = (func, limit) => {
    let lastFunc;
    let lastRan;
    return (...args) => {
      if (!lastRan) {
        func(...args);
        lastRan = Date.now();
      } else {
        clearTimeout(lastFunc);
        lastFunc = setTimeout(() => {
          if ((Date.now() - lastRan) >= limit) {
            func(...args);
            lastRan = Date.now();
          }
        }, limit - (Date.now() - lastRan));
      }
    };
  };

  // Funcție pentru obținerea CSRF token-ului
  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  const csrftoken = getCookie('csrftoken');  // Obține token-ul CSRF din cookie-uri

  // Trimite coordonatele relative către server pentru a muta cursorul
  const sendMouseMove = (deltaX, deltaY) => {
    fetch('/shortcuts/keyboard_mouse/move_mouse/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,  // Adăugăm tokenul CSRF la cerere
      },
      body: JSON.stringify({ action: 'move', x: deltaX, y: deltaY })
    }).catch(error => console.error('Error:', error));
  };
  

  const throttledMouseMove = throttle(sendMouseMove, dynamicThrottleLimit);

  const handleTouchStart = (event) => {
    const touch = event.touches[0];
    setStartTouch({ x: touch.clientX, y: touch.clientY });
    setIsClick(true);  // La începutul atingerii, presupunem că e un click
  };

  const handleTouchMove = (event) => {
    event.preventDefault();
    const touch = event.touches[0];

    if (startTouch) {
      const deltaX = (touch.clientX - startTouch.x) * sensitivity;
      const deltaY = (touch.clientY - startTouch.y) * sensitivity;

      if (Math.abs(deltaX) > 5 || Math.abs(deltaY) > 5) {
        setIsClick(false);  // Dacă delta este semnificativă, e o mișcare, nu un click
      }

      const movementMagnitude = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
      if (movementMagnitude < 10) {
        dynamicThrottleLimit = 1000;
      } else if (movementMagnitude < 50) {
        dynamicThrottleLimit = 850;
      } else {
        dynamicThrottleLimit = 450;
      }

      throttledMouseMove(deltaX, deltaY);

      setStartTouch({ x: touch.clientX, y: touch.clientY });
    }
  };

  const handleTouchEnd = () => {
    if (isClick) {
      handleClick('left');
    }
    setStartTouch(null);
  };

  const handleClick = (button = 'left', double = false) => {
    fetch('/shortcuts/keyboard_mouse/move_mouse/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ action: 'click', button: button, double: double })
    }).catch(error => console.error('Error:', error));
  };

  const sendKeyboardInput = (text) => {
    fetch('/shortcuts/keyboard_mouse/keyboard_input/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ key: text })
    }).catch(error => console.error('Error:', error));
  };

  const toggleKeyboard = () => {
    if (isKeyboardOpen) {
      inputRef.current.blur();  // Înlăturăm focusul de la tastatură
      setIsKeyboardOpen(false);  // Închidem tastatura
    } else {
      inputRef.current.focus();  // Deschidem tastatura
      setIsKeyboardOpen(true);
    }
  };

  const handleInputChange = (event) => {
    const newText = event.target.value;
    if (newText.length < inputText.length) {
      sendKeyboardInput('Backspace');
    } else {
      const lastChar = newText[newText.length - 1];
      if (lastChar === '\n') {
        sendKeyboardInput('Enter');
      } else {
        sendKeyboardInput(lastChar);
      }
    }
    setInputText(newText);
  };

  // Combinație pentru gestionarea `keydown` și `blur`
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Backspace') {
        sendKeyboardInput('Backspace');  // Trimite la server apăsarea pe Backspace
        setInputText((prevText) => prevText.slice(0, -1));  // Șterge ultimul caracter din UI imediat
      }
    };

    const handleBlur = () => {
      setIsKeyboardOpen(false);  // Actualizăm starea pentru a închide butonul
    };

    // Adăugăm evenimentele
    const textarea = inputRef.current;
    document.addEventListener('keydown', handleKeyDown);
    textarea.addEventListener('blur', handleBlur);

    return () => {
      // Curățăm evenimentele la demontarea componentului
      document.removeEventListener('keydown', handleKeyDown);
      textarea.removeEventListener('blur', handleBlur);
    };
  }, []);

  const handleRightClick = (event) => {
    event.preventDefault(); // Previne comportamentul default pentru click dreapta
    handleClick('right');
  };

  const handleDoubleClick = () => {
    handleClick('left', true); // Dublu click pe click stânga
  };

  return (
    <div>
      <div
        className="touchpad-container"
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
        onContextMenu={handleRightClick}  // Captură pentru click dreapta
        onDoubleClick={handleDoubleClick}  // Captură pentru dublu click
      >
        <h2>Touchpad Controller <SwipeIcon /></h2>
        <p>Folosește touchpad-ul pentru a mișca cursorul și apasă pentru a face click.</p>
        <p>Click dreapta prin apăsare lungă sau dublu tap pentru dublu click.</p>
      </div>

      <button 
        onClick={toggleKeyboard} 
        className={`keyboard-toggle ${isKeyboardOpen ? 'keyboard-open' : ''}`}
      >
        {isKeyboardOpen ? 'Închide tastatura' : 'Deschide tastatura'} <KeyboardIcon />
      </button>

      <textarea
        ref={inputRef}
        value={inputText}
        onChange={handleInputChange}
        rows="1"
        className="hidden-textarea"
      />
    </div>
  );
};

export default Keyboard_mouse;
