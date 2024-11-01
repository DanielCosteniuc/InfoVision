import React, { useState } from 'react';
import axios from 'axios';
import '../assets/styles/MicrosoftTeams.css';
import NotificationsIcon from '@mui/icons-material/Notifications'; // Icon pentru Activity
import ChatIcon from '@mui/icons-material/Chat'; // Icon pentru Chat
import GroupIcon from '@mui/icons-material/Group'; // Icon pentru Teams
import AssignmentIcon from '@mui/icons-material/Assignment'; // Icon pentru Assignments
import CalendarTodayIcon from '@mui/icons-material/CalendarToday'; // Icon pentru Calendar
import PhoneIcon from '@mui/icons-material/Phone'; // Icon pentru Calls
import CloudIcon from '@mui/icons-material/Cloud'; // Icon pentru OneDrive
import CloseIcon from '@mui/icons-material/Close'; // Icon pentru Închidere Teams
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward'; // Icon pentru Sageata in sus
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward'; // Icon pentru Sageata in jos
import VideocamIcon from '@mui/icons-material/Videocam'; // Icon pentru Video Call
import CallEndIcon from '@mui/icons-material/CallEnd'; // Icon pentru End Call
import MicIcon from '@mui/icons-material/Mic'; // Icon pentru Microfon
import MicOffIcon from '@mui/icons-material/MicOff'; // Icon pentru Microfon Mutat
import VideocamOffIcon from '@mui/icons-material/VideocamOff'; // Icon pentru Camera Oprită
import VideoCallIcon from '@mui/icons-material/VideoCall';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import VolumeDownIcon from '@mui/icons-material/VolumeDown';
import VolumeOff from '@mui/icons-material/VolumeOff';
import OpenInBrowserIcon from '@mui/icons-material/OpenInBrowser'; // Iconiță pentru "Adu în față Teams"
import FullscreenIcon from '@mui/icons-material/Fullscreen'; // Iconiță pentru "Maximizează Fereastra"


