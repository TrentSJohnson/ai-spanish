import { useState, useEffect } from 'react';
import { vocabService } from '../services/api';

function VocabList({ onRefreshNeeded }) {
  const [vocabWords, setVocabWords] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadVocabWords = async () => {
    try {
      const words = await vocabService.getVocabWords();
      setVocabWords(words);
    } catch (error) {
      console.error("Error loading vocab words:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadVocabWords();
  }, [onRefreshNeeded]);

  const handleDelete = async (wordId) => {
    try {
      await vocabService.deleteVocabWord(wordId);
      await loadVocabWords(); // Refresh the list
    } catch (error) {
      console.error("Error deleting word:", error);
    }
  };

  if (isLoading) {
    return <div>Loading vocabulary...</div>;
  }

  return (
    <div className="vocab-list">
      <h2>Vocabulary Words</h2>
      {vocabWords.length === 0 ? (
        <p>No vocabulary words added yet.</p>
      ) : (
        <ul className="vocab-words">
          {vocabWords.map((word) => (
            <li key={word.id} className="vocab-word-item">
              <span>{word.word}</span>
              <button 
                onClick={() => handleDelete(word.id)}
                className="delete-btn"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default VocabList;
