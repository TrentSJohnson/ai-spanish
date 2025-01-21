import { useState } from 'react'
import { generateService } from '../services/api'

function TranslationSection() {
  const [currentSentence, setCurrentSentence] = useState({
    id: null,
    text: "¿Cómo estás?"
  })
  const [isLoading, setIsLoading] = useState(false)
  const [englishTranslation, setEnglishTranslation] = useState("")
  const [feedback, setFeedback] = useState({
    generalFeedback: "",
    vocabGrades: []
  })

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
      setFeedback({
        generalFeedback: response.feedback,
        vocabGrades: response.vocab_word_grades || []
      })
    } catch (error) {
      console.error("Error checking translation:", error)
      setFeedback({
        generalFeedback: "Error checking translation. Please try again.",
        vocabGrades: []
      })
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
        <div className="button-container">
          <button type="submit" className="submit-btn">
            Check Translation
          </button>
        </div>
      </form>
      
      {feedback.generalFeedback && (
        <div className="feedback-container">
          <p className="feedback-text">{feedback.generalFeedback}</p>
          {feedback.vocabGrades.length > 0 && (
            <div className="vocab-feedback">
              <h3>Vocabulary Usage:</h3>
              {feedback.vocabGrades.map((grade, index) => (
                <div key={index} className={`vocab-grade ${grade.is_correct ? 'correct' : 'incorrect'}`}>
                  <span className="vocab-word">{grade.vocab_word}</span>
                  <span className="vocab-feedback-text">{grade.feedback}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default TranslationSection
