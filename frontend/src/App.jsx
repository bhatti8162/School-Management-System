import { useState } from 'react'
import Dashboard from './component/Dashboard'
import Header from './component/Header'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      {/* <Header /> */}
      <Dashboard />
    </>
  )
}

export default App
