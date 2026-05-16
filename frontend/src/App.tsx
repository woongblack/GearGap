import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import AppShell from './components/AppShell';
import LandingScreen from './screens/LandingScreen';
import AnalysisScreen from './screens/AnalysisScreen';
import RecommendationsScreen from './screens/RecommendationsScreen';
import LoadingScreen from './screens/LoadingScreen';
import ErrorScreen from './screens/ErrorScreen';
import Toast from './components/Toast';
import { REALMS } from './data/mock';
import { api } from './api/client';

function AppRoutes() {
  const navigate = useNavigate();
  const [toast, setToast] = useState({ show: false, msg: '' });

  function handleSearch({ name, realm }: { name: string; realm: string }) {
    const realmLabel = REALMS.find(r => r.value === realm)?.label || realm;
    setToast({ show: true, msg: `Scanning ${name} · ${realmLabel} …` });

    setTimeout(() => {
      setToast(t => ({ ...t, show: false }));
      navigate('/loading', { state: { charName: name, realm } });
    }, 900);
  }

  return (
    <>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<LandingScreen onSearch={handleSearch} />} />
          <Route path="/loading" element={<LoadingScreenWrapper />} />
          <Route path="/c/:realm/:name" element={<AnalysisScreen />} />
          <Route path="/c/:realm/:name/recs" element={<RecommendationsScreen />} />
          <Route path="/errors" element={<ErrorScreen />} />
        </Route>
      </Routes>
      <Toast msg={toast.msg} show={toast.show} />
    </>
  );
}

function LoadingScreenWrapper() {
  const navigate = useNavigate();
  const location = useLocation();
  const { charName, realm } = (location.state as { charName?: string; realm?: string }) ?? {};

  useEffect(() => {
    if (!charName || !realm) {
      navigate('/', { replace: true });
      return;
    }

    api.getRoadmap(realm, charName)
      .then(roadmap => {
        navigate(`/c/${encodeURIComponent(realm)}/${encodeURIComponent(charName)}`, {
          state: { roadmap },
          replace: true,
        });
      })
      .catch(err => {
        navigate('/errors', {
          state: { message: err.message },
          replace: true,
        });
      });
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <LoadingScreen
      charName={charName}
      realm={realm}
      onCancel={() => navigate('/')}
    />
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}
