import { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios';

function App() {
  const [message, setMessage] = useState(null);
  const [cityName, setCityName] = useState('');
  const [cities, setCities] = useState<Array<{id: number; name: string}>>([]);

  const fetchMessage = () => {
    axios.get('/api/message').then((r) => {
      setMessage(r.data)
    })
  }

  const loadCities = () => {
    axios.get('/api/cities').then((r) => setCities(r.data));
  }

  const addCity = async (e: React.FormEvent) => {
    e.preventDefault();
    const name = cityName.trim();
    if (!name) return;
    try {
      await axios.post('/api/cities', { name });
      setCityName('');
      loadCities();
    } catch {
      // можно вывести ошибку пользователю
    }
  }

  const removeCity = async (id: number) => {
    await axios.delete(`/api/cities/${id}`);
    loadCities();
  }

  useEffect(() => {
    fetchMessage();
    loadCities();
  }, [])

  return (
    <>
      <div>
        {message && message}
      </div>
      <hr />
      <form onSubmit={addCity}>
        <input
          placeholder="Город"
          value={cityName}
          onChange={(e) => setCityName(e.target.value)}
        />
        <button type="submit">Добавить</button>
      </form>
      <ul>
        {cities.map(c => (
          <li key={c.id}>
            {c.name}
            <button onClick={() => removeCity(c.id)} style={{ marginLeft: 8 }}>Удалить</button>
          </li>
        ))}
      </ul>
    </>
  )
}

export default App
