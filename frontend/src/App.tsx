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
import { HogaresTransitoPage } from './pages/HogaresTransitoPage'
import { HogarFormPage } from './pages/HogarFormPage'
import { SolicitudAdopcionFormPage } from './pages/SolicitudAdopcionFormPage'
import { MisSolicitudesPage } from './pages/MisSolicitudesPage'
import { SolicitudesRescatistaPage } from './pages/SolicitudesRescatistaPage'
import { AdopcionConfirmacionPage } from './pages/AdopcionConfirmacionPage'
import { SeguimientosRescatistaPage } from './pages/SeguimientosRescatistaPage'
import { SeguimientoFormPage } from './pages/SeguimientoFormPage'
import { EstadisticasPage } from './pages/EstadisticasPage'

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
          <Route path="/rescatista/hogares" element={<HogaresTransitoPage />} />
          <Route path="/rescatista/hogares/nuevo" element={<HogarFormPage />} />
          <Route path="/rescatista/hogares/:id/editar" element={<HogarFormPage />} />
          <Route path="/rescatista/solicitudes" element={<SolicitudesRescatistaPage />} />
          <Route path="/rescatista/seguimientos" element={<SeguimientosRescatistaPage />} />
          <Route path="/rescatista/adopciones/:adopcionId/seguimiento/nuevo" element={<SeguimientoFormPage />} />
          <Route path="/rescatista/estadisticas" element={<EstadisticasPage />} />
        </Route>

        <Route element={<ProtectedRoute />}>
          <Route path="/solicitudes/nueva/:animalId" element={<SolicitudAdopcionFormPage />} />
          <Route path="/mis-solicitudes" element={<MisSolicitudesPage />} />
          <Route path="/mis-solicitudes/:solicitudId/adopcion" element={<AdopcionConfirmacionPage />} />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}

export default App