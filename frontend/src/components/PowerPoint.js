import React, { useState } from 'react';
import '../assets/styles/PowerPoint.css';
import SaveIcon from '@mui/icons-material/Save';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import RefreshIcon from '@mui/icons-material/Refresh';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import VolumeDownIcon from '@mui/icons-material/VolumeDown';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import CloseIcon from '@mui/icons-material/Close';

const PowerPoint = () => {
  const [showConfirm, setShowConfirm] = useState(false);
  const handleRequest = (url) => {
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  const handleActivatePowerPoint = () => {
    handleRequest('/shortcuts/powerpoint/activate-powerpoint/');
  };

  const handleAddSlide = () => {
    handleRequest('/shortcuts/powerpoint/add-slide/');
  };

  const handleSavePresentation = () => {
    handleRequest('/shortcuts/powerpoint/save-presentation/');
  };

  const handleDeleteSlide = () => {
    const confirmed = window.confirm('Sigur vrei să ștergi acest slide?');
    if (confirmed) {
      handleRequest('/shortcuts/powerpoint/delete-slide/');
    }
  };

  const handleStartPresentation = () => {
    handleRequest('/shortcuts/powerpoint/start-presentation/');
  };

  const handleStopPresentation = () => {
    handleRequest('/shortcuts/powerpoint/stop-presentation/');
  };

  const handleNextSlide = () => {
    handleRequest('/shortcuts/powerpoint/next-slide/');
  };

  const handlePreviousSlide = () => {
    handleRequest('/shortcuts/powerpoint/previous-slide/');
  };

  const handleIncreaseVolume = () => {
    handleRequest('/shortcuts/powerpoint/increase-volume/');
  };

  const handleDecreaseVolume = () => {
    handleRequest('/shortcuts/powerpoint/decrease-volume/');
  };

  const handleGoToFirstSlide = () => {
    handleRequest('/shortcuts/powerpoint/go-to-first-slide/');
  };

  const handleGoToLastSlide = () => {
    handleRequest('/shortcuts/powerpoint/go-to-last-slide/');
  };

  const handleClosePowerPoint = () => {
    handleRequest('/shortcuts/powerpoint/close-powerpoint/');
    setShowConfirm(false);
  };

  const confirmClosePowerPoint = () => {
    setShowConfirm(true);
  }
  
  return (
    <div className="powerpoint-container">
      <h1 className="title">Microsoft PowerPoint</h1>
      <div className="button-container">
        <button onClick={handleActivatePowerPoint} className="button activate-powerpoint-button">
          <RefreshIcon className="button-icon" /> Adu în față PowerPoint
        </button>
        <button onClick={handleSavePresentation} className="button save-presentation-button">
          <SaveIcon className="button-icon" /> Salvare
        </button>
        <button onClick={handleAddSlide} className="button">
          <AddIcon className="button-icon" /> Slide
        </button>
        <button onClick={handleDeleteSlide} className="button">
          <DeleteIcon className="button-icon" /> Slide
        </button>
        <button onClick={handleStartPresentation} className="button">
          <PlayArrowIcon className="button-icon" /> Start
        </button>
        <button onClick={handleStopPresentation} className="button">
          <StopIcon className="button-icon" /> Stop
        </button>
        <button onClick={handlePreviousSlide} className="button">
          <NavigateBeforeIcon className="button-icon" />
        </button>
        <button onClick={handleNextSlide} className="button">
          <NavigateNextIcon className="button-icon" />
        </button>
        <button onClick={handleGoToFirstSlide} className="button">
          <ArrowUpwardIcon className="button-icon" />
        </button>
        <button onClick={handleGoToLastSlide} className="button">
          <ArrowDownwardIcon className="button-icon" />
        </button>
        <button onClick={handleIncreaseVolume} className="button increase-volume-button">
          <VolumeUpIcon className="button-icon" />
        </button>
        <button onClick={handleDecreaseVolume} className="button decrease-volume-button">
          <VolumeDownIcon className="button-icon" />
        </button>
        <button onClick={confirmClosePowerPoint} className="button close-powerpoint-button">
          <CloseIcon className="button-icon" /> Închide PowerPoint
        </button>
      </div>
      {showConfirm && (
        <div className="modal">
          <div className="modal-content">
            <p>Ești sigur că vrei să închizi PowerPoint?</p>
            <button onClick={handleClosePowerPoint} className="confirm-button">Da</button>
            <button onClick={() => setShowConfirm(false)} className="cancel-button">Nu</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PowerPoint;
