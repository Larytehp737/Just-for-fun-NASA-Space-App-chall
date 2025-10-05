import { Slider } from '@radix-ui/react-slider';
import { motion } from 'framer-motion';

interface EyeControlsProps {
  intensity: number;
  onIntensityChange: (value: number) => void;
  style: string;
  onStyleChange: (style: string) => void;
}

export const EyeControls = ({
  intensity,
  onIntensityChange,
  style,
  onStyleChange
}: EyeControlsProps) => {
  return (
    <div className="w-full max-w-md mx-auto space-y-6 p-4">
      {/* Contrôle de l'intensité */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          Intensité de l'effet
        </label>
        <Slider
          value={[intensity]}
          onValueChange={(values) => onIntensityChange(values[0])}
          min={0}
          max={100}
          step={1}
          className="w-full"
        />
      </div>

      {/* Sélection du style */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          Style visuel
        </label>
        <div className="grid grid-cols-3 gap-2">
          {['naturel', 'anime', 'surréaliste'].map((styleOption) => (
            <motion.button
              key={styleOption}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => onStyleChange(styleOption)}
              className={`
                px-4 py-2 rounded-lg text-sm font-medium
                ${style === styleOption
                  ? 'bg-primary text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }
              `}
            >
              {styleOption}
            </motion.button>
          ))}
        </div>
      </div>
    </div>
  );
};