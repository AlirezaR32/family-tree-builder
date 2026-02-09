import React, { useState } from 'react';
import './RelationshipManager.css';

function RelationshipManager({ people, onAddRelationship }) {
  const [relationshipType, setRelationshipType] = useState('parent-child');
  const [parentId, setParentId] = useState('');
  const [childId, setChildId] = useState('');
  const [person1Id, setPerson1Id] = useState('');
  const [person2Id, setPerson2Id] = useState('');

  const handleSubmitParentChild = (e) => {
    e.preventDefault();
    if (!parentId || !childId) {
      alert('لطفاً والد و فرزند را انتخاب کنید');
      return;
    }
    if (parentId === childId) {
      alert('یک فرد نمی‌تواند والد خودش باشد');
      return;
    }
    onAddRelationship({ parent_id: parentId, child_id: childId }, 'parent-child');
    setParentId('');
    setChildId('');
  };

  const handleSubmitSpouse = (e) => {
    e.preventDefault();
    if (!person1Id || !person2Id) {
      alert('لطفاً هر دو همسر را انتخاب کنید');
      return;
    }
    if (person1Id === person2Id) {
      alert('یک فرد نمی‌تواند همسر خودش باشد');
      return;
    }
    onAddRelationship({ person1_id: person1Id, person2_id: person2Id }, 'spouse');
    setPerson1Id('');
    setPerson2Id('');
  };

  return (
    <div className="relationship-manager card">
      <h2>🔗 مدیریت روابط</h2>

      <div className="relationship-type-selector">
        <button
          className={`type-btn ${relationshipType === 'parent-child' ? 'active' : ''}`}
          onClick={() => setRelationshipType('parent-child')}
        >
          👨‍👩‍👧‍👦 والد - فرزند
        </button>
        <button
          className={`type-btn ${relationshipType === 'spouse' ? 'active' : ''}`}
          onClick={() => setRelationshipType('spouse')}
        >
          💑 همسر
        </button>
      </div>

      {relationshipType === 'parent-child' ? (
        <form onSubmit={handleSubmitParentChild} className="relationship-form">
          <div className="form-group">
            <label>والد:</label>
            <select
              value={parentId}
              onChange={(e) => setParentId(e.target.value)}
              required
            >
              <option value="">انتخاب کنید</option>
              {people.map((person) => (
                <option key={person.id} value={person.id}>
                  {person.name} ({person.id}) - {person.gender === 'male' ? 'مرد' : 'زن'}
                </option>
              ))}
            </select>
          </div>

          <div className="arrow">⬇️</div>

          <div className="form-group">
            <label>فرزند:</label>
            <select
              value={childId}
              onChange={(e) => setChildId(e.target.value)}
              required
            >
              <option value="">انتخاب کنید</option>
              {people.map((person) => (
                <option key={person.id} value={person.id}>
                  {person.name} ({person.id}) - {person.gender === 'male' ? 'مرد' : 'زن'}
                </option>
              ))}
            </select>
          </div>

          <button type="submit" className="btn btn-primary">
            ➕ افزودن رابطه والد-فرزند
          </button>
        </form>
      ) : (
        <form onSubmit={handleSubmitSpouse} className="relationship-form">
          <div className="form-group">
            <label>همسر اول:</label>
            <select
              value={person1Id}
              onChange={(e) => setPerson1Id(e.target.value)}
              required
            >
              <option value="">انتخاب کنید</option>
              {people.map((person) => (
                <option key={person.id} value={person.id}>
                  {person.name} ({person.id}) - {person.gender === 'male' ? 'مرد' : 'زن'}
                </option>
              ))}
            </select>
          </div>

          <div className="arrow">💕</div>

          <div className="form-group">
            <label>همسر دوم:</label>
            <select
              value={person2Id}
              onChange={(e) => setPerson2Id(e.target.value)}
              required
            >
              <option value="">انتخاب کنید</option>
              {people.map((person) => (
                <option key={person.id} value={person.id}>
                  {person.name} ({person.id}) - {person.gender === 'male' ? 'مرد' : 'زن'}
                </option>
              ))}
            </select>
          </div>

          <button type="submit" className="btn btn-primary">
            ➕ افزودن رابطه همسری
          </button>
        </form>
      )}
    </div>
  );
}

export default RelationshipManager;
