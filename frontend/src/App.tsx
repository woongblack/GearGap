import { useState } from 'react';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import AppShell from './components/AppShell';
import LandingScreen from './screens/LandingScreen';
import AnalysisScreen from './screens/AnalysisScreen';
import RecommendationsScreen from './screens/RecommendationsScreen';
import LoadingScreen from './screens/LoadingScreen';
import ErrorScreen from './screens/ErrorScreen';
import Toast from './components/Toast';
import { REALMS } from './data/mock';

function AppRoutes() {
  const navigate = useNavigate();
  const [toast, setToast] = useState({ show: false, msg: '' });

  function handleSearch({ name, realm }: { name: string; realm: string }) {
    const realmLabel = REALMS.find(r => r.value === realm)?.label || realm;
    setToast({ show: true, msg: `Scanning ${name} · ${realmLabel} …` });
    
    setTimeout(() => {
      setToast(t => ({ ...t, show: false }));
      navigate('/loading', { state: { charName: name, realm: realmLabel } });
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

// Wrapper for LoadingScreen to handle navigation
import { useLocation } from 'react-router-dom';
function LoadingScreenWrapper() {
  const navigate = useNavigate();
  const location = useLocation();
  const { charName, realm } = location.state || { charName: '아즈모단', realm: '아즈샤라' };

  return (
    <LoadingScreen 
      charName={charName} 
      realm={realm} 
      onCancel={() => navigate('/')} 
      onComplete={() => navigate(`/c/${realm}/${charName}`)} 
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
