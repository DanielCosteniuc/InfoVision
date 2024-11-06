import React, { useState } from 'react';
import axios from 'axios';
import '../assets/styles/Skype.css'; // Presupunem că stilurile pentru Skype se vor afla aici

// Importăm pictogramele din Material-UI
import VideoCallIcon from '@mui/icons-material/VideoCall';
import PhoneIcon from '@mui/icons-material/Phone';
import MicIcon from '@mui/icons-material/Mic';
import MicOffIcon from '@mui/icons-material/MicOff';
import VideocamIcon from '@mui/icons-material/Videocam';
import VideocamOffIcon from '@mui/icons-material/VideocamOff';
import PhoneDisabledIcon from '@mui/icons-material/PhoneDisabled';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import ChatIcon from '@mui/icons-material/Chat';
import ContactsIcon from '@mui/icons-material/Contacts';
import OpenInBrowserIcon from '@mui/icons-material/OpenInBrowser';
import CloseIcon from '@mui/icons-material/Close';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import PhoneCallbackIcon from '@mui/icons-material/PhoneCallback'; // Icon pentru răspuns la apel
import Keyboard_mouse from './Keyboard_mouse'; // Import Keyboard_mouse component

const Skype = ({ onClose }) => {
  const [errorMessage, setErrorMessage] = useState('');
  const [activeSection, setActiveSection] = useState(null); // Stare pentru secțiunea activă (chats sau contacts)
  const [isMuted, setIsMuted] = useState(false); // Stare pentru microfon (muted/unmuted)
  const [isCameraOn, setIsCameraOn] = useState(false); // Stare pentru cameră (on/off)

  const handleSkypeAction = (endpoint) => {
    axios.post(`/shortcuts/skype/${endpoint}/`)
      .then(response => {
        console.log(response.data.message || 'Action performed successfully');
        setErrorMessage(''); // Resetăm orice eroare
      })
      .catch(error => {
        console.error('There was an error performing the action!', error);
        setErrorMessage('There was an error performing the action.');
      });
  };

  const toggleSection = (section) => {
    if (section === 'chats') {
      // Apelăm endpoint-ul pentru deschiderea chat-urilor
      handleSkypeAction('open-chats');
    }
    if (section === 'contacts') {
      // Apelăm endpoint-ul pentru deschiderea contactelor
      handleSkypeAction('open-contacts');
    }
    // Dacă secțiunea este deja activă, o dezactivăm; altfel, o activăm
    setActiveSection(activeSection === section ? null : section);
  };

  const toggleMute = () => {
    handleSkypeAction('toggle-mute');
    setIsMuted(!isMuted); // Inversăm starea microfonului
  };

  const toggleCamera = () => {
    handleSkypeAction('toggle-camera');
    setIsCameraOn(!isCameraOn); // Inversăm starea camerei
  };

  const confirmCloseSkype = () => {
    setActiveSection(null);
    handleSkypeAction('close-skype');
  };

  const answerCall = () => {
    handleSkypeAction('answer-call'); // Endpoint pentru răspuns la apel
  };

  return (
    <div className="skype-container">
      
      <h1 className="title">Skype</h1>
      <div className="holder-skype">
      <div className="left">
      {/* Prima linie de butoane */}
      <div className="button-row">
        <div className="first-line">
          <button onClick={() => handleSkypeAction('open-skype')} className="button open-skype-button">
            <OpenInBrowserIcon /> Adu în față
          </button>
          <button onClick={confirmCloseSkype} className="button close-skype-button">
            <CloseIcon /> Închide Skype
          </button>
          </div>
          <div className="second-line">
            <button onClick={answerCall} className="button answer-call-button">
              <PhoneCallbackIcon /> Răspunde la apel
            </button>
          
            <button onClick={() => toggleSection('chats')} className={`button chats-button ${activeSection === 'chats' ? 'active' : ''}`}>
              <ChatIcon /> Chats
            </button>
            <button onClick={() => toggleSection('contacts')} className={`button contacts-button ${activeSection === 'contacts' ? 'active' : ''}`}>
              <ContactsIcon /> Contacts
            </button>
            </div>
      </div>
      {/* Afișează butoanele pentru secțiunea Chats */}
      {activeSection === 'chats' && (
        <div className="button-group chats">
          <div className="button-group-chats0">
          <button onClick={() => handleSkypeAction('next-conversation')} className="button next-conversation-button">
            <ArrowForwardIcon /> Următorul chat
          </button>
          <button onClick={() => handleSkypeAction('previous-conversation')} className="button previous-conversation-button">
            <ArrowBackIcon /> Chat-ul anterior
          </button>
         
          </div>

          <div className="button-group-chats1">
          <button onClick={() => handleSkypeAction('start-video-call')} className="button video-call-button">
            <VideoCallIcon />Apel video 
          </button>
          <button onClick={() => handleSkypeAction('start-audio-call')} className="button audio-call-button">
            <PhoneIcon /> Apel audio
          </button>

          </div>
              
          <div className="button-group-chats2">
              <button onClick={toggleCamera} className="button camera-button">
                {isCameraOn ? <VideocamIcon /> : <VideocamOffIcon />} {isCameraOn ? 'Camera' : 'Camera'}
              </button>
              <button onClick={() => handleSkypeAction('hang-up')} className="button hang-up-button">
                <PhoneDisabledIcon /> Închide apelul
              </button>
              <button onClick={toggleMute} className="button mute-button">
                    {isMuted ? <MicOffIcon /> : <MicIcon />} {isMuted ? 'Microfon' : 'Microfon'}
                  </button>
              </div>
        
          
        </div>
      )}

      {/* Afișează butoanele pentru secțiunea Contacts */}
      {activeSection === 'contacts' && (
        <div className="button-group contacts">
          <button onClick={() => handleSkypeAction('navigate-up')} className="button navigate-up-button">
            <ArrowUpwardIcon /> Contactul anterior
          </button>
          
          <button onClick={() => handleSkypeAction('open-contact')} className="button open-contact-button">
            <OpenInBrowserIcon /> Deschide contactul
          </button>
          <button onClick={toggleMute} className="button mute-button">
            {isMuted ? <MicOffIcon /> : <MicIcon />} {isMuted ? 'Microfon' : 'Microfon'}
          </button>
          <button onClick={toggleCamera} className="button camera-button">
            {isCameraOn ? <VideocamIcon /> : <VideocamOffIcon />} {isCameraOn ? 'Camera' : 'Camera'}
          </button>
          <button onClick={() => handleSkypeAction('navigate-down')} className="button navigate-down-button">
            <ArrowDownwardIcon /> Contactul urmator
          </button>
          <button onClick={() => handleSkypeAction('start-video-call')} className="button video-call-button">
            <VideoCallIcon /> Apel video
          </button>
          
          
          <button onClick={() => handleSkypeAction('start-audio-call')} className="button audio-call-button">
            <PhoneIcon /> Apel audio
          </button>
          <button onClick={() => handleSkypeAction('hang-up')} className="button hang-up-button">
            <PhoneDisabledIcon /> Închide apel
          </button>
        </div>
      )}

      {errorMessage && (
        <div className="error-message">
          {errorMessage}
        </div>
      )}

      </div>
      <div className="right">
      <Keyboard_mouse />
      </div>
      </div>
    </div>
  
 
    
    
  );
};

export default Skype;
