import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import MicrosoftTeams from './components/MicrosoftTeams';
import Zoom from './components/Zoom';
import Skype from './components/Skype';
import MicrosoftWord from './components/MicrosoftWord';
import MicrosoftExcel from './components/MicrosoftExcel';
import PowerPoint from './components/PowerPoint';
import PDFReader from './components/PDF';
import Chrome from './components/chrome';
import WhatsApp from './components/WhatsApp';
import FileExplorer from './components/FileExplorer';
import Keyboard_mouse from './components/Keyboard_mouse';
import './App.css';

const App = () => {
  const [isFullscreen, setIsFullscreen] = useState(false);

  const toggleFullscreen = () => {
    if (!isFullscreen) {
      // Request full screen
      if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen().catch((err) => {
          console.error("Failed to enable full screen mode:", err);
        });
      } else if (document.documentElement.mozRequestFullScreen) {
        document.documentElement.mozRequestFullScreen();
      } else if (document.documentElement.webkitRequestFullscreen) {
        document.documentElement.webkitRequestFullscreen();
      } else if (document.documentElement.msRequestFullscreen) {
        document.documentElement.msRequestFullscreen();
      }
    } else {
      // Exit full screen if currently in full screen mode
      if (document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement || document.msFullscreenElement) {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        }
      }
    }
    setIsFullscreen(!isFullscreen);
  };

  return (
    <Router>
      <div className={`App ${isFullscreen ? 'fullscreen' : ''}`}>
        <Sidebar />
        <div className="content">
          <button onClick={toggleFullscreen} className="fullscreen-toggle">
            {isFullscreen ? 'Exit Full Screen' : 'Full Screen'}
          </button>
          <Routes>
            {/* Default redirect to File Explorer */}
            <Route path="/" element={<Navigate to="/shortcuts/fileexplorer" />} />
            <Route path="/shortcuts/fileexplorer" element={<FileExplorer />} />
            <Route path="/shortcuts/teams" element={<MicrosoftTeams />} />
            <Route path="/shortcuts/zoom" element={<Zoom />} />
            <Route path="/shortcuts/skype" element={<Skype />} />
            <Route path="/shortcuts/word" element={<MicrosoftWord />} />
            <Route path="/shortcuts/excel" element={<MicrosoftExcel />} />
            <Route path="/shortcuts/powerpoint" element={<PowerPoint />} />
            <Route path="/shortcuts/pdf" element={<PDFReader />} />
            <Route path="/shortcuts/chrome" element={<Chrome />} />
            <Route path="/shortcuts/whatsapp" element={<WhatsApp />} />
            <Route path="/shortcuts/keyboard_mouse" element={<Keyboard_mouse />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
