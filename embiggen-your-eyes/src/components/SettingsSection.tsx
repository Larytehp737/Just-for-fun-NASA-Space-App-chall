import { useState } from 'react';
import { motion } from 'framer-motion';
import { Eye, Type, Monitor, Volume2, Palette } from 'lucide-react';

interface SettingsSectionProps {
  onSettingsChange: (settings: Settings) => void;
  initialSettings?: Partial<Settings>;
}

interface Settings {
  fontSize: number;
  contrast: number;
  reducedMotion: boolean;
  highContrast: boolean;
  animationSpeed: number;
}

const defaultSettings: Settings = {
  fontSize: 16,
  contrast: 100,
  reducedMotion: false,
  highContrast: false,
  animationSpeed: 1,
};

export const SettingsSection = ({ 
  onSettingsChange,
  initialSettings = {}
}: SettingsSectionProps) => {
  const [settings, setSettings] = useState<Settings>({
    ...defaultSettings,
    ...initialSettings,
  });
  const [activeTab, setActiveTab] = useState('accessibility');

  const tabs = [
    { id: 'accessibility', label: 'Accessibilité', icon: <Eye size={20} /> },
    { id: 'display', label: 'Affichage', icon: <Monitor size={20} /> },
    { id: 'animations', label: 'Animations', icon: <Volume2 size={20} /> },
    { id: 'theme', label: 'Thème', icon: <Palette size={20} /> },
  ];

  const updateSetting = <K extends keyof Settings>(key: K, value: Settings[K]) => {
    const newSettings = { ...settings, [key]: value };
    setSettings(newSettings);
    onSettingsChange(newSettings);
  };

  return (
    <div className="bg-background rounded-lg shadow-lg p-6 max-w-2xl mx-auto">
      {/* Tabs */}
      <div className="flex space-x-2 mb-6 overflow-x-auto pb-2">
        {tabs.map((tab) => (
          <motion.button
            key={tab.id}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setActiveTab(tab.id)}
            className={`
              flex items-center space-x-2 px-4 py-2 rounded-lg
              ${activeTab === tab.id
                ? 'bg-primary text-primary-foreground'
                : 'hover:bg-foreground/10'}
            `}
          >
            {tab.icon}
            <span>{tab.label}</span>
          </motion.button>
        ))}
      </div>

      {/* Content */}
      <div className="space-y-6">
        {activeTab === 'accessibility' && (
          <>
            {/* Taille du texte */}
            <div className="space-y-2">
              <label className="flex items-center space-x-2">
                <Type size={20} />
                <span>Taille du texte</span>
              </label>
              <input
                type="range"
                min="12"
                max="24"
                value={settings.fontSize}
                onChange={(e) => updateSetting('fontSize', Number(e.target.value))}
                className="w-full"
              />
              <div className="flex justify-between text-sm text-foreground/60">
                <span>Petit</span>
                <span>{settings.fontSize}px</span>
                <span>Grand</span>
              </div>
            </div>

            {/* Contraste */}
            <div className="space-y-2">
              <label className="flex items-center space-x-2">
                <Monitor size={20} />
                <span>Contraste</span>
              </label>
              <input
                type="range"
                min="75"
                max="125"
                value={settings.contrast}
                onChange={(e) => updateSetting('contrast', Number(e.target.value))}
                className="w-full"
              />
            </div>

            {/* Options d'accessibilité */}
            <div className="space-y-2">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={settings.reducedMotion}
                  onChange={(e) => updateSetting('reducedMotion', e.target.checked)}
                  className="rounded border-foreground/20"
                />
                <span>Réduire les animations</span>
              </label>

              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={settings.highContrast}
                  onChange={(e) => updateSetting('highContrast', e.target.checked)}
                  className="rounded border-foreground/20"
                />
                <span>Mode contraste élevé</span>
              </label>
            </div>
          </>
        )}

        {activeTab === 'animations' && (
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="flex items-center space-x-2">
                <Volume2 size={20} />
                <span>Vitesse des animations</span>
              </label>
              <input
                type="range"
                min="0.5"
                max="2"
                step="0.1"
                value={settings.animationSpeed}
                onChange={(e) => updateSetting('animationSpeed', Number(e.target.value))}
                className="w-full"
              />
              <div className="flex justify-between text-sm text-foreground/60">
                <span>Lent</span>
                <span>{settings.animationSpeed}x</span>
                <span>Rapide</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};