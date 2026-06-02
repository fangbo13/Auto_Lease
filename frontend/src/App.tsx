import { Routes, Route } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import Dashboard from './pages/Dashboard'
import ContractUpload from './pages/ContractUpload'
import ManualInput from './pages/ManualInput'
import CalculationResult from './pages/CalculationResult'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<ContractUpload />} />
          <Route path="/manual" element={<ManualInput />} />
          <Route path="/results/:id" element={<CalculationResult />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
