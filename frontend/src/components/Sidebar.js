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
  const [openWordDocs, setOpenWordDocs] = useState([]); 
  const [openExcelDocs, setOpenExcelDocs] = useState([]); 
  const [openPowerPointDocs, setOpenPowerPointDocs] = useState([]); 

  useEffect(() => {
    fetchBackendUrl();
    const interval = setInterval(fetchAllOpenDocs, 5000); 
    return () => clearInterval(interval);
  }, []);

  const fetchBackendUrl = async () => {
    try {
      const response = await axios.get('/api/server-info');
      const { ip, port } = response.data;
      const url = `http://${ip}:${port}`;
      setBackendUrl(url);
    } catch (error) {
      console.error('Error fetching the backend URL!', error);
    }
  };

  const fetchAllOpenDocs = () => {
    const apps = [
      { appName: 'word', setter: setOpenWordDocs },
      { appName: 'excel', setter: setOpenExcelDocs },
      { appName: 'powerpoint', setter: setOpenPowerPointDocs }
    ];

    apps.forEach(({ appName, setter }) => {
      fetchOpenDocs(appName, setter);
    });
  };

  const fetchOpenDocs = async (appName, setDocs) => {
    try {
      const response = await axios.get(`/shortcuts/file-explorer/list_open_files/${appName}/`);
      if (response.data.success) {
        console.log(`Fetched ${appName} docs:`, response.data.files); 
        setDocs(response.data.files);
      }
    } catch (error) {
      console.error(`Error fetching open ${appName} documents:`, error);
    }
  };

  const activateDoc = async (appName, filePath, endpoint) => {
    try {
      console.log("Activating document:", filePath);
      const response = await axios.get(endpoint, { params: { filePath } });
      console.log("Server response:", response);  // Debug full response

      if (response.data.success) {
        console.log(response.data.message);
      } else {
        console.error(`Could not activate the ${appName} document:`, response.data.message);
      }
    } catch (error) {
      console.error(`Error activating ${appName} document:`, error);
    }
  };

  const openApp = (appName) => {
    axios.post(`${backendUrl}/shortcuts/${appName}/open-${appName}/`)
      .then(response => console.log(response.data.message || `${appName} opened successfully`))
      .catch(error => console.error(`Error opening ${appName}!`, error));
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <img src={LogoIcon} alt="My Shortcuts Logo" className="logo-icon" />
        <h2 className="sidebar-title">My Shortcuts</h2>
      </div>

      {/* Link și butoane pentru deschiderea aplicațiilor */}

      <Link to="/shortcuts/fileexplorer" className="sidebar-button">
        <img src={FileExplorerIcon} alt="File Explorer" className="icon" />
        File Explorer
      </Link>

      <Link to="/shortcuts/teams" className="sidebar-button" onClick={() => openApp('teams')}>
        <img src={TeamsIcon} alt="Microsoft Teams" className="icon" />
        Microsoft Teams
      </Link>

      <Link to="/shortcuts/skype" className="sidebar-button">
        <img src={SkypeIcon} alt="Skype" className="icon" />
        Skype
      </Link>

      {/* Word Section */}
      <Link to="/shortcuts/word" className="sidebar-button" onClick={() => openApp('word')}>
        <img src={WordIcon} alt="Microsoft Word" className="icon" />
        Microsoft Word
      </Link>
      <div className="open-docs">
        {openWordDocs.map((doc, index) => (
          <button
            key={index}
            onClick={() => activateDoc('word', doc.path, '/shortcuts/word/activate_word_file')}
            className="open-doc-button"
          >
            {doc.name}
          </button>
        ))}
      </div>

      {/* Excel Section */}
      <Link to="/shortcuts/excel" className="sidebar-button" onClick={() => openApp('excel')}>
        <img src={ExcelIcon} alt="Microsoft Excel" className="icon" />
        Microsoft Excel
      </Link>
      <div className="open-docs">
        {openExcelDocs.map((doc, index) => (
          <button
            key={index}
            onClick={() => activateDoc('excel', doc.path, '/shortcuts/excel/activate_excel_file')}
            className="open-doc-button"
          >
            {doc.name}
          </button>
        ))}
      </div>

      {/* PowerPoint Section */}
      <Link to="/shortcuts/powerpoint" className="sidebar-button" onClick={() => openApp('powerpoint')}>
        <img src={PowerPointIcon} alt="PowerPoint" className="icon" />
        PowerPoint
      </Link>
      <div className="open-docs">
        {openPowerPointDocs.map((doc, index) => (
          <button
            key={index}
            onClick={() => activateDoc('powerpoint', doc.path, '/shortcuts/powerpoint/activate_powerpoint_file')}
            className="open-doc-button"
          >
            {doc.name}
          </button>
        ))}
      </div>

      <Link to="/shortcuts/pdf" className="sidebar-button" onClick={() => openApp('pdf')}>
        <img src={PdfIcon} alt="PDF Reader" className="icon" />
        PDF Reader
      </Link>

      <Link to="/shortcuts/chrome" className="sidebar-button" onClick={() => openApp('chrome')}>
        <img src={ChromeIcon} alt="Chrome" className="icon" />
        Chrome
      </Link>

      <Link to="/shortcuts/keyboard_mouse" className="sidebar-button">
        <KeyboardIcon alt="Keyboard_mouse" className="icon" />
        Tastatura/Mouse
      </Link>

      <div className="copyright">
        &copy; 2024-Costeniuc Daniel
      </div>

      
    </div>
  );
};

export default Sidebar;
