import { useState } from 'react'
import './App.css'
import { vocabService, generateService } from './services/api'
import VocabList from './components/VocabList'

function App() {
  const [currentSentence, setCurrentSentence] = useState({
    id: null,
    text: "¿Cómo estás?"
  })
  const [isLoading, setIsLoading] = useState(false)
  const [englishTranslation, setEnglishTranslation] = useState("")
  const [newVocabWord, setNewVocabWord] = useState("")

  const handleTranslationSubmit = (e) => {
    e.preventDefault()
    // TODO: Add validation logic here
    console.log("Submitted translation:", englishTranslation)
  }

  const handleGenerateClick = async () => {
    setIsLoading(true)
    try {
      const response = await generateService.generateSentence()
      setCurrentSentence({
        id: response.id,
        text: response.sentence
      })
    } catch (error) {
      console.error("Error generating sentence:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleVocabSubmit = async (e) => {
    e.preventDefault()
    try {
      console.log(newVocabWord)
      await vocabService.createVocabWord(newVocabWord)
      setNewVocabWord("")
    } catch (error) {
      console.error("Error adding vocab word:", error)
    }
  }

  return (
    <>
      <h1>Translation Practice</h1>
      <div className="translation-container">
        <h2>Translate this sentence:</h2>
        <div className="sentence-controls">
          <p className="spanish-text">{currentSentence.text}</p>
          <button 
            onClick={handleGenerateClick}
            disabled={isLoading}
            className="generate-btn"
          >
            {isLoading ? 'Generating...' : 'Generate New Sentence'}
          </button>
        </div>
        
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

      <VocabList />
    </>
  )
}

export default App
