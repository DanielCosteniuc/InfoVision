import RefreshIcon from '@mui/icons-material/Refresh';
import CallIcon from '@mui/icons-material/Call';
import VideocamIcon from '@mui/icons-material/Videocam';
import CallEndIcon from '@mui/icons-material/CallEnd';
import ChatIcon from '@mui/icons-material/Chat';
import CloseIcon from '@mui/icons-material/Close';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import LogoutIcon from '@mui/icons-material/Logout';
import ExitToAppIcon from '@mui/icons-material/ExitToApp'; // Importă iconița
import '../assets/styles/WhatsApp.css';
import React, { useState, useEffect } from 'react';

const WhatsApp = () => {
  const [errorMessage, setErrorMessage] = useState('');
  const [qrCodeImage, setQrCodeImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false); // Stare pentru confirmare închidere

  const [timeLeft, setTimeLeft] = useState(55);
  const [isTimerActive, setIsTimerActive] = useState(false);

  const [isAudioCallActive, setIsAudioCallActive] = useState(false);
  const [isVideoCallActive, setIsVideoCallActive] = useState(false);

  const handleRequest = (url, callback) => {
    setIsLoading(true);
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then(response => {
        setIsLoading(false);
        if (!response.ok) {
          if (response.status === 500) {
            setIsAudioCallActive(false);
            setIsVideoCallActive(false);
          }
          throw new Error(`Server Error: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        if (!data.success) {
          setErrorMessage(data.message);
        } else {
          setErrorMessage('');
          if (callback) callback(data);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setErrorMessage('A apărut o eroare.');
        setIsAudioCallActive(false);
        setIsVideoCallActive(false);
      });
  };

  const handleActivateWhatsApp = () => {
    handleRequest('/shortcuts/whatsapp/activate-whatsapp/');
  };

  const handleCaptureQRCode = () => {
    handleRequest('/shortcuts/whatsapp/capture-qr-whatsapp/', (data) => {
      if (data.qr_code_path) {
        setQrCodeImage(`${data.qr_code_path}?${new Date().getTime()}`);
        setIsConnected(false);
        setTimeLeft(60);
        setIsTimerActive(true);
      } else {
        setIsConnected(true);
      }
    });
  };

  const handleNextChat = () => {
    handleRequest('/shortcuts/whatsapp/next-chat/');
  };

  const handlePreviousChat = () => {
    handleRequest('/shortcuts/whatsapp/previous-chat/');
  };

  const handleOpenChat = () => {
    handleRequest('/shortcuts/whatsapp/open-chat/');
  };

  const handleCloseChat = () => {
    handleRequest('/shortcuts/whatsapp/close-chat/');
  };

  const handleStartAudioCall = () => {
    handleRequest('/shortcuts/whatsapp/start-audio-call/', () => {
      setIsAudioCallActive(true);
    });
  };

  const handleStopAudioCall = () => {
    handleRequest('/shortcuts/whatsapp/close-call/', () => {
      setIsAudioCallActive(false);
    });
  };

  const handleStartVideoCall = () => {
    handleRequest('/shortcuts/whatsapp/start-video-call/', () => {
      setIsVideoCallActive(true);
    });
  };

  const handleStopVideoCall = () => {
    handleRequest('/shortcuts/whatsapp/close-call/', () => {
      setIsVideoCallActive(false);
    });
  };

  const handleLogout = () => {
    handleRequest('/shortcuts/whatsapp/logout-whatsapp/', () => {
      setIsConnected(false);
      setQrCodeImage(null);
    });
  };

  // Funcția pentru a închide WhatsApp după confirmare
  const handleCloseWhatsApp = () => {
    handleRequest('/shortcuts/whatsapp/close-whatsapp/', () => {
      setShowConfirm(false); // Ascundem dialogul de confirmare după închidere
    });
  };

  // Funcția pentru a afișa dialogul de confirmare
  const confirmCloseWhatsApp = () => {
    setShowConfirm(true); // Afișează confirmarea pentru închidere
  };

  useEffect(() => {
    if (isTimerActive && timeLeft > 0) {
      const timerInterval = setInterval(() => {
        setTimeLeft(timeLeft - 1);
      }, 1000);

      return () => clearInterval(timerInterval);
    } else if (timeLeft === 0) {
      setQrCodeImage(null);
      setIsTimerActive(false);
    }
  }, [timeLeft, isTimerActive]);

  return (
    <div className="whatsapp-container">
      <h1 className="title">WhatsApp</h1>
      <div className="button-container">
        <button onClick={handleActivateWhatsApp} className="button activate-whatsapp-button">
          <RefreshIcon className="button-icon" /> Adu în față WhatsApp
        </button>
        <button onClick={handleCaptureQRCode} className="button capture-qr-button">
          {isLoading ? "Se încarcă..." : "Conectare"}
        </button>
        <button onClick={handlePreviousChat} className="button previous-chat-button">
          <ChevronLeftIcon className="button-icon" /> Previous Chat
        </button>
        <button onClick={handleNextChat} className="button next-chat-button">
          <ChevronRightIcon className="button-icon" /> Next Chat
        </button>
        <button onClick={handleOpenChat} className="button open-chat-button">
          <ChatIcon className="button-icon" /> Deschide primul chat
        </button>
        <button onClick={handleCloseChat} className="button close-chat-button">
          <CloseIcon className="button-icon" /> Close Chat
        </button>

        {isAudioCallActive ? (
          <button onClick={handleStopAudioCall} className="button stop-call-button">
            <CallEndIcon className="button-icon" /> Stop Audio Call
          </button>
        ) : (
          <button onClick={handleStartAudioCall} className="button audio-call-button">
            <CallIcon className="button-icon" /> Start Audio Call
          </button>
        )}

        {isVideoCallActive ? (
          <button onClick={handleStopVideoCall} className="button stop-call-button">
            <CallEndIcon className="button-icon" /> Stop Video Call
          </button>
        ) : (
          <button onClick={handleStartVideoCall} className="button video-call-button">
            <VideocamIcon className="button-icon" /> Start Video Call
          </button>
        )}

        <button onClick={handleLogout} className="button logout-button">
          <LogoutIcon className="button-icon" /> Log Out
        </button>

        {/* Adăugăm butonul pentru închiderea WhatsApp cu confirmare */}
        <button onClick={confirmCloseWhatsApp} className="button close-whatsapp-button">
          <ExitToAppIcon className="button-icon" /> Închide WhatsApp
        </button>
      </div>

      {qrCodeImage && !isConnected && (
        <div className="qr-code-container">
          <h2>Scanează acest cod QR pentru a te conecta:</h2>
          <img src={qrCodeImage} alt="QR Code" className="qr-code-image" />
          <p>Timp rămas: {timeLeft} secunde</p>
        </div>
      )}

      {isConnected && (
        <div className="connected-message">
          <h2>Utilizatorul este deja conectat la WhatsApp!</h2>
        </div>
      )}

      {errorMessage && <div className="error-message">{errorMessage}</div>}

      {/* Afișează confirmarea pentru închidere */}
      {showConfirm && (
        <div className="modal">
          <div className="modal-content">
            <p>Ești sigur că vrei să închizi WhatsApp?</p>
            <button onClick={handleCloseWhatsApp} className="confirm-button">Da</button>
            <button onClick={() => setShowConfirm(false)} className="cancel-button">Nu</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default WhatsApp;
