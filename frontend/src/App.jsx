import { useState } from 'react'
import './App.css'

function App() {
  const [spanishSentence] = useState("¿Cómo estás?")
  const [englishTranslation, setEnglishTranslation] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    // TODO: Add validation logic here
    console.log("Submitted translation:", englishTranslation)
  }

  return (
    <>
      <h1>Translation Practice</h1>
      <div className="translation-container">
        <h2>Translate this sentence:</h2>
        <p className="spanish-text">{spanishSentence}</p>
        
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={englishTranslation}
            onChange={(e) => setEnglishTranslation(e.target.value)}
            placeholder="Enter English translation"
            className="translation-input"
          />
          <button type="submit" className="submit-btn">
            Check Translation
          </button>
        </form>
      </div>
    </>
  )
}

export default App
