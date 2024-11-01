import React, { useState, useEffect } from 'react';
import '../assets/styles/Zoom.css';
import RefreshIcon from '@mui/icons-material/Refresh';
import axios from 'axios';

const Zoom = () => {
  const [userInfo, setUserInfo] = useState(null);
  const [error, setError] = useState('');
  const [authenticated, setAuthenticated] = useState(null);
  const [backendUrl, setBackendUrl] = useState('');
  const [accessToken, setAccessToken] = useState(''); // Token de acces

  // Fetch backend URL from the server
  const fetchBackendUrl = async () => {
    try {
      const response = await axios.get('/api/server-info');
      const { ip, port } = response.data;
      const url = `http://${ip}:${port}`;
      setBackendUrl(url);
    } catch (error) {
      console.error('Error fetching backend URL:', error);
    }
  };

  // Check if the user is authenticated and retrieve the access token
  const checkAuthentication = () => {
    const savedToken = localStorage.getItem('zoom_access_token');
    
    if (savedToken) {
      setAccessToken(savedToken);
      setAuthenticated(true);
      fetchUserInfo(); 
    } else {
      axios.get(`${backendUrl}/shortcuts/zoom/check-auth/`)
        .then(response => {
          const data = response.data;
          if (data.authenticated) {
            setAuthenticated(true);
            setAccessToken(data.access_token);
            localStorage.setItem('zoom_access_token', data.access_token);
            fetchUserInfo();
          } else {
            setAuthenticated(false);
          }
        })
        .catch(err => {
          console.error('Error:', err);
          setAuthenticated(false);
        });
    }
  };

  // Fetch user info (list of contact names) from the backend
  const fetchUserInfo = () => {
    axios.get(`${backendUrl}/shortcuts/zoom/get-contacts/`)
      .then(response => {
        const data = response.data;
        console.log("Response from backend:", data);
  
        if (data.success) {
          if (Array.isArray(data.contact_names)) {
            setUserInfo(data.contact_names); // Setează lista de nume a contactelor
          } else {
            setError('Expected an array of contact names, but received something else.');
          }
        } else {
          setError(data.error || 'Unable to fetch user info');
        }
      })
      .catch(err => {
        setError('An error occurred while fetching user info');
        console.error('Error:', err);
      });
  };

  useEffect(() => {
    fetchBackendUrl(); // Fetch the backend URL first
  }, []);

  useEffect(() => {
    if (backendUrl) {
      checkAuthentication(); // Check authentication after backend URL is fetched
    }
  }, [backendUrl]);

  const handleLogin = () => {
    window.location.href = `${backendUrl}/shortcuts/zoom/oauth/login/`;
  };

  // Funcția pentru a deschide Zoom
  const handleOpenZoom = () => {
    axios.post(`${backendUrl}/shortcuts/zoom/open-zoom/`)
      .then(response => {
        if (response.data.success) {
          alert("Zoom has been opened successfully.");
        } else {
          alert("Failed to open Zoom: " + response.data.message);
        }
      })
      .catch(err => {
        alert("Error while opening Zoom.");
        console.error('Error:', err);
      });
  };

  // Logout handler
  const handleLogout = () => {
    localStorage.removeItem('zoom_access_token'); // Ștergem tokenul din localStorage
    setAuthenticated(false); // Resetăm starea de autentificare
    setAccessToken(''); // Resetăm tokenul de acces
  };

  if (authenticated === null) {
    return <p>Verific autentificarea...</p>;
  }

  return (
    <div className="zoom-container">
      <h1 className="title">Zoom</h1>

      {!authenticated ? (
        <button onClick={handleLogin} className="button login-button">
          Autentificare cu Zoom
        </button>
      ) : (
        <>
          {/* Show user contacts */}
          {error && <p className="error">{error}</p>}
          {userInfo && Array.isArray(userInfo) ? (
            <ul className="contacts-list">
              {userInfo.map((name, index) => (
                <li key={index}>
                  <strong>Nume:</strong> {name} {/* Afișăm doar numele contactelor */}
                </li>
              ))}
            </ul>
          ) : (
            <p>{error || 'No contacts found.'}</p>
          )}

          {/* Zoom Control Buttons */}
          <div className="button-container">
            <button className="button activate-zoom-button" onClick={handleOpenZoom}>
              <RefreshIcon className="button-icon" /> Adu în față Zoom
            </button>
            
            {/* Logout Button */}
            <button onClick={handleLogout} className="button logout-button">
              Logout
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Zoom;
