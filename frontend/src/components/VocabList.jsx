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
      <style>
        {`
          .vocab-word-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            border-bottom: 1px solid #333;
            margin: 10px 0;
            background: #242424;
            border-radius: 8px;
          }
          .word-text {
            font-weight: bold;
            min-width: 150px;
            text-align: left;
            font-size: 1.1em;
          }
          .word-stats {
            display: flex;
            gap: 40px;
            color: #999;
            flex-grow: 1;
            justify-content: center;
          }
          .delete-btn {
            padding: 5px 10px;
            background: #ff4444;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
          }
          .delete-btn:hover {
            background: #cc0000;
          }
        `}
      </style>
      <h2>Vocabulary Words</h2>
      {vocabWords.length === 0 ? (
        <p>No vocabulary words added yet.</p>
      ) : (
        <ul className="vocab-words">
          {vocabWords
            .sort((a, b) => b.score - a.score)
            .map((word) => (
              <li key={word.id} className="vocab-word-item">
                <span className="word-text">{word.word}</span>
                <div className="word-stats">
                  <span>Score: {word.score}</span>
                  <span>Guesses: {word.guesses}</span>
                  <span>Correct: {word.correct}</span>
                </div>
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
