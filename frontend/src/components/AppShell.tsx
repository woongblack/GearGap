import { Outlet } from 'react-router-dom';
import Background from './Background';
import Topbar from './Topbar';

export default function AppShell() {
  return (
    <>
      <Background />
      <div className="shell">
        <Topbar />
        <Outlet />
        <footer>
          <span className="legal">© 2026 GearGap · v0.4.2</span>
          <div className="links">
            <a href="#about">About</a>
            <a href="#api">API</a>
            <a href="#discord">Discord</a>
            <a href="#changelog">Changelog</a>
          </div>
        </footer>
      </div>
    </>
  );
}
