import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { Upload } from 'lucide-react'

export const ImageUploader = () => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    // TODO: Handle file upload
    console.log(acceptedFiles)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif']
    }
  })

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className="w-full max-w-2xl mx-auto"
    >
      <div
        {...getRootProps()}
        className={`
          p-8 border-2 border-dashed rounded-lg 
          flex flex-col items-center justify-center
          min-h-[300px] cursor-pointer
          transition-colors duration-200
          ${isDragActive ? 'border-primary bg-secondary/50' : 'border-border'}
        `}
      >
        <input {...getInputProps()} />
        <Upload size={40} className="mb-4 text-muted-foreground" />
        {isDragActive ? (
          <p className="text-lg text-center text-muted-foreground">
            Déposez l'image ici...
          </p>
        ) : (
          <div className="text-center">
            <p className="text-lg mb-2 text-muted-foreground">
              Glissez-déposez une image ici, ou cliquez pour sélectionner
            </p>
            <p className="text-sm text-muted-foreground">
              PNG, JPG ou GIF (max 10MB)
            </p>
          </div>
        )}
      </div>
    </motion.div>
  )
}