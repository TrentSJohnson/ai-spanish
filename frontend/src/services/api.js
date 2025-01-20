import axios from 'axios';

const API_URL = 'http://localhost:8000';
const API_PREFIX = '/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const vocabService = {
  createVocabWord: async (word) => {
    const response = await api.post(`${API_PREFIX}/vocab/words`, null, { params: { word } });
    return response.data;
  },
  
  getVocabWords: async () => {
    const response = await api.get(`${API_PREFIX}/vocab/words`);
    return response.data;
  },
};

export const generateService = {
  generateSentence: async (vocabWordIds = null) => {
    const response = await api.post(`${API_PREFIX}/generate/sentence`, { vocab_word_ids: vocabWordIds });
    return response.data;
  },

  checkSentence: async (sentenceId, translation) => {
    const response = await api.post(`${API_PREFIX}/generate/check`, {
      sentence_id: sentenceId,
      translation: translation
    });
    return response.data;
  },
};
