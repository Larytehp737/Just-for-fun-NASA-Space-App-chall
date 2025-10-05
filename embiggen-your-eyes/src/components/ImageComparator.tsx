import { useState } from 'react';
import { motion } from 'framer-motion';

interface ImageComparatorProps {
  originalImage: string;
  processedImage: string;
}

export const ImageComparator = ({ originalImage, processedImage }: ImageComparatorProps) => {
  const [sliderPosition, setSliderPosition] = useState(50);
  const [isDragging, setIsDragging] = useState(false);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!isDragging) return;
    
    const rect = e.currentTarget.getBoundingClientRect();
    const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
    setSliderPosition((x / rect.width) * 100);
  };

  return (
    <div 
      className="relative w-full aspect-video max-w-3xl mx-auto overflow-hidden rounded-lg"
      onMouseMove={handleMouseMove}
      onMouseDown={() => setIsDragging(true)}
      onMouseUp={() => setIsDragging(false)}
      onMouseLeave={() => setIsDragging(false)}
    >
      {/* Image originale */}
      <div className="absolute inset-0">
        <img 
          src={originalImage} 
          alt="Original"
          className="w-full h-full object-cover"
        />
      </div>

      {/* Image transformée */}
      <div 
        className="absolute inset-0"
        style={{ 
          clipPath: `polygon(0 0, ${sliderPosition}% 0, ${sliderPosition}% 100%, 0 100%)` 
        }}
      >
        <img 
          src={processedImage} 
          alt="Transformée"
          className="w-full h-full object-cover"
        />
      </div>

      {/* Slider */}
      <motion.div 
        className="absolute top-0 bottom-0"
        style={{ left: `${sliderPosition}%` }}
        whileHover={{ scale: 1.1 }}
        drag="x"
        dragConstraints={{ left: 0, right: 0 }}
      >
        <div className="w-1 h-full bg-white shadow-lg" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 bg-white rounded-full shadow-lg flex items-center justify-center">
          ⇄
        </div>
      </motion.div>
    </div>
  );
};