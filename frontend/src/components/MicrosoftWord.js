import React, { useState } from 'react';
import '../assets/styles/MicrosoftWord.css';
import KeyboardDoubleArrowDownIcon from '@mui/icons-material/KeyboardDoubleArrowDown';
import KeyboardDoubleArrowUpIcon from '@mui/icons-material/KeyboardDoubleArrowUp';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import SaveIcon from '@mui/icons-material/Save';
import RefreshIcon from '@mui/icons-material/Refresh';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import ZoomOutIcon from '@mui/icons-material/ZoomOut';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CloseIcon from '@mui/icons-material/Close';

const MicrosoftWord = () => {
  const [errorMessage, setErrorMessage] = useState('');
  const [isReadMode, setIsReadMode] = useState(false); 
  const [showConfirm, setShowConfirm] = useState(false);
  const handleRequest = (url) => {
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then(response => response.json())
    .then(data => {
      if (!data.success) {
        setErrorMessage(data.message);
      } else {
        setErrorMessage('');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      setErrorMessage('A apărut o eroare.');
    });
  };

  const handleGoToEnd = () => {
    handleRequest('/shortcuts/word/go-to-end/');
  };

  const handleGoToStart = () => {
    handleRequest('/shortcuts/word/go-to-start/');
  };

  const handlePageDown = () => {
    handleRequest(isReadMode ? '/shortcuts/word/read-mode-next-page/' : '/shortcuts/word/page-down/');
  };

  const handlePageUp = () => {
    handleRequest(isReadMode ? '/shortcuts/word/read-mode-previous-page/' : '/shortcuts/word/page-up/');
  };

  const handleSaveAs = () => {
    handleRequest('/shortcuts/word/save-as/');
  };

  const handleActivateWord = () => {
    handleRequest('/shortcuts/word/activate-word/');
  };

  const handleZoomIn = () => {
    handleRequest('/shortcuts/word/zoom-in/');
  };

  const handleZoomOut = () => {
    handleRequest('/shortcuts/word/zoom-out/');
  };

  const handleReadModeToggle = () => {
    handleRequest(isReadMode ? '/shortcuts/word/exit-read-mode/' : '/shortcuts/word/read-mode/'); 
    setIsReadMode(!isReadMode); 
  };

  const handleCloseWord = () => {
    handleRequest('/shortcuts/word/close-word/');
    setShowConfirm(false);
  };

  const confirmCloseWord = () => {
    setShowConfirm(true);
  }

  return (
    <div className="microsoft-word-container">
      <h1 className="title">Microsoft Word</h1>
      <div className="button-container">
        <button onClick={handleActivateWord} className="button activate-word-button">
          <RefreshIcon className="button-icon" /> Adu în față Word
        </button>
        
        <button onClick={handleZoomOut} className="button zoom-out-button">
          <ZoomOutIcon className="button-icon" /> Zoom Out
        </button>
        
        <button onClick={handleGoToStart} className="button go-to-start-button">
          <KeyboardDoubleArrowUpIcon className="button-icon" /> Go to Start
        </button>
        
        <button onClick={handleZoomIn} className="button zoom-in-button">
          <ZoomInIcon className="button-icon" /> Zoom In
        </button>
        
        <button onClick={handleGoToEnd} className="button go-to-end-button">
          <KeyboardDoubleArrowDownIcon className="button-icon" /> Go to End
        </button>
        
        <button onClick={handleSaveAs} className="button save-as-button">
          <SaveIcon className="button-icon" /> Salvează
        </button>

        <button onClick={handlePageUp} className="button page-up-button">
          {isReadMode ? <ArrowBackIcon className="button-icon" /> : <ArrowUpwardIcon className="button-icon" />}
          {isReadMode ? 'Previous Page' : 'Page Up'}
        </button>
        
        <button onClick={handlePageDown} className="button page-down-button">
          {isReadMode ? <ArrowForwardIcon className="button-icon" /> : <ArrowDownwardIcon className="button-icon" />}
          {isReadMode ? 'Next Page' : 'Page Down'}
        </button>

        <button onClick={handleReadModeToggle} className="button read-mode-button">
          {isReadMode ? <VisibilityOffIcon className="button-icon" /> : <VisibilityIcon className="button-icon" />}
          {isReadMode ? 'Ieși din Mod Citire' : 'Mod Citire'}
        </button>

        <button onClick={confirmCloseWord} className="button close-word-button">
          <CloseIcon className="button-icon" /> Închide Word
        </button>

      </div>
      
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      {/*Confirmare buton inchidere */}
      {showConfirm && (
        <div className="modal">
          <div className="modal-content">
            <p>Ești sigur că vrei să închizi Microsoft Word?</p>
            <button onClick={handleCloseWord} className="confirm-button">Da</button>
            <button onClick={() => setShowConfirm(false)} className="cancel-button">Nu</button>
          </div>
        </div>
      )}

    </div>
  );
};

export default MicrosoftWord;
