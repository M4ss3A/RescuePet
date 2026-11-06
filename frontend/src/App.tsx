import { Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { LandingPage } from './pages/LandingPage'
import { CatalogoPage } from './pages/CatalogoPage'
import { LoginPage } from './pages/LoginPage'
import { RescatistaDashboardPage } from './pages/RescatistaDashboardPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { ProtectedRoute } from './components/ProtectedRoute'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<LandingPage />} />
        <Route path="/catalogo" element={<CatalogoPage />} />
        <Route path="/login" element={<LoginPage />} />

        <Route element={<ProtectedRoute allowedRoles={['RESCATISTA']} />}>
          <Route path="/rescatista" element={<RescatistaDashboardPage />} />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}

export default App