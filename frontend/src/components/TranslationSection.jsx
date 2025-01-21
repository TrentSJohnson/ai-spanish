import { useState } from 'react'
import { generateService } from '../services/api'

function TranslationSection() {
  const [currentSentence, setCurrentSentence] = useState({
    id: null,
    text: "¿Cómo estás?"
  })
  const [isLoading, setIsLoading] = useState(false)
  const [englishTranslation, setEnglishTranslation] = useState("")
  const [feedback, setFeedback] = useState("")

  const handleTranslationSubmit = async (e) => {
    e.preventDefault()
    if (!currentSentence.id || !englishTranslation.trim()) {
      return
    }
    
    try {
      const response = await generateService.checkSentence(
        currentSentence.id, 
        englishTranslation
      )
      setFeedback(response.result)
    } catch (error) {
      console.error("Error checking translation:", error)
      setFeedback("Error checking translation. Please try again.")
    }
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

  return (
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
      
      <form onSubmit={handleTranslationSubmit} className="translation-form">
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
      
      {feedback && (
        <div className="feedback-container">
          <p className="feedback-text">{feedback}</p>
        </div>
      )}
    </div>
  )
}

export default TranslationSection
