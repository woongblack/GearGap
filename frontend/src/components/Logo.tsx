import { Link } from 'react-router-dom';

export default function Logo() {
  return (
    <Link to="/" className="logo">
      <span className="logo-mark">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <path d="M16 2 L28 9 L28 23 L16 30 L4 23 L4 9 Z"
                stroke="var(--gold)" strokeWidth="1.2" fill="oklch(0.22 0.014 65)" />
          <path d="M16 8 L23 12 L23 20 L16 24 L9 20 L9 12 Z"
                stroke="var(--gold-deep)" strokeWidth="0.8" fill="none" />
          <circle cx="16" cy="16" r="2.5" fill="var(--gold)" />
          <path d="M16 11 L16 14 M16 18 L16 21 M11 16 L14 16 M18 16 L21 16"
                stroke="var(--gold)" strokeWidth="1" />
        </svg>
      </span>
      <span>Gear<span className="logo-gap">Gap</span></span>
    </Link>
  );
}
