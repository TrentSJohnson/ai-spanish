import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const vocabService = {
  createVocabWord: async (word) => {
    const response = await api.post('/vocab/words', null, { params: { word } });
    return response.data;
  },
  
  getVocabWords: async () => {
    const response = await api.get('/vocab/words');
    return response.data;
  },
};

export const translationService = {
  generateSentence: async (vocabWordIds = null) => {
    const response = await api.post('/generate/sentence', { vocab_word_ids: vocabWordIds });
    return response.data;
  },

  checkTranslation: async (sentenceId, translation) => {
    const response = await api.post('/generate/check', {
      sentence_id: sentenceId,
      translation: translation
    });
    return response.data;
  },
};
