import { useState } from 'react'
import Student from './component/Student'
import Header from './component/Header'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Header />
      <Student />
    </>
  )
}

export default App
