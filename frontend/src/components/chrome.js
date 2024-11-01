import React, { useState } from 'react';
import '../assets/styles/chrome.css';
import RefreshIcon from '@mui/icons-material/Refresh';
import OpenInBrowserIcon from '@mui/icons-material/OpenInBrowser';
import CloseIcon from '@mui/icons-material/Close';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import EmailIcon from '@mui/icons-material/Email';
import ChatIcon from '@mui/icons-material/Chat';
import DriveIcon from '@mui/icons-material/DriveFileMove';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import NewspaperIcon from '@mui/icons-material/Newspaper';
import CodeIcon from '@mui/icons-material/Code';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import YouTubeIcon from '@mui/icons-material/YouTube';

const Chrome = () => {
  const [errorMessage, setErrorMessage] = useState('');

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

  return (
    <div className="chrome-container">
      <h1 className="title">Google Chrome</h1>
      <div className="button-container">
        <button onClick={() => handleRequest('/shortcuts/chrome/activate-chrome/')} className="button activate-chrome-button">
          <RefreshIcon className="button-icon" /> Adu în față Chrome
        </button>
        <button onClick={() => handleRequest('/shortcuts/chrome/open-chrome-new-tab/')} className="button open-tab-button">
          <OpenInBrowserIcon className="button-icon" /> Deschide Tab Nou
        </button>
        

        <button onClick={() => handleRequest('/shortcuts/chrome/previous-tab/')} className="button previous-tab-button">
          <NavigateBeforeIcon className="button-icon" /> Tab Anterior
        </button>
        <button onClick={() => handleRequest('/shortcuts/chrome/scroll-down-chrome/')} className="button scroll-down-button">
          <ArrowDownwardIcon className="button-icon" /> Scroll Down
        </button>
        
        <button onClick={() => handleRequest('/shortcuts/chrome/close-current-tab/')} className="button close-tab-button">
          <CloseIcon className="button-icon" /> Închide Tabul Curent
        </button>
        <button onClick={() => handleRequest('/shortcuts/chrome/scroll-up-chrome/')} className="button scroll-up-button">
          <ArrowUpwardIcon className="button-icon" /> Scroll Up
        </button>
        <button onClick={() => handleRequest('/shortcuts/chrome/next-tab/')} className="button next-tab-button">
          <NavigateNextIcon className="button-icon" /> Tab Următor
        </button>
        <button onClick={() => handleRequest('/shortcuts/chrome/open-gmail/')} className="button gmail-button">
          <EmailIcon className="button-icon" /> Gmail
        </button>
        
        <button onClick={() => handleRequest('/shortcuts/chrome/open-drive/')} className="button drive-button">
          <DriveIcon className="button-icon" /> Google Drive
        </button>
        <button onClick={() => handleRequest('/shortcuts/chrome/open-calendar/')} className="button calendar-button">
          <CalendarTodayIcon className="button-icon" /> Google Calendar
        </button>
        
        <button onClick={() => handleRequest('/shortcuts/chrome/open-youtube/')} className="button youtube-button">
          <YouTubeIcon className="button-icon" /> YouTube
        </button>
      </div>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
    </div>
  );
};

export default Chrome;
