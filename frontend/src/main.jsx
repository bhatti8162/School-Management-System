import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './Styles/App.css'
import './Styles/Dashboard.css'
import './Styles/Profile.css'
import './Styles/List.css'
import './Styles/Form.css'
// import './Styles/Family.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
