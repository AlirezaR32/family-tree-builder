import React, { useState } from 'react';
import './PersonManager.css';

function PersonManager({ people, onAddPerson, onDeletePerson }) {
  const [formData, setFormData] = useState({
    id: '',
    name: '',
    gender: 'male',
    birth_year: '',
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.id || !formData.name) {
      alert('لطفاً شناسه و نام را وارد کنید');
      return;
    }

    const personData = {
      id: formData.id,
      name: formData.name,
      gender: formData.gender,
      birth_year: formData.birth_year ? parseInt(formData.birth_year) : null,
    };

    onAddPerson(personData);
    setFormData({ id: '', name: '', gender: 'male', birth_year: '' });
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="person-manager card">
      <h2>👤 مدیریت افراد</h2>
      
      <form onSubmit={handleSubmit} className="person-form">
        <div className="form-group">
          <label>شناسه (ID):</label>
          <input
            type="text"
            name="id"
            value={formData.id}
            onChange={handleChange}
            placeholder="مثال: p1"
            required
          />
        </div>

        <div className="form-group">
          <label>نام:</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="نام فرد"
            required
          />
        </div>

        <div className="form-group">
          <label>جنسیت:</label>
          <select name="gender" value={formData.gender} onChange={handleChange}>
            <option value="male">مرد</option>
            <option value="female">زن</option>
          </select>
        </div>

        <div className="form-group">
          <label>سال تولد (اختیاری):</label>
          <input
            type="number"
            name="birth_year"
            value={formData.birth_year}
            onChange={handleChange}
            placeholder="1370"
            min="1300"
            max="1410"
          />
        </div>

        <button type="submit" className="btn btn-primary">
          ➕ افزودن فرد
        </button>
      </form>

      <div className="people-list">
        <h3>لیست افراد ({people.length} نفر)</h3>
        {people.length === 0 ? (
          <p className="empty-message">هنوز فردی اضافه نشده است</p>
        ) : (
          <div className="people-grid">
            {people.map((person) => (
              <div key={person.id} className="person-card">
                <div className="person-info">
                  <span className="person-icon">
                    {person.gender === 'male' ? '👨' : '👩'}
                  </span>
                  <div>
                    <strong>{person.name}</strong>
                    <span className="person-id">({person.id})</span>
                    {person.birth_year && (
                      <div className="birth-year">متولد {person.birth_year}</div>
                    )}
                  </div>
                </div>
                <button
                  className="btn-delete"
                  onClick={() => onDeletePerson(person.id)}
                  title="حذف"
                >
                  🗑️
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default PersonManager;
