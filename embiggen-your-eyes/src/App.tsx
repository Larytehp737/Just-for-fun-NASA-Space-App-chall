import { useState } from 'react'
import { ImageUploader } from './components/ImageUploader'

function App() {
  return (
    <main className="min-h-screen bg-background p-4 md:p-8">
      <div className="container mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center">
          Embiggen Your Eyes
        </h1>
        <ImageUploader />
      </div>
    </main>
  )
}

export default App