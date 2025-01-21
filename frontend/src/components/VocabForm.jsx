import { useState } from 'react'
import { vocabService } from '../services/api'

function VocabForm({ onVocabAdded }) {
  const [newVocabWord, setNewVocabWord] = useState("")

  const handleVocabSubmit = async (e) => {
    e.preventDefault()
    try {
      await vocabService.createVocabWord(newVocabWord)
      setNewVocabWord("")
      onVocabAdded()
    } catch (error) {
      console.error("Error adding vocab word:", error)
    }
  }

  return (
    <div className="vocab-container">
      <h2>Add New Vocabulary Word</h2>
      <form onSubmit={handleVocabSubmit} className="vocab-form">
        <div className="input-button-group">
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
        </div>
      </form>
    </div>
  )
}

export default VocabForm
