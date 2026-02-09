import React, { useState, useEffect } from 'react';
import FamilyTreeVisualization from './components/FamilyTreeVisualization';
import PersonManager from './components/PersonManager';
import RelationshipManager from './components/RelationshipManager';
import PathFinder from './components/PathFinder';
import './App.css';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [people, setPeople] = useState([]);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    fetchPeople();
  }, []);

  const fetchPeople = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/people`);
      const data = await response.json();
      if (data.success) {
        setPeople(data.data);
      }
    } catch (error) {
      showNotification('خطا در دریافت اطلاعات: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 4000);
  };

  const handleAddPerson = async (personData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/person`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(personData),
      });
      const data = await response.json();
      if (data.success) {
        showNotification(data.message);
        fetchPeople();
      } else {
        showNotification(data.error, 'error');
      }
    } catch (error) {
      showNotification('خطا در افزودن فرد: ' + error.message, 'error');
    }
  };

  const handleDeletePerson = async (personId) => {
    if (!window.confirm('آیا از حذف این فرد اطمینان دارید؟')) return;
    
    try {
      const response = await fetch(`${API_BASE_URL}/person/${personId}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (data.success) {
        showNotification(data.message);
        fetchPeople();
      } else {
        showNotification(data.error, 'error');
      }
    } catch (error) {
      showNotification('خطا در حذف فرد: ' + error.message, 'error');
    }
  };

  const handleAddRelationship = async (relationshipData, type) => {
    try {
      const endpoint = type === 'parent-child' ? 'parent-child' : 'spouse';
      const response = await fetch(`${API_BASE_URL}/relationship/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(relationshipData),
      });
      const data = await response.json();
      if (data.success) {
        showNotification(data.message);
        fetchPeople();
      } else {
        showNotification(data.error, 'error');
      }
    } catch (error) {
      showNotification('خطا در افزودن رابطه: ' + error.message, 'error');
    }
  };

  const handleLoadSampleData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/sample-data`, {
        method: 'POST',
      });
      const data = await response.json();
      if (data.success) {
        showNotification(data.message);
        fetchPeople();
      } else {
        showNotification(data.error, 'error');
      }
    } catch (error) {
      showNotification('خطا در بارگذاری داده‌ها: ' + error.message, 'error');
    }
  };

  return (
    <div className="app" dir="rtl">
      <header className="app-header">
        <h1>🌳 سیستم شجره‌نامه خانوادگی</h1>
        <p>مدیریت و مشاهده روابط خانوادگی با الگوریتم‌های DFS و BFS</p>
      </header>

      {notification && (
        <div className={`notification ${notification.type}`}>
          {notification.message}
        </div>
      )}

      <div className="main-container">
        <div className="left-panel">
          <div className="controls-section">
            <button 
              className="btn btn-secondary" 
              onClick={handleLoadSampleData}
            >
              📥 بارگذاری داده نمونه
            </button>
          </div>

          <PersonManager 
            people={people}
            onAddPerson={handleAddPerson}
            onDeletePerson={handleDeletePerson}
          />

          <RelationshipManager 
            people={people}
            onAddRelationship={handleAddRelationship}
          />

          <PathFinder 
            people={people}
            onNotification={showNotification}
          />
        </div>

        <div className="right-panel">
          <FamilyTreeVisualization 
            people={people}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
