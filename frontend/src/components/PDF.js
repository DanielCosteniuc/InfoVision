import React, { useState } from 'react';
import '../assets/styles/PDF.css';
import RefreshIcon from '@mui/icons-material/Refresh';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import ZoomOutIcon from '@mui/icons-material/ZoomOut';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import ChromeReaderModeIcon from '@mui/icons-material/ChromeReaderMode';
import PrintIcon from '@mui/icons-material/Print';
import CloseIcon from '@mui/icons-material/Close'; // Importă iconița de închidere

const PDF = () => {
  const [errorMessage, setErrorMessage] = useState('');
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

  const handleActivatePDF = () => {
    handleRequest('/shortcuts/pdf/activate-acrobat/');
  };

  const handleZoomIn = () => {
    handleRequest('/shortcuts/pdf/zoom-in-pdf/');
  };

  const handleZoomOut = () => {
    handleRequest('/shortcuts/pdf/zoom-out-pdf/');
  };

  const handleNextPage = () => {
    handleRequest('/shortcuts/pdf/next-page-pdf/');
  };

  const handlePreviousPage = () => {
    handleRequest('/shortcuts/pdf/previous-page-pdf/');
  };

  const handleReadMode = () => {
    handleRequest('/shortcuts/pdf/read-mode-pdf/');
  };

  const handlePrint = () => {
    handleRequest('/shortcuts/pdf/print-pdf/');
  };

  const handleClosePDF = () => {
    handleRequest('/shortcuts/pdf/close-acrobat/');
    setShowConfirm(false); // Închide fereastra modală după confirmare
  };

  const confirmClosePDF = () => {
    setShowConfirm(true); // Afișează fereastra modală pentru confirmare
  };

  return (
    <div className="pdf-container">
      <h1 className="title">Adobe Acrobat</h1>
      <div className="button-container">
        <button onClick={handleActivatePDF} className="button activate-pdf-button">
          <RefreshIcon className="button-icon" /> Adu în față Acrobat
        </button>
        <button onClick={handleZoomIn} className="button zoom-in-button">
          <ZoomInIcon className="button-icon" /> Zoom In
        </button>
        <button onClick={handleZoomOut} className="button zoom-out-button">
          <ZoomOutIcon className="button-icon" /> Zoom Out
        </button>
        <button onClick={handleNextPage} className="button next-page-button">
          <NavigateNextIcon className="button-icon" /> Pagina următoare
        </button>
        <button onClick={handlePreviousPage} className="button previous-page-button">
          <NavigateBeforeIcon className="button-icon" /> Pagina anterioară
        </button>
        <button onClick={handleReadMode} className="button read-mode-button">
          <ChromeReaderModeIcon className="button-icon" /> Modul de citire
        </button>
        <button onClick={handlePrint} className="button print-button">
          <PrintIcon className="button-icon" /> Printare
        </button>
        <button onClick={confirmClosePDF} className="button close-pdf-button">
          <CloseIcon className="button-icon" /> Închide Acrobat
        </button>
      </div>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      
      {showConfirm && (
        <div className="modal">
          <div className="modal-content">
            <p>Ești sigur că vrei să închizi Adobe Acrobat?</p>
            <button onClick={handleClosePDF} className="confirm-button">Da</button>
            <button onClick={() => setShowConfirm(false)} className="cancel-button">Nu</button>
          </div>
        </div>
      )}
      
    </div>
  );
};

export default PDF;
