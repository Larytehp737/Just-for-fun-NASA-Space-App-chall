import { motion } from 'framer-motion';
import { Sparkles, Camera, Palette, Wand2 } from 'lucide-react';

interface StyleCard {
  id: string;
  name: string;
  description: string;
  icon: JSX.Element;
  preview: string;
}

const styles: StyleCard[] = [
  {
    id: 'natural',
    name: 'Naturel',
    description: 'Amélioration subtile et réaliste des yeux',
    icon: <Camera className="w-6 h-6" />,
    preview: '/styles/natural.jpg'
  },
  {
    id: 'anime',
    name: 'Anime',
    description: 'Style manga expressif et dynamique',
    icon: <Sparkles className="w-6 h-6" />,
    preview: '/styles/anime.jpg'
  },
  {
    id: 'surreal',
    name: 'Surréaliste',
    description: 'Effets artistiques dramatiques',
    icon: <Palette className="w-6 h-6" />,
    preview: '/styles/surreal.jpg'
  },
  {
    id: 'fantasy',
    name: 'Fantaisie',
    description: 'Effets magiques et enchanteurs',
    icon: <Wand2 className="w-6 h-6" />,
    preview: '/styles/fantasy.jpg'
  }
];

interface StyleGridProps {
  onStyleSelect: (style: string) => void;
  selectedStyle: string;
}

export const StyleGrid = ({ onStyleSelect, selectedStyle }: StyleGridProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 p-6">
      {styles.map((style) => (
        <motion.div
          key={style.id}
          whileHover={{ y: -5 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => onStyleSelect(style.id)}
          className={`
            relative overflow-hidden rounded-xl cursor-pointer
            border-2 transition-colors duration-200
            ${selectedStyle === style.id 
              ? 'border-primary shadow-lg' 
              : 'border-border hover:border-primary/50'}
          `}
        >
          {/* Preview Image */}
          <div className="relative aspect-square">
            <img
              src={style.preview}
              alt={style.name}
              className="object-cover w-full h-full"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent" />
          </div>

          {/* Content */}
          <div className="absolute bottom-0 left-0 right-0 p-4">
            <div className="flex items-center space-x-2 mb-2">
              {style.icon}
              <h3 className="font-medium text-lg">{style.name}</h3>
            </div>
            <p className="text-sm text-foreground/80">{style.description}</p>
          </div>

          {/* Selected Indicator */}
          {selectedStyle === style.id && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="absolute top-2 right-2 w-6 h-6 bg-primary rounded-full flex items-center justify-center"
            >
              <svg
                className="w-4 h-4 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </motion.div>
          )}
        </motion.div>
      ))}
    </div>
  );
};