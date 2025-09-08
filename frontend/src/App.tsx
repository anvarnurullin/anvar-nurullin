import { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios';

function App() {
  const [message, setMessage] = useState(null);
  const fetchMessage = () => {
    axios.get('/api/message').then((r) => {
      setMessage(r.data)
    })
  }
  useEffect(() => {
    fetchMessage()
  }, [])

  return (
    <>
      <div>
        {message && message}
      </div>
    </>
  )
}

export default App
