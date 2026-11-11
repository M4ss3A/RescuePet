import { Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { LandingPage } from './pages/LandingPage'
import { CatalogoPage } from './pages/CatalogoPage'
import { AnimalDetailPage } from './pages/AnimalDetailPage'
import { LoginPage } from './pages/LoginPage'
import { RescatistaDashboardPage } from './pages/RescatistaDashboardPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { ProtectedRoute } from './components/ProtectedRoute'
import { RegisterPage } from './pages/RegisterPage'
import { AnimalFormPage } from './pages/AnimalFormPage'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<LandingPage />} />
        <Route path="/catalogo" element={<CatalogoPage />} />
        <Route path="/catalogo/:id" element={<AnimalDetailPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/registro" element={<RegisterPage />} />
        
        <Route element={<ProtectedRoute allowedRoles={['RESCATISTA']} />}>
          <Route path="/rescatista" element={<RescatistaDashboardPage />} />
          <Route path="/rescatista/animales/nuevo" element={<AnimalFormPage />} />
          <Route path="/rescatista/animales/:id/editar" element={<AnimalFormPage />} />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}

export default App