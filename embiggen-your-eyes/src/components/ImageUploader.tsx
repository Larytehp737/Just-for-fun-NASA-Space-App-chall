'use client';

import { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, X } from 'lucide-react';

interface ImageUploaderProps {
  onImageUpload: (file: File) => void;
  maxSize?: number; // en MB
}

export function ImageUploader({ onImageUpload, maxSize = 10 }: ImageUploaderProps) {
  const [error, setError] = useState<string | null>(null);
  const [preview, setPreview] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      if (file.size > maxSize * 1024 * 1024) {
        setError(`L'image doit faire moins de ${maxSize}MB`);
        return;
      }

      const objectUrl = URL.createObjectURL(file);
      setPreview(objectUrl);
      onImageUpload(file);
      setError(null);
    }
  }, [maxSize, onImageUpload]);

  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragReject
  } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': [],
      'image/png': [],
      'image/webp': [],
      'image/avif': []
    },
    multiple: false,
    maxSize: maxSize * 1024 * 1024
  });

  useEffect(() => {
    return () => {
      if (preview) {
        URL.revokeObjectURL(preview);
      }
    };
  }, [preview]);

  return (
    <div className="w-full max-w-2xl mx-auto">
      <AnimatePresence>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="space-y-4"
        >
          <div
            className={`
              relative p-8 border-2 border-dashed rounded-lg
              bg-background/50 backdrop-blur-sm
              transition-colors duration-200
              ${isDragActive ? 'border-accent bg-accent/5' : 'border-border hover:border-accent/50'}
              ${isDragReject ? 'border-destructive bg-destructive/5' : ''}
              ${error ? 'border-destructive bg-destructive/5' : ''}
            `}
            style={{ minHeight: '300px' }}
            {...getRootProps()}
          >
            <input {...getInputProps()} />
            {preview ? (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="absolute inset-0 bg-black/50 backdrop-blur-sm rounded-lg flex items-center justify-center"
              >
                <img
                  src={preview}
                  alt="Prévisualisation"
                  className="max-h-[250px] w-auto object-contain rounded-lg"
                />
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setPreview(null);
                  }}
                  className="absolute top-2 right-2 p-1 rounded-full bg-background/20 hover:bg-background/40 transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </motion.div>
            ) : (
              <div className="text-center space-y-4">
                <div className="flex flex-col items-center justify-center gap-2">
                  <Upload className="h-12 w-12 text-foreground/60" />
                  <p className="text-xl font-semibold">
                    {isDragActive
                      ? "Déposez l'image ici"
                      : "Glissez-déposez une image ou cliquez pour en sélectionner une"}
                  </p>
                </div>
                <p className="text-sm text-foreground/60">
                  Formats supportés: JPEG, PNG, WebP, AVIF
                </p>
                {error && (
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-sm text-destructive font-medium"
                  >
                    {error}
                  </motion.p>
                )}
              </div>
            )}
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}