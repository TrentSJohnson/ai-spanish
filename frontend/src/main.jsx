import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import KeycloakProvider from './components/KeycloakProvider'

createRoot(document.getElementById('root')).render(
  <KeycloakProvider>
    <App />
  </KeycloakProvider>
)
