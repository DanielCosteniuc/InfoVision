import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import FolderIcon from '../assets/icons_explorer/416376_envelope_files_folder_interface_office_icon.png';
import PdfIcon from '../assets/icons_explorer/2133056_document_eps_file_format_pdf_icon.png';
import WordIcon from '../assets/icons_explorer/272702_word_icon.png';
import ExcelIcon from '../assets/icons_explorer/272697_excel_icon.png';
import PowerPointIcon from '../assets/icons_explorer/272700_powerpoint_icon.png';
import ImageIcon from '../assets/icons_explorer/1564523_photo_pic_picture_gallery_image_icon.png';
import FileIcon from '../assets/icons_explorer/290138_document_extension_file_format_paper_icon.png';
import VideoIcon from '../assets/icons_explorer/103524_run_video_icon.png';
import { FiDownload, FiArrowUp, FiArrowLeft, FiRefreshCcw } from 'react-icons/fi';
import { AiFillHome } from 'react-icons/ai';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import Typography from '@mui/material/Typography';
import '../assets/styles/FileExplorer.css';

const truncateText = (text, maxLength) => {
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

const FileExplorer = () => {
  const [files, setFiles] = useState([]);
  const [partitions, setPartitions] = useState([]);
  const [currentPath, setCurrentPath] = useState('');
  const containerRef = useRef(null);
  const navigate = useNavigate(); // Hook pentru a naviga programatic

  useEffect(() => {
    const savedPath = localStorage.getItem('currentPath');
    if (savedPath) {
      fetchFiles(savedPath);
    } else {
      fetchPartitions();
    }
  }, []);

  useEffect(() => {
    if (currentPath) {
      localStorage.setItem('currentPath', currentPath);
    }
  }, [currentPath]);

  const fetchPartitions = () => {
    axios.get('/shortcuts/file-explorer/partitions/')
      .then(response => {
        setPartitions(response.data.partitions);
        setFiles([]);
        setCurrentPath('');
        localStorage.removeItem('currentPath');
      })
      .catch(error => {
        console.error('There was an error fetching the partitions!', error);
      });
  };

  const fetchFiles = (path) => {
    axios.get(`/shortcuts/file-explorer/list/?path=${path}`)
      .then(response => {
        setFiles(response.data.files);
        setCurrentPath(path);
      })
      .catch(error => {
        console.error('There was an error fetching the files!', error);
      });
  };

  const handlePartitionClick = (partition) => {
    fetchFiles(partition);
  };

  const handleDirectoryClick = (dir) => {
    const newPath = currentPath ? `${currentPath}/${dir}` : dir;
    fetchFiles(newPath);
  };

  const handleBackClick = () => {
    if (currentPath === '') {
      return;
    } else if (partitions.includes(currentPath)) {
      fetchPartitions();
    } else {
      const newPath = currentPath.split('/').slice(0, -1).join('/');
      if (newPath) {
        fetchFiles(newPath);
      } else {
        fetchPartitions();
      }
    }
  };

  const handleFileClick = (file) => {
    const filePath = currentPath ? `${currentPath}/${file.name}` : file.name;
  
    // Trimitem cererea către backend pentru a deschide fișierul local
    const url = `/shortcuts/file-explorer/server-action/?filePath=${encodeURIComponent(filePath)}`;
    
    fetch(url, { method: 'POST' })
      .then(response => {
        if (response.ok) {
          const ext = file.name.split('.').pop().toLowerCase();
  
          // Navigăm către ruta corectă în funcție de extensia fișierului
          if (['doc', 'docx'].includes(ext)) {
            navigate('/shortcuts/word'); // Navigăm la Microsoft Word
          } else if (['xls', 'xlsx'].includes(ext)) {
            navigate('/shortcuts/excel'); // Navigăm la Microsoft Excel
          } else if (['ppt', 'pptx'].includes(ext)) {
            navigate('/shortcuts/powerpoint'); // Navigăm la PowerPoint
          } else if (ext === 'pdf') {
            navigate('/shortcuts/pdf'); // Navigăm la PDF Reader
          } else if (['mp4', 'avi', 'mov'].includes(ext)) {
            window.open(`/shortcuts/file-explorer/play-video/?filePath=${encodeURIComponent(filePath)}`, '_blank');
          } else {
            console.log('No associated component for this file type.');
          }
        } else {
          console.error('Failed to open the file:', response.statusText);
        }
      })
      .catch(error => console.error('Error:', error));
  };
  

  const handleDownloadClick = (file, event) => {
    event.stopPropagation();
    const filePath = currentPath ? `${currentPath}/${file.name}` : file.name;
    const url = `/shortcuts/file-explorer/download/?filePath=${encodeURIComponent(filePath)}`;

    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.blob();
      })
      .then(blob => {
        const link = document.createElement('a');
        const blobUrl = window.URL.createObjectURL(blob);
        link.href = blobUrl;
        link.download = file.name;
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(blobUrl);
        document.body.removeChild(link);
      })
      .catch(error => {
        console.error('Error downloading file:', error);
      });
  };

  const getIcon = (file) => {
    const ext = file.name.split('.').pop().toLowerCase();
    if (file.is_dir) return <img src={FolderIcon} alt="Folder" className="file-icon" />;
    if (['jpg', 'jpeg', 'png', 'gif'].includes(ext)) return <img src={ImageIcon} alt="Gallery" className="file-icon" />;
    if (ext === 'pdf') return <img src={PdfIcon} alt="PDF" className="file-icon" />;
    if (['doc', 'docx'].includes(ext)) return <img src={WordIcon} alt="Word document" className="file-icon" />;
    if (['xls', 'xlsx'].includes(ext)) return <img src={ExcelIcon} alt="Excel spreadsheet" className="file-icon" />;
    if (['ppt', 'pptx'].includes(ext)) return <img src={PowerPointIcon} alt="PowerPoint presentation" className="file-icon" />;
    if (['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm', 'mpeg', 'mpg', 'm4v', '3gp', '3g2', 'ogv', 'vob'].includes(ext)) return <img src={VideoIcon} alt="Video" className="file-icon" />;
    return <img src={FileIcon} alt="File" className="file-icon" />;
  };

  const handleScrollToTop = () => {
    if (containerRef.current) {
      containerRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleHomeClick = () => {
    fetchPartitions();
  };

  return (
    <div className="file-explorer-container" ref={containerRef}>
      <div className="main-content">
        <div className="file-explorer">
          <div className="header">
            <button onClick={handleBackClick} className="icon-button">
              <FiArrowLeft />
            </button>
            <button onClick={handleHomeClick} className="icon-button">
              <AiFillHome />
            </button>
            <button onClick={() => currentPath ? fetchFiles(currentPath) : fetchPartitions()} className="icon-button">
              <FiRefreshCcw />
            </button>
            <button onClick={handleScrollToTop} className="icon-button">
              <FiArrowUp />
            </button>
            <Breadcrumbs aria-label="breadcrumb" className="breadcrumb">
              <Typography color="textPrimary">{currentPath || "Select a partition"}</Typography>
            </Breadcrumbs>
          </div>
          <div className="file-list">
            <ul className="file-entries">
              {currentPath === '' && partitions.length > 0 ? (
                partitions.map((partition, index) => (
                  <li 
                    key={index} 
                    onClick={() => handlePartitionClick(partition)} 
                    className="file-entry directory"
                  >
                    <span className="icon"><img src={FolderIcon} alt="Folder" className="file-icon" /></span>
                    <span className="file-name">{partition}</span>
                    <span className="file-type">Partition</span>
                  </li>
                ))
              ) : (
                files.map((file, index) => (
                  <li 
                    key={index} 
                    onClick={() => file.is_dir ? handleDirectoryClick(file.name) : handleFileClick(file)} 
                    className={`file-entry ${file.is_dir ? 'directory' : 'file'}`}
                  >
                    <span className="icon">{getIcon(file)}</span>
                    <span className="file-name">{truncateText(file.name, 25)}</span>
                    <span className="file-type download-container">
                      <span className="alt-text">{file.is_dir ? 'Folder' : 'File'}</span>
                      {!file.is_dir && (
                        <span className="download-icon" onClick={(e) => handleDownloadClick(file, e)}>
                          <FiDownload />
                        </span>
                      )}
                    </span>
                  </li>
                ))
              )}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileExplorer;
