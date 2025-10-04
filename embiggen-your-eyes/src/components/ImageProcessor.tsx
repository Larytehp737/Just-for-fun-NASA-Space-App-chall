import { useState, useCallback } from 'react';
import { ImageUploader } from './ImageUploader';
import { ImageComparator } from './ImageComparator';
import { EyeControls } from './EyeControls';
import { StyleSelector } from './StyleSelector';

interface ProcessedImage {
  url: string;
  style: string;
  intensity: number;
}

export const ImageProcessor = () => {
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [processedImage, setProcessedImage] = useState<ProcessedImage | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  // Simule le traitement d'image (à remplacer par l'API réelle)
  const processImage = useCallback(async (
    imageUrl: string,
    style: string,
    intensity: number
  ) => {
    setIsProcessing(true);
    
    try {
      // Simulation d'un appel API
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Pour la démo, on renvoie la même image
      setProcessedImage({
        url: imageUrl,
        style,
        intensity
      });
    } catch (error) {
      console.error('Erreur lors du traitement:', error);
    } finally {
      setIsProcessing(false);
    }
  }, []);

  // Gestion de l'upload d'image
  const handleImageUpload = async (file: File) => {
    const imageUrl = URL.createObjectURL(file);
    setOriginalImage(imageUrl);
    
    // Lance le traitement initial
    await processImage(imageUrl, 'natural', 50);
  };

  // Gestion des changements de style
  const handleStyleChange = async (style: string) => {
    if (!originalImage || !processedImage) return;
    
    await processImage(
      originalImage,
      style,
      processedImage.intensity
    );
  };

  // Gestion des changements d'intensité
  const handleIntensityChange = async (intensity: number) => {
    if (!originalImage || !processedImage) return;
    
    await processImage(
      originalImage,
      processedImage.style,
      intensity
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-8">
      {!originalImage ? (
        <ImageUploader onImageUpload={handleImageUpload} />
      ) : (
        <>
          <ImageComparator
            originalImage={originalImage}
            processedImage={processedImage?.url || originalImage}
          />
          
          <div className="space-y-6">
            <StyleSelector
              selectedStyle={processedImage?.style || 'natural'}
              onStyleSelect={handleStyleChange}
            />
            
            <EyeControls
              intensity={processedImage?.intensity || 50}
              onIntensityChange={handleIntensityChange}
              style={processedImage?.style || 'natural'}
              onStyleChange={handleStyleChange}
            />
          </div>

          {isProcessing && (
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
              <div className="bg-white p-4 rounded-lg">
                Traitement en cours...
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};