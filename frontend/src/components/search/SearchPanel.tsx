import { useState } from 'react';
import type { FormEvent } from 'react';
import { REALMS } from '../../data/mock';

interface SearchPanelProps {
  onSubmit: (data: { name: string; realm: string }) => void;
}

export default function SearchPanel({ onSubmit }: SearchPanelProps) {
  const [name, setName] = useState('');
  const [realm, setRealm] = useState('azshara');

  function submit(e: FormEvent) {
    e.preventDefault();
    if (!name.trim()) return;
    onSubmit({ name: name.trim(), realm });
  }

  return (
    <div className="search-panel">
      <span className="search-corner-tr"></span>
      <span className="search-corner-bl"></span>
      <form className="search-form" onSubmit={submit}>
        <label className="field">
          <span className="field-label">Character</span>
          <input
            type="text"
            placeholder="캐릭터명을 입력하세요"
            value={name}
            onChange={(e) => setName(e.target.value)}
            autoComplete="new-password"
          />
        </label>
        <label className="field">
          <span className="field-label">Realm · KR</span>
          <select value={realm} onChange={(e) => setRealm(e.target.value)}>
            {REALMS.map((r) => (
              <option key={r.value} value={r.value}>{r.label}</option>
            ))}
          </select>
        </label>
        <button type="submit" className="search-btn">
          <svg viewBox="0 0 16 16" fill="none">
            <circle cx="7" cy="7" r="5" stroke="currentColor" strokeWidth="1.6"/>
            <path d="M11 11 L14 14" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round"/>
          </svg>
          Analyze
        </button>
      </form>
    </div>
  );
}
