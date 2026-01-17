import React, { useState, useEffect } from 'react';
import { Eye, EyeOff, Plus, Trash2, Maximize2, LogOut, Video, AlertCircle, X } from 'lucide-react';

export default function CCTVDashboard() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [cameras, setCameras] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newCamera, setNewCamera] = useState({ name: '', url: '' });
  const [gridMode, setGridMode] = useState('2x2');
  const [expandedCamera, setExpandedCamera] = useState(null);
  const [error, setError] = useState('');

  // Demo credentials
  const DEMO_CREDENTIALS = { username: 'admin', password: 'admin123' };

  useEffect(() => {
    // Load Google Fonts
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Outfit:wght@700&family=DM+Sans:wght@400;500;600&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    if (credentials.username === DEMO_CREDENTIALS.username && 
        credentials.password === DEMO_CREDENTIALS.password) {
      setIsAuthenticated(true);
      setError('');
    } else {
      setError('Invalid credentials');
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setCredentials({ username: '', password: '' });
    setCameras([]);
  };

  const addCamera = () => {
    if (newCamera.name && newCamera.url) {
      setCameras([...cameras, { 
        id: Date.now(), 
        name: newCamera.name, 
        url: newCamera.url,
        status: 'online'
      }]);
      setNewCamera({ name: '', url: '' });
      setShowAddModal(false);
    }
  };

  const removeCamera = (id) => {
    setCameras(cameras.filter(cam => cam.id !== id));
    if (expandedCamera === id) setExpandedCamera(null);
  };

  const getGridClass = () => {
    switch(gridMode) {
      case '1x1': return 'grid-cols-1';
      case '2x2': return 'grid-cols-1 md:grid-cols-2';
      case '3x3': return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3';
      case '4x4': return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4';
      default: return 'grid-cols-1 md:grid-cols-2';
    }
  };

  if (!isAuthenticated) {
    return (
      <>
        <style>{`
          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }
          
          body {
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          }
          
          html, body, #root {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
          }
          
          .login-container {
            min-height: 100vh;
            width: 100%;
            background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #020617 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            position: relative;
            overflow: hidden;
          }
          
          .bg-animation {
            position: absolute;
            inset: 0;
            opacity: 0.2;
            pointer-events: none;
          }
          
          .bg-blob-1 {
            position: absolute;
            top: 25%;
            left: 25%;
            width: 400px;
            height: 400px;
            background: #3b82f6;
            border-radius: 50%;
            filter: blur(80px);
            animation: pulse-animation 4s ease-in-out infinite;
          }
          
          .bg-blob-2 {
            position: absolute;
            bottom: 25%;
            right: 25%;
            width: 400px;
            height: 400px;
            background: #06b6d4;
            border-radius: 50%;
            filter: blur(80px);
            animation: pulse-animation 4s ease-in-out infinite;
            animation-delay: 700ms;
          }
          
          @keyframes pulse-animation {
            0%, 100% { opacity: 0.2; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(1.1); }
          }
          
          .login-box {
            width: 100%;
            max-width: 450px;
            position: relative;
            z-index: 10;
            background: rgba(15, 23, 42, 0.5);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(71, 85, 105, 0.5);
            border-radius: 1.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            padding: 2.5rem;
          }
          
          .logo-container {
            text-align: center;
            margin-bottom: 2.5rem;
          }
          
          .logo-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 4rem;
            height: 4rem;
            background: linear-gradient(135deg, #3b82f6, #06b6d4);
            border-radius: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
          }
          
          .logo-title {
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(to right, #60a5fa, #22d3ee);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
          }
          
          .logo-subtitle {
            color: #94a3b8;
            font-size: 0.875rem;
          }
          
          .form-group {
            margin-bottom: 1.5rem;
          }
          
          .form-label {
            display: block;
            font-size: 0.875rem;
            font-weight: 500;
            color: #cbd5e1;
            margin-bottom: 0.5rem;
          }
          
          .form-input {
            width: 100%;
            padding: 0.875rem 1rem;
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid #334155;
            border-radius: 0.75rem;
            color: #f1f5f9;
            font-size: 1rem;
            transition: all 0.2s;
          }
          
          .form-input:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
          }
          
          .form-input::placeholder {
            color: #64748b;
          }
          
          .password-wrapper {
            position: relative;
          }
          
          .password-toggle {
            position: absolute;
            right: 1rem;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: #94a3b8;
            cursor: pointer;
            padding: 0.5rem;
            display: flex;
            align-items: center;
            transition: color 0.2s;
          }
          
          .password-toggle:hover {
            color: #cbd5e1;
          }
          
          .error-message {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.875rem;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 0.5rem;
            color: #fca5a5;
            font-size: 0.875rem;
            margin-bottom: 1.5rem;
          }
          
          .submit-button {
            width: 100%;
            padding: 0.875rem;
            background: linear-gradient(to right, #3b82f6, #06b6d4);
            border: none;
            border-radius: 0.75rem;
            color: white;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
          }
          
          .submit-button:hover {
            background: linear-gradient(to right, #2563eb, #0891b2);
            transform: scale(1.02);
          }
          
          .submit-button:active {
            transform: scale(0.98);
          }
          
          .demo-hint {
            text-align: center;
            margin-top: 1.5rem;
            font-size: 0.75rem;
            color: #64748b;
          }
        `}</style>
        
        <div className="login-container">
          <div className="bg-animation">
            <div className="bg-blob-1"></div>
            <div className="bg-blob-2"></div>
          </div>

          <div className="login-box">
            <div className="logo-container">
              <div className="logo-icon">
                <Video size={32} color="white" />
              </div>
              <h1 className="logo-title">SecureVision</h1>
              <p className="logo-subtitle">Enterprise CCTV Monitoring System</p>
            </div>

            <form onSubmit={handleLogin}>
              <div className="form-group">
                <label className="form-label">Username</label>
                <input
                  type="text"
                  value={credentials.username}
                  onChange={(e) => setCredentials({...credentials, username: e.target.value})}
                  className="form-input"
                  placeholder="Enter username"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Password</label>
                <div className="password-wrapper">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={credentials.password}
                    onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                    className="form-input"
                    placeholder="Enter password"
                    style={{ paddingRight: '3rem' }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="password-toggle"
                  >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>
              </div>

              {error && (
                <div className="error-message">
                  <AlertCircle size={16} />
                  <span>{error}</span>
                </div>
              )}

              <button type="submit" className="submit-button">
                Access Dashboard
              </button>

              <p className="demo-hint">
                Demo: admin / admin123
              </p>
            </form>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <style>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        
        body {
          font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          background: #020617;
          color: #f1f5f9;
        }
        
        .dashboard {
          min-height: 100vh;
          background: #020617;
        }
        
        .header {
          background: rgba(15, 23, 42, 0.8);
          backdrop-filter: blur(20px);
          border-bottom: 1px solid #1e293b;
          padding: 1rem 1.5rem;
          display: flex;
          align-items: center;
          justify-content: space-between;
          position: sticky;
          top: 0;
          z-index: 50;
        }
        
        .header-left {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }
        
        .header-logo {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 2.5rem;
          height: 2.5rem;
          background: linear-gradient(135deg, #3b82f6, #06b6d4);
          border-radius: 0.5rem;
          box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.2);
        }
        
        .header-title {
          font-family: 'Outfit', sans-serif;
          font-size: 1.25rem;
          font-weight: 700;
          background: linear-gradient(to right, #60a5fa, #22d3ee);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
        
        .header-subtitle {
          font-size: 0.75rem;
          color: #64748b;
        }
        
        .header-right {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }
        
        .btn {
          padding: 0.5rem 1rem;
          border: none;
          border-radius: 0.5rem;
          font-size: 0.875rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        
        .btn-primary {
          background: #3b82f6;
          color: white;
          box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.2);
        }
        
        .btn-primary:hover {
          background: #2563eb;
        }
        
        .btn-icon {
          padding: 0.5rem;
          background: transparent;
          color: #94a3b8;
        }
        
        .btn-icon:hover {
          background: #1e293b;
          color: #ef4444;
        }
        
        .select {
          padding: 0.5rem 1rem;
          background: #1e293b;
          border: 1px solid #334155;
          border-radius: 0.5rem;
          color: #cbd5e1;
          font-size: 0.875rem;
          cursor: pointer;
        }
        
        .select:focus {
          outline: none;
          border-color: #3b82f6;
        }
        
        .main-content {
          padding: 1.5rem;
        }
        
        .empty-state {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          min-height: 70vh;
          text-align: center;
        }
        
        .empty-icon {
          width: 6rem;
          height: 6rem;
          background: rgba(30, 41, 59, 0.5);
          border-radius: 1.5rem;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 1.5rem;
        }
        
        .empty-title {
          font-family: 'Outfit', sans-serif;
          font-size: 1.5rem;
          font-weight: 700;
          color: #cbd5e1;
          margin-bottom: 0.5rem;
        }
        
        .empty-text {
          color: #64748b;
          max-width: 28rem;
          margin-bottom: 1.5rem;
        }
        
        .camera-grid {
          display: grid;
          gap: 1.5rem;
        }
        
        .grid-cols-1 {
          grid-template-columns: 1fr;
        }
        
        @media (min-width: 768px) {
          .grid-cols-2 {
            grid-template-columns: repeat(2, 1fr);
          }
        }
        
        @media (min-width: 1024px) {
          .grid-cols-3 {
            grid-template-columns: repeat(3, 1fr);
          }
          .grid-cols-4 {
            grid-template-columns: repeat(4, 1fr);
          }
        }
        
        .camera-card {
          position: relative;
          background: #0f172a;
          border: 1px solid #1e293b;
          border-radius: 1rem;
          overflow: hidden;
          box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
          transition: all 0.3s;
        }
        
        .camera-card:hover {
          box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        }
        
        .camera-header {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          background: linear-gradient(to bottom, rgba(15, 23, 42, 0.9), transparent);
          padding: 1rem;
          z-index: 10;
          display: flex;
          align-items: center;
          justify-content: space-between;
          opacity: 0;
          transition: opacity 0.3s;
        }
        
        .camera-card:hover .camera-header {
          opacity: 1;
        }
        
        .camera-name {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.875rem;
          font-weight: 600;
          color: white;
        }
        
        .status-dot {
          width: 0.5rem;
          height: 0.5rem;
          background: #22c55e;
          border-radius: 50%;
          animation: pulse-dot 2s ease-in-out infinite;
        }
        
        @keyframes pulse-dot {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        
        .camera-actions {
          display: flex;
          gap: 0.5rem;
        }
        
        .action-btn {
          padding: 0.5rem;
          background: rgba(30, 41, 59, 0.8);
          border: none;
          border-radius: 0.5rem;
          color: white;
          cursor: pointer;
          display: flex;
          align-items: center;
          transition: all 0.2s;
        }
        
        .action-btn:hover {
          background: #334155;
        }
        
        .action-btn-danger:hover {
          background: #ef4444;
        }
        
        .camera-video {
          aspect-ratio: 16 / 9;
          background: #1e293b;
          position: relative;
        }
        
        .camera-video iframe {
          width: 100%;
          height: 100%;
          border: none;
        }
        
        .camera-footer {
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          background: linear-gradient(to top, rgba(15, 23, 42, 0.9), transparent);
          padding: 0.75rem;
          opacity: 0;
          transition: opacity 0.3s;
        }
        
        .camera-card:hover .camera-footer {
          opacity: 1;
        }
        
        .camera-status {
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-size: 0.75rem;
          color: #cbd5e1;
        }
        
        .live-badge {
          display: flex;
          align-items: center;
          gap: 0.25rem;
        }
        
        .live-dot {
          width: 0.375rem;
          height: 0.375rem;
          background: #22c55e;
          border-radius: 50%;
        }
        
        .modal-overlay {
          position: fixed;
          inset: 0;
          background: rgba(0, 0, 0, 0.6);
          backdrop-filter: blur(4px);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 1rem;
          z-index: 100;
        }
        
        .modal {
          background: #0f172a;
          border: 1px solid #334155;
          border-radius: 1.5rem;
          box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
          padding: 1.5rem;
          width: 100%;
          max-width: 28rem;
        }
        
        .modal-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 1.5rem;
        }
        
        .modal-title {
          font-family: 'Outfit', sans-serif;
          font-size: 1.25rem;
          font-weight: 700;
          color: white;
        }
        
        .close-btn {
          padding: 0.5rem;
          background: transparent;
          border: none;
          color: #94a3b8;
          cursor: pointer;
          display: flex;
          align-items: center;
          transition: all 0.2s;
          border-radius: 0.5rem;
        }
        
        .close-btn:hover {
          background: #1e293b;
          color: white;
        }
        
        .modal-body {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        
        .modal-hint {
          font-size: 0.75rem;
          color: #64748b;
          margin-top: 0.5rem;
        }
        
        .modal-actions {
          display: flex;
          gap: 0.75rem;
          margin-top: 1rem;
        }
        
        .btn-cancel {
          flex: 1;
          padding: 0.875rem;
          background: #1e293b;
          color: #cbd5e1;
        }
        
        .btn-cancel:hover {
          background: #334155;
        }
        
        .btn-submit {
          flex: 1;
          padding: 0.875rem;
          background: linear-gradient(to right, #3b82f6, #06b6d4);
          color: white;
          font-weight: 600;
        }
        
        .btn-submit:hover {
          background: linear-gradient(to right, #2563eb, #0891b2);
        }
      `}</style>

      <div className="dashboard">
        <header className="header">
          <div className="header-left">
            <div className="header-logo">
              <Video size={20} color="white" />
            </div>
            <div>
              <div className="header-title">SecureVision</div>
              <div className="header-subtitle">
                {cameras.length} {cameras.length === 1 ? 'Camera' : 'Cameras'} Active
              </div>
            </div>
          </div>

          <div className="header-right">
            <button onClick={() => setShowAddModal(true)} className="btn btn-primary">
              <Plus size={16} />
              Add Camera
            </button>

            <select
              value={gridMode}
              onChange={(e) => setGridMode(e.target.value)}
              className="select"
            >
              <option value="1x1">1×1 Grid</option>
              <option value="2x2">2×2 Grid</option>
              <option value="3x3">3×3 Grid</option>
              <option value="4x4">4×4 Grid</option>
            </select>

            <button onClick={handleLogout} className="btn btn-icon" title="Logout">
              <LogOut size={20} />
            </button>
          </div>
        </header>

        <main className="main-content">
          {cameras.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">
                <Video size={48} color="#475569" />
              </div>
              <h2 className="empty-title">No Cameras Added</h2>
              <p className="empty-text">
                Start monitoring by adding your first CCTV camera stream. Click the "Add Camera" button to get started.
              </p>
              <button onClick={() => setShowAddModal(true)} className="btn btn-primary">
                <Plus size={20} />
                Add Your First Camera
              </button>
            </div>
          ) : (
            <div className={`camera-grid ${getGridClass()}`}>
              {cameras.map((camera) => (
                <div key={camera.id} className="camera-card">
                  <div className="camera-header">
                    <div className="camera-name">
                      <div className="status-dot"></div>
                      {camera.name}
                    </div>
                    <div className="camera-actions">
                      <button
                        onClick={() => setExpandedCamera(expandedCamera === camera.id ? null : camera.id)}
                        className="action-btn"
                        title="Maximize"
                      >
                        <Maximize2 size={16} />
                      </button>
                      <button
                        onClick={() => removeCamera(camera.id)}
                        className="action-btn action-btn-danger"
                        title="Remove"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>

                  <div className="camera-video">
                    <iframe
                      src={camera.url}
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                      title={camera.name}
                    />
                  </div>

                  <div className="camera-footer">
                    <div className="camera-status">
                      <span className="live-badge">
                        <div className="live-dot"></div>
                        LIVE
                      </span>
                      <span>{new Date().toLocaleTimeString()}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </main>

        {showAddModal && (
          <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h3 className="modal-title">Add New Camera</h3>
                <button onClick={() => setShowAddModal(false)} className="close-btn">
                  <X size={20} />
                </button>
              </div>

              <div className="modal-body">
                <div className="form-group">
                  <label className="form-label">Camera Name</label>
                  <input
                    type="text"
                    value={newCamera.name}
                    onChange={(e) => setNewCamera({...newCamera, name: e.target.value})}
                    className="form-input"
                    placeholder="e.g., Main Entrance"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Stream URL</label>
                  <input
                    type="text"
                    value={newCamera.url}
                    onChange={(e) => setNewCamera({...newCamera, url: e.target.value})}
                    className="form-input"
                    placeholder="rtsp:// or https://"
                  />
                  <p className="modal-hint">
                    Supports RTSP, HTTP, or embedded YouTube/streaming URLs
                  </p>
                </div>

                <div className="modal-actions">
                  <button onClick={() => setShowAddModal(false)} className="btn btn-cancel">
                    Cancel
                  </button>
                  <button onClick={addCamera} className="btn btn-submit">
                    Add Camera
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}