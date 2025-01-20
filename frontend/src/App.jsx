import { useState } from 'react'
import './App.css'

function App() {
  const [spanishSentence] = useState("¿Cómo estás?")
  const [englishTranslation, setEnglishTranslation] = useState("")
  const [newVocabWord, setNewVocabWord] = useState("")

  const handleTranslationSubmit = (e) => {
    e.preventDefault()
    // TODO: Add validation logic here
    console.log("Submitted translation:", englishTranslation)
  }

  const handleVocabSubmit = (e) => {
    e.preventDefault()
    console.log("Submitted vocab word:", newVocabWord)
    setNewVocabWord("")
  }

  return (
    <>
      <h1>Translation Practice</h1>
      <div className="vocab-container">
        <h2>Add New Vocabulary Word</h2>
        <form onSubmit={handleVocabSubmit}>
          <input
            type="text"
            value={newVocabWord}
            onChange={(e) => setNewVocabWord(e.target.value)}
            placeholder="Enter new Spanish word"
            className="vocab-input"
          />
          <button type="submit" className="submit-btn">
            Add Word
          </button>
        </form>
      </div>
      
      <div className="translation-container">
        <h2>Translate this sentence:</h2>
        <p className="spanish-text">{spanishSentence}</p>
        
        <form onSubmit={handleTranslationSubmit}>
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
