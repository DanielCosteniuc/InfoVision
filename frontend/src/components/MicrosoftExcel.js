import React, { useState } from 'react';
import '../assets/styles/MicrosoftExcel.css';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';   // Iconiță pentru scroll up
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward'; // Iconiță pentru scroll down
import ArrowBackIcon from '@mui/icons-material/ArrowBack';         // Iconiță pentru scroll stânga
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos'; // Iconiță pentru scroll dreapta
import DeleteIcon from '@mui/icons-material/Delete';
import SaveIcon from '@mui/icons-material/Save';
import RefreshIcon from '@mui/icons-material/Refresh';
import AddIcon from '@mui/icons-material/Add';
import CloseIcon from '@mui/icons-material/Close';

const MicrosoftExcel = () => {
  const [errorMessage, setErrorMessage] = useState('');
  const [showConfirmation, setShowConfirmation] = useState(false);
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

  const handleActivateExcel = () => {
    handleRequest('/shortcuts/excel/activate-excel/');
  };

  const handleSaveExcel = () => {
    handleRequest('/shortcuts/excel/save-excel/');
  };

  const handleAddSheet = () => {
    handleRequest('/shortcuts/excel/add-sheet/');
  };

  const handleNextSheet = () => {
    handleRequest('/shortcuts/excel/next-sheet/');
  };

  const handlePrevSheet = () => {
    handleRequest('/shortcuts/excel/prev-sheet/');
  };

  const handleDeleteSheet = () => {
    handleRequest('/shortcuts/excel/delete-active-sheet/');
    setShowConfirmation(false);
  };

  const handleCloseExcel = () => {
    handleRequest('/shortcuts/excel/close-excel/');
    setShowConfirm(false);
  };

  const handleScrollUp = () => {
    handleRequest('/shortcuts/excel/scroll-up/');
  };

  const handleScrollDown = () => {
    handleRequest('/shortcuts/excel/scroll-down/');
  };

  const handleScrollLeft = () => {
    handleRequest('/shortcuts/excel/scroll-left/');  // Derulează la stânga
  };

  const handleScrollRight = () => {
    handleRequest('/shortcuts/excel/scroll-right/');  // Derulează la dreapta
  };

  const confirmCloseExcel = () => {
    setShowConfirm(true);
  }

  return (
    <div className="microsoft-excel-container">
      <h1 className="title">Microsoft Excel</h1>
      <div className="button-container">
        <button onClick={handleActivateExcel} className="button activate-excel-button">
          <RefreshIcon className="button-icon" /> Adu în față Excel
        </button>
        <button onClick={handlePrevSheet} className="button prev-sheet-button">
          <ArrowBackIcon className="button-icon" /> Sheet
        </button>
        <button onClick={handleNextSheet} className="button next-sheet-button">
          <ArrowForwardIcon className="button-icon" /> Sheet
        </button>
        <button onClick={handleAddSheet} className="button add-sheet-button">
          <AddIcon className="button-icon" /> Adaugă Sheet
        </button>
        <button onClick={() => setShowConfirmation(true)} className="button delete-sheet-button">
          <DeleteIcon className="button-icon" /> Șterge Sheet
        </button>
        <button onClick={handleSaveExcel} className="button save-excel-button">
          <SaveIcon className="button-icon" /> Salvează Excel
        </button>

        {/* Butoane pentru scroll up și scroll down */}
        <button onClick={handleScrollUp} className="button scroll-up-button">
          <ArrowUpwardIcon className="button-icon" /> Mută în sus
        </button>
        <button onClick={handleScrollDown} className="button scroll-down-button">
          <ArrowDownwardIcon className="button-icon" /> Mută în jos
        </button>

        {/* Butoane pentru scroll stânga și dreapta */}
        <button onClick={handleScrollLeft} className="button scroll-left-button">
          <ArrowBackIcon className="button-icon" /> Mută la stânga
        </button>
        <button onClick={handleScrollRight} className="button scroll-right-button">
          <ArrowForwardIosIcon className="button-icon" /> Mută la dreapta
        </button>

        <button onClick={confirmCloseExcel} className="button close-excel-button">
          <CloseIcon className="button-icon" /> Închide Excel
        </button>
      </div>

      {showConfirmation && (
        <div className="confirmation-dialog">
          <p>Sigur vrei să elimini sheetul activ?</p>
          <button onClick={handleDeleteSheet} className="confirm-button">Confirmă</button>
          <button onClick={() => setShowConfirmation(false)} className="cancel-button">Anulează</button>
        </div>
      )}
      {errorMessage && <div className="error-message">{errorMessage}</div>}

      {/*Confirmare buton inchidere */}
      {showConfirm && (
        <div className="modal">
          <div className="modal-content">
            <p>Ești sigur că vrei să închizi Microsoft Excel?</p>
            <button onClick={handleCloseExcel} className="confirm-button">Da</button>
            <button onClick={() => setShowConfirm(false)} className="cancel-button">Nu</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default MicrosoftExcel;
