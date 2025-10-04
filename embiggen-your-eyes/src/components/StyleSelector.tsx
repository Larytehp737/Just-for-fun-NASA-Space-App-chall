import { useState } from 'react';
import { motion } from 'framer-motion';

interface StyleOption {
  id: string;
  name: string;
  preview: string;
  description: string;
}

const styles: StyleOption[] = [
  {
    id: 'natural',
    name: 'Naturel',
    preview: '/styles/natural.jpg',
    description: 'Amélioration subtile et réaliste'
  },
  {
    id: 'anime',
    name: 'Anime',
    preview: '/styles/anime.jpg',
    description: 'Style manga japonais expressif'
  },
  {
    id: 'surreal',
    name: 'Surréaliste',
    preview: '/styles/surreal.jpg',
    description: 'Effet artistique dramatique'
  },
  {
    id: 'cyberpunk',
    name: 'Cyberpunk',
    preview: '/styles/cyber.jpg',
    description: 'Look futuriste et néon'
  }
];

interface StyleSelectorProps {
  selectedStyle: string;
  onStyleSelect: (styleId: string) => void;
}

export const StyleSelector = ({ selectedStyle, onStyleSelect }: StyleSelectorProps) => {
  const [hoveredStyle, setHoveredStyle] = useState<string | null>(null);

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4">
      {styles.map((style) => (
        <motion.div
          key={style.id}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className={`
            relative cursor-pointer rounded-lg overflow-hidden
            ${selectedStyle === style.id ? 'ring-2 ring-primary ring-offset-2' : ''}
          `}
          onMouseEnter={() => setHoveredStyle(style.id)}
          onMouseLeave={() => setHoveredStyle(null)}
          onClick={() => onStyleSelect(style.id)}
        >
          <img
            src={style.preview}
            alt={style.name}
            className="w-full aspect-square object-cover"
          />
          
          {/* Info overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: hoveredStyle === style.id ? 1 : 0 }}
            className="absolute inset-0 bg-black/50 p-4 flex flex-col justify-end"
          >
            <h3 className="text-white font-medium">{style.name}</h3>
            <p className="text-white/80 text-sm">{style.description}</p>
          </motion.div>
        </motion.div>
      ))}
    </div>
  );
};