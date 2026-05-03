import { NavLink } from 'react-router-dom';
import Logo from './Logo';

export default function Topbar() {
  return (
    <nav className="topbar">
      <Logo />
      <div className="nav-links">
        <NavLink to="/" end className={({ isActive }) => (isActive ? 'active' : '')}>Search</NavLink>
        <NavLink to="/c/azshara/아즈모단" className={({ isActive }) => (isActive ? 'active' : '')}>Analysis</NavLink>
        <NavLink to="/c/azshara/아즈모단/recs" className={({ isActive }) => (isActive ? 'active' : '')}>Compare</NavLink>
        <a href="#leaderboards">Leaderboards</a>
        <button className="nav-cta">Sign In</button>
      </div>
    </nav>
  );
}
