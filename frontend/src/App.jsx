import { useState } from 'react'
import './App.css'
import VocabList from './components/VocabList'
import TranslationSection from './components/TranslationSection'
import VocabForm from './components/VocabForm'

function App() {
  const [refreshVocabTrigger, setRefreshVocabTrigger] = useState(0)

  const handleVocabAdded = () => {
    setRefreshVocabTrigger(prev => prev + 1)
  }

  return (
    <>
      <h1>Translation Practice</h1>
      <TranslationSection />
      <VocabForm onVocabAdded={handleVocabAdded} />
      <VocabList onRefreshNeeded={refreshVocabTrigger} />
    </>
  )
}

export default App