const MicrosoftTeamsButton = () => {
  const [errorMessage, setErrorMessage] = useState('');
  const [isMicMuted, setIsMicMuted] = useState(false); // Starea pentru mutare microfon
  const [isCameraOn, setIsCameraOn] = useState(true); // Starea pentru pornirea camerei
  const [showConfirm, setShowConfirm] = useState(false); // Starea pentru confirmarea închiderii Teams

  const handleNavigation = (endpoint) => {
    axios.post(endpoint)
      .catch(() => {
        setErrorMessage('A apărut o eroare.');
      });
  };

  const toggleMute = () => {
    setIsMicMuted(!isMicMuted); // Inversează starea microfonului
    handleNavigation('/shortcuts/teams/mute-microphone/');
  };

  const toggleCamera = () => {
    setIsCameraOn(!isCameraOn); // Inversează starea camerei
    handleNavigation('/shortcuts/teams/toggle-camera/');
  };

  const handleCloseTeams = () => {
    handleNavigation('/shortcuts/teams/close-teams/');
    setShowConfirm(false); // Ascunde dialogul după confirmare
  };

  const confirmCloseTeams = () => {
    setShowConfirm(true); // Afișează dialogul de confirmare
  };

  const handleMaximizeWindow = () => {
    handleNavigation('/shortcuts/teams/maximize-active-window/'); 
  };

  return (
    <div className="teams-container">
      <h2 className="title">Microsoft Teams</h2>
      <div className="button-container">
        {/* Butoane principale pentru navigare */}
        <button className="button activity-button" onClick={() => handleNavigation('/shortcuts/teams/activity/')}>
          <NotificationsIcon />
        </button>

        <button className="button chat-button" onClick={() => handleNavigation('/shortcuts/teams/chat/')}>
          <ChatIcon />
        </button>

        <button className="button teams-button" onClick={() => handleNavigation('/shortcuts/teams/teams/')}>
          <GroupIcon />
        </button>

        <button className="button assignments-button" onClick={() => handleNavigation('/shortcuts/teams/assignments/')}>
          <AssignmentIcon />
        </button>

        <button className="button calendar-button" onClick={() => handleNavigation('/shortcuts/teams/calendar/')}>
          <CalendarTodayIcon />
        </button>

        <button className="button calls-button" onClick={() => handleNavigation('/shortcuts/teams/calls/')}>
          <PhoneIcon />
        </button>

        <button className="button onedrive-button" onClick={() => handleNavigation('/shortcuts/teams/onedrive/')}>
          <CloudIcon />
        </button>
      </div>

      {/* Container pentru Chat și Volum în aceeași linie */}
      <div className="chat-and-volume-container">
        {/* Container Chat */}
        <div className="chat-container">
          <h3 className="chat-title">Chat</h3>
          <div className="chat-button-container">
            <button className="button arrow-up-button" onClick={() => handleNavigation('/shortcuts/teams/arrow-up/')}>
              <ArrowUpwardIcon />
            </button>
            <button className="button start-audio-call-button" onClick={() => handleNavigation('/shortcuts/teams/start-audio-call/')}>
              <PhoneIcon />
            </button>
            <button className="button start-video-call-button" onClick={() => handleNavigation('/shortcuts/teams/start-video-call/')}>
              <VideoCallIcon />
            </button>

            <button className="button arrow-down-button" onClick={() => handleNavigation('/shortcuts/teams/arrow-down/')}>
              <ArrowDownwardIcon />
            </button>
            <button className="button toggle-camera-button" onClick={toggleCamera}>
              {isCameraOn ? <VideocamIcon /> : <VideocamOffIcon />}
            </button>

            <button className="button mute-button" onClick={toggleMute}>
              {isMicMuted ? <MicOffIcon /> : <MicIcon />}
            </button>
            <button className="button end-call-button" onClick={() => handleNavigation('/shortcuts/teams/end-call/')}>
              <CallEndIcon />
            </button>
          </div>
        </div>

        {/* Container Volum */}
        <div className="volume-container">
          <h3 className="volume-title">Volum</h3>
          <div className="volume-button-container">
            <button className="button volume-down-button" onClick={() => handleNavigation('/shortcuts/teams/volume-down/')}>
              <VolumeDownIcon /> {/* Volum Jos */}
            </button>
            <button className="button volume-up-button" onClick={() => handleNavigation('/shortcuts/teams/volume-up/')}>
              <VolumeUpIcon /> {/* Volum Sus */}
            </button>
            <button className="button volume-mute-button" onClick={() => handleNavigation('/shortcuts/teams/volume-mute/')}>
              <VolumeOff /> {/* Volum Oprit */}
            </button>
          </div>
        </div>

        {/* Container Primire Apel */}
        <div className="call-controls-container">
          <h3 className="call-title">Primire apel</h3>
          <div className="call-button-container">
            <button className="button accept-audio-call-button" onClick={() => handleNavigation('/shortcuts/teams/accept-audio-call/')}>
              <PhoneIcon /> {/* Acceptă Apel Audio */}
            </button>
            <button className="button accept-video-call-button" onClick={() => handleNavigation('/shortcuts/teams/accept-video-call/')}>
              <VideocamIcon /> {/* Acceptă Apel Video */}
            </button>

            <button className="button toggle-mic-button" onClick={toggleMute}>
              {isMicMuted ? <MicOffIcon /> : <MicIcon />} {/* Microfon Mut/Activ */}
            </button>

            <button className="button toggle-camera-button" onClick={toggleCamera}>
              {isCameraOn ? <VideocamIcon /> : <VideocamOffIcon />} {/* Deschide/Inchide Camera */}
            </button>

            <button className="button end-call-button" onClick={() => handleNavigation('/shortcuts/teams/end-call-reject/')}>
              <CallEndIcon /> {/* Închide Apel */}
            </button>
          </div>
        </div>
      </div>

      {/* Ultimul rând pentru butoanele Teams */}
      <div className="final-button-row">
        <button className="button open-teams-button" onClick={() => handleNavigation('/shortcuts/teams/open-teams/')}>
          <OpenInBrowserIcon/>Adu în față Teams
        </button>

        <button className="button maximize-window-button" onClick={handleMaximizeWindow}>
          <FullscreenIcon/>Maximizează Fereastra
        </button>

        <button className="button close-teams-button" onClick={confirmCloseTeams}>
          <CloseIcon /> Închide Teams
        </button>
      </div>

      {/* Mesaj de eroare */}
      {errorMessage && <div className="error-message">{errorMessage}</div>}

      {/*Confirmare buton închidere Teams */}
      {showConfirm && (
        <div className="modal">
          <div className="modal-content">
            <p>Ești sigur că vrei să închizi Microsoft Teams?</p>
            <button onClick={handleCloseTeams} className="confirm-button">Da</button>
            <button onClick={() => setShowConfirm(false)} className="cancel-button">Nu</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default MicrosoftTeamsButton;
