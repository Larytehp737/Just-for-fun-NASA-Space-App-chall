'use client';

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ImageUploader } from './components/ImageUploader'
import { Navbar } from './components/Navbar'
import { Upload, Sparkles, Eye } from 'lucide-react'

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false)

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode)
    document.documentElement.classList.toggle('dark')
  }

  return (
    <div className={`min-h-screen ${isDarkMode ? 'dark' : ''}`}>
      <div className="min-h-screen bg-background transition-colors duration-200">
        <Navbar onThemeToggle={toggleTheme} isDarkMode={isDarkMode} />
        <main className="pt-16 min-h-[calc(100vh-4rem)] bg-gradient-to-b from-background via-background/95 to-background/90 p-4 md:p-8">
          <div className="container mx-auto max-w-7xl">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="text-center space-y-6 mb-16"
            >
              <h1 className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-accent to-accent-foreground">
                Embiggen Your Eyes
              </h1>
              <p className="text-xl text-foreground/80 max-w-2xl mx-auto">
                Transformez vos photos en leur donnant un regard captivant et expressif grâce à notre technologie d'amélioration des yeux alimentée par l'IA.
              </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="card hover:border-accent/50"
              >
                <Upload className="w-12 h-12 mb-4 text-accent" />
                <h2 className="text-xl font-semibold mb-2">Upload Simple</h2>
                <p className="text-foreground/60">
                  Glissez-déposez vos images ou sélectionnez-les depuis votre appareil. Prise en charge de plusieurs formats.
                </p>
              </motion.div>
              
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="card hover:border-accent/50"
              >
                <Eye className="w-12 h-12 mb-4 text-accent" />
                <h2 className="text-xl font-semibold mb-2">Personnalisation</h2>
                <p className="text-foreground/60">
                  Ajustez la taille, la forme et l'expression des yeux selon vos préférences avec des contrôles intuitifs.
                </p>
              </motion.div>
              
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="card hover:border-accent/50"
              >
                <Sparkles className="w-12 h-12 mb-4 text-accent" />
                <h2 className="text-xl font-semibold mb-2">Résultats Instantanés</h2>
                <p className="text-foreground/60">
                  Visualisez les changements en temps réel et comparez facilement l'avant/après de vos modifications.
                </p>
              </motion.div>
            </div>

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5 }}
              className="max-w-4xl mx-auto"
            >
              <div className="text-center mb-8">
                <h2 className="text-2xl font-semibold mb-2">Commencez dès maintenant</h2>
                <p className="text-foreground/60">
                  Importez une photo pour découvrir la magie de l'amélioration des yeux
                </p>
              </div>
              <ImageUploader onImageUpload={(file: File) => console.log('Image uploadée:', file)} />
            </motion.div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default App