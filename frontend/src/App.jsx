import React, { useState, useEffect } from 'react';
import './index.css';

function App() {
  const [reports, setReports] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState('dashboard');

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
        const response = await fetch(`${baseUrl}/reports`);
        const data = await response.json();
        setReports(data);
      } catch (err) {
        console.error("Failed to fetch reports:", err);
      }
    };

    const fetchUsers = async () => {
      try {
        const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
        const response = await fetch(`${baseUrl}/users`);
        const data = await response.json();
        setUsers(data);
      } catch (err) {
        console.error("Failed to fetch users:", err);
      }
    };

    const initialFetch = async () => {
      setLoading(true);
      await Promise.all([fetchReports(), fetchUsers()]);
      setLoading(false);
    };

    initialFetch();
    const interval = setInterval(() => {
      fetchReports();
      fetchUsers();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  if (loading) return <div style={{ display: 'grid', placeItems: 'center', height: '100vh', fontSize: '2rem' }}>Loading SafeTrack Dashboard...</div>;

  const getStatusStyle = (risk) => {
    if (risk === 'Red') return { color: '#ef4444', fontWeight: 'bold' };
    if (risk === 'Yellow') return { color: '#f59e0b', fontWeight: 'bold' };
    return { color: '#10b981', fontWeight: 'bold' };
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h1 style={{ fontSize: '1.5rem', marginBottom: '2rem', color: '#4f46e5' }}>SafeTrack Admin</h1>
        <nav>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li
              className={`btn ${view === 'dashboard' ? 'active' : ''}`}
              style={{ marginBottom: '1rem', cursor: 'pointer', padding: '10px', borderRadius: '8px', backgroundColor: view === 'dashboard' ? '#4f46e5' : 'transparent', color: view === 'dashboard' ? 'white' : '#94a3b8' }}
              onClick={() => setView('dashboard')}
            >
              📊 Dashboard
            </li>
            <li
              className={`btn ${view === 'patients' ? 'active' : ''}`}
              style={{ marginBottom: '1rem', cursor: 'pointer', padding: '10px', borderRadius: '8px', backgroundColor: view === 'patients' ? '#4f46e5' : 'transparent', color: view === 'patients' ? 'white' : '#94a3b8' }}
              onClick={() => setView('patients')}
            >
              👥 Patients
            </li>
            <li style={{ marginBottom: '1rem', color: '#334155', padding: '10px' }}>🔔 Alerts</li>
            <li style={{ marginBottom: '1rem', color: '#334155', padding: '10px' }}>📈 Analytics</li>
          </ul>
        </nav>
      </aside>

      <main className="main-content">
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <h2>{view === 'dashboard' ? 'Health Reports Overview' : 'Registered Patients List'}</h2>
          <div style={{ color: '#94a3b8' }}>Today: {new Date().toLocaleDateString()}</div>
        </header>

        {view === 'dashboard' ? (
          <>
            <section className="grid-3" style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginBottom: '2rem' }}>
              <div className="card">
                <h3 style={{ color: '#94a3b8', fontSize: '0.9rem' }}>Total Patients</h3>
                <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{users.length}</p>
              </div>
              <div className="card">
                <h3 style={{ color: '#94a3b8', fontSize: '0.9rem' }}>Critical Alerts</h3>
                <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#ef4444' }}>
                  {reports.filter(r => r.medical_analysis?.risk_level === 'Red').length}
                </p>
              </div>
              <div className="card">
                <h3 style={{ color: '#94a3b8', fontSize: '0.9rem' }}>Avg Recovery</h3>
                <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#10b981' }}>86%</p>
              </div>
            </section>

            <section className="vitals-list">
              <div className="card" style={{ padding: '2rem' }}>
                <h3>Real-time Vitals Monitoring</h3>
                <table className="table" style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ color: '#94a3b8', borderBottom: '1px solid #334155' }}>
                      <th style={{ padding: '1rem' }}>Patient</th>
                      <th>Risk</th>
                      <th>Recovery</th>
                      <th>Heart Rate</th>
                      <th>SpO2</th>
                      <th>Temp</th>
                      <th>Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {reports.map((p) => (
                      <tr key={p._id} style={{ borderBottom: '1px solid #334155' }}>
                        <td style={{ padding: '1rem' }}>{p.user_id}</td>
                        <td>
                          <span style={getStatusStyle(p.medical_analysis?.risk_level)}>
                            {p.medical_analysis?.risk_level || 'Stable'}
                          </span>
                        </td>
                        <td>{p.medical_analysis?.recovery_score || 0}%</td>
                        <td>{p.heart_rate} bpm</td>
                        <td>{p.spo2}%</td>
                        <td>{p.temperature}°C</td>
                        <td style={{ color: '#94a3b8' }}>{new Date(p.timestamp).toLocaleTimeString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        ) : (
          <section className="patients-list">
            <div className="card" style={{ padding: '2rem' }}>
              <h3>Registered Patient Directory</h3>
              <table className="table" style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ color: '#94a3b8', borderBottom: '1px solid #334155' }}>
                    <th style={{ padding: '1rem' }}>Full Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Joined date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((u) => (
                    <tr key={u._id} style={{ borderBottom: '1px solid #334155' }}>
                      <td style={{ padding: '1rem' }}>{u.full_name}</td>
                      <td>{u.email}</td>
                      <td><span style={{ backgroundColor: '#1e293b', padding: '4px 8px', borderRadius: '4px' }}>{u.role}</span></td>
                      <td style={{ color: '#94a3b8' }}>{u.created_at ? new Date(u.created_at).toLocaleDateString() : 'N/A'}</td>
                      <td>
                        <button className="btn" style={{ backgroundColor: '#4f46e5', color: 'white', border: 'none', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer' }}>View Details</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
