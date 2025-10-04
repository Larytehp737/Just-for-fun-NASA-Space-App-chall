import { useState } from 'react';

interface AccessibilityControlsProps {
  onFontSizeChange: (size: number) => void;
  onContrastChange: (high: boolean) => void;
  onReduceMotion: (reduce: boolean) => void;
}

export const AccessibilityControls = ({
  onFontSizeChange,
  onContrastChange,
  onReduceMotion
}: AccessibilityControlsProps) => {
  const [fontSize, setFontSize] = useState(16);
  const [highContrast, setHighContrast] = useState(false);
  const [reduceMotion, setReduceMotion] = useState(false);

  const handleFontSizeChange = (newSize: number) => {
    setFontSize(newSize);
    onFontSizeChange(newSize);
  };

  const handleContrastChange = (value: boolean) => {
    setHighContrast(value);
    onContrastChange(value);
  };

  const handleMotionChange = (value: boolean) => {
    setReduceMotion(value);
    onReduceMotion(value);
  };

  return (
    <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
      <h2 className="text-lg font-medium">Paramètres d'accessibilité</h2>

      {/* Taille du texte */}
      <div>
        <label className="block text-sm text-gray-700">Taille du texte</label>
        <div className="flex items-center space-x-4 mt-2">
          <button
            onClick={() => handleFontSizeChange(14)}
            className={`px-3 py-1 rounded ${
              fontSize === 14 ? 'bg-primary text-white' : 'bg-gray-200'
            }`}
          >
            A
          </button>
          <button
            onClick={() => handleFontSizeChange(16)}
            className={`px-3 py-1 rounded ${
              fontSize === 16 ? 'bg-primary text-white' : 'bg-gray-200'
            }`}
          >
            AA
          </button>
          <button
            onClick={() => handleFontSizeChange(18)}
            className={`px-3 py-1 rounded ${
              fontSize === 18 ? 'bg-primary text-white' : 'bg-gray-200'
            }`}
          >
            AAA
          </button>
        </div>
      </div>

      {/* Contraste */}
      <div>
        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            checked={highContrast}
            onChange={(e) => handleContrastChange(e.target.checked)}
            className="rounded border-gray-300 text-primary focus:ring-primary"
          />
          <span className="text-sm text-gray-700">
            Mode contraste élevé
          </span>
        </label>
      </div>

      {/* Réduction des animations */}
      <div>
        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            checked={reduceMotion}
            onChange={(e) => handleMotionChange(e.target.checked)}
            className="rounded border-gray-300 text-primary focus:ring-primary"
          />
          <span className="text-sm text-gray-700">
            Réduire les animations
          </span>
        </label>
      </div>
    </div>
  );
};