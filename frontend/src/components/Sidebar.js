import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

import TeamsIcon from '../assets/icons_sidebar/business.png';
import WordIcon from '../assets/icons_sidebar/word.png';
import ExcelIcon from '../assets/icons_sidebar/excel.png';
import PowerPointIcon from '../assets/icons_sidebar/office.png';
import ChromeIcon from '../assets/icons_sidebar/chrome.png';
import PdfIcon from '../assets/icons_sidebar/acrobat.png';
import FileExplorerIcon from '../assets/icons_sidebar/folder.png';
import ZoomIcon from '../assets/icons_sidebar/zoom.png';
import WhatsappIcon from '../assets/icons_sidebar/whatsapp.png';
import SkypeIcon from '../assets/icons_sidebar/skype.png';
import LogoIcon from '../assets/logo/logo3.png';
import KeyboardIcon from '@mui/icons-material/Keyboard';

import '../assets/styles/Sidebar.css';

const Sidebar = () => {
  const [backendUrl, setBackendUrl] = useState('');
  const [serverInfo, setServerInfo] = useState({ ip: '', port: '' });

  useEffect(() => {
    fetchBackendUrl();
  }, []);

  const fetchBackendUrl = async () => {
    try {
      const response = await axios.get('/api/server-info');
      const { ip, port } = response.data;
      const url = `http://${ip}:${port}`;
      setBackendUrl(url);
      setServerInfo({ ip, port });
    } catch (error) {
      console.error('There was an error fetching the backend URL!', error);
    }
  };

  // Funcții pentru deschiderea aplicațiilor locale
  const openTeams = () => {
    axios.post(`${backendUrl}/shortcuts/teams/open-teams/`)
      .then(response => {
        console.log(response.data.message || 'Microsoft Teams opened successfully');
      })
      .catch(error => {
        console.error('There was an error opening Microsoft Teams!', error);
      });
  };

  const openWord = () => {
    axios.post(`${backendUrl}/shortcuts/word/open-word/`)
      .then(response => {
        console.log(response.data.message || 'Microsoft Word opened successfully');
      })
      .catch(error => {
        console.error('There was an error opening Microsoft Word!', error);
      });
  };

  const openExcel = () => {
    axios.post(`${backendUrl}/shortcuts/excel/open-excel/`)
      .then(response => {
        console.log(response.data.message || 'Microsoft Excel opened successfully');
      })
      .catch(error => {
        console.error('There was an error opening Microsoft Excel!', error);
      });
  };

  const openPowerPoint = () => {
    axios.post(`${backendUrl}/shortcuts/powerpoint/open-powerpoint/`)
      .then(response => {
        console.log(response.data.message || 'Microsoft PowerPoint opened successfully');
      })
      .catch(error => {
        console.error('There was an error opening Microsoft PowerPoint!', error);
      });
  };

  const openPdfReader = () => {
    axios.post(`${backendUrl}/shortcuts/pdf/open-acrobat/`)
      .then(response => {
        console.log(response.data.message || 'PDF Reader opened successfully');
      })
      .catch(error => {
        console.error('There was an error opening PDF Reader!', error);
      });
  };

  const openChrome = () => {
    axios.post(`${backendUrl}/shortcuts/chrome/open-chrome/`)
      .then(response => {
        console.log(response.data.message || 'Chrome opened successfully');
      })
      .catch(error => {
        console.error('There was an error opening Chrome!', error);
      });
  };

  const openWhatsApp = () => {
    axios.post(`${backendUrl}/shortcuts/whatsapp/open-whatsapp/`)
      .then(response => {
        console.log(response.data.message || 'WhatsApp opened successfully');
      })
      .catch(error => {
        console.error('There was an error opening WhatsApp!', error);
      });
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <img src={LogoIcon} alt="My Shortcuts Logo" className="logo-icon" />
        <h2 className="sidebar-title">InfoVision SDG</h2>
      </div>

      {/* Link și butoane pentru deschiderea aplicațiilor */}

      <Link to="/shortcuts/fileexplorer" className="sidebar-button">
        <img src={FileExplorerIcon} alt="File Explorer" className="icon" />
        File Explorer
      </Link>

      <Link to="/shortcuts/word" className="sidebar-button" onClick={openWord}>
        <img src={WordIcon} alt="Microsoft Word" className="icon" />
        Microsoft Word
      </Link>

      <Link to="/shortcuts/excel" className="sidebar-button" onClick={openExcel}>
        <img src={ExcelIcon} alt="Microsoft Excel" className="icon" />
        Microsoft Excel
      </Link>

      <Link to="/shortcuts/powerpoint" className="sidebar-button" onClick={openPowerPoint}>
        <img src={PowerPointIcon} alt="PowerPoint" className="icon" />
        PowerPoint
      </Link>

      <Link to="/shortcuts/pdf" className="sidebar-button" onClick={openPdfReader}>
        <img src={PdfIcon} alt="PDF Reader" className="icon" />
        PDF Reader
      </Link>

      <Link to="/shortcuts/chrome" className="sidebar-button" onClick={openChrome}>
        <img src={ChromeIcon} alt="Chrome" className="icon" />
        Chrome
      </Link>

      <Link to="/shortcuts/whatsapp" className="sidebar-button" onClick={openWhatsApp}>
        <img src={WhatsappIcon} alt="WhatsApp" className="icon" />
        WhatsApp
      </Link>

      <Link to="/shortcuts/teams" className="sidebar-button" onClick={openTeams}>
        <img src={TeamsIcon} alt="Microsoft Teams" className="icon" />
        Microsoft Teams
      </Link>

      <Link to="/shortcuts/zoom" className="sidebar-button">
        <img src={ZoomIcon} alt="Zoom" className="icon" />
        Zoom
      </Link>

      <Link to="/shortcuts/skype" className="sidebar-button">
        <img src={SkypeIcon} alt="Skype" className="icon" />
        Skype
      </Link>

      <Link to="/shortcuts/keyboard_mouse" className="sidebar-button">
        <KeyboardIcon alt="Keyboard_mouse" className="icon" />
        Tastatura/Mouse
      </Link>

      <div className="copyright">
        &copy; 2024-SDG
      </div>

      
    </div>
  );
};

export default Sidebar;
