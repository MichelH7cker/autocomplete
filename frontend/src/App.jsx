import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="bg-slate-100 min-h-screen flex flex-col items-center pt-10 px-4">
      <div className="w-full max-w-xl">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-slate-800">Busca com autocompletar</h1>
          <p className="text-slate-600 mt-2">Encontre sugestões enquanto digita. Digite no campo abaixo</p>
        </header>

        <main className="relative">
          oi 
        </main>
      </div>
    </div>
  )
}

export default App
