import { useState } from 'react';
import { Menu, X, Eye, Settings, Image, Download, Moon, Sun, Smile } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useUserPreferences } from '../store/userPreferences';
import { ParentalGate } from './ParentalGate';

interface NavbarProps {
  onThemeToggle: () => void;
  isDarkMode: boolean;
}

export const Navbar = ({ onThemeToggle, isDarkMode }: NavbarProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [askGate, setAskGate] = useState(false);
  const { settings, updateSettings } = useUserPreferences();
  const kidsOn = settings.kidsMode;

  const toggleKids = () => {
    if (kidsOn) {
      // Leaving kids mode requires parental gate
      setAskGate(true);
    } else {
      updateSettings({ kidsMode: true });
      // update URL param
      const url = new URL(window.location.href);
      url.searchParams.set('kids', '1');
      window.history.replaceState({}, '', url.toString());
    }
  };

  const menuItems = [
    { icon: <Eye size={20} />, label: 'Améliorer', href: '#enhance' },
    { icon: <Image size={20} />, label: 'Galerie', href: '#gallery' },
    { icon: <Settings size={20} />, label: 'Paramètres', href: '#settings' },
    { icon: <Download size={20} />, label: 'Exporter', href: '#export' },
  ];

  return (
    <nav className="fixed top-0 w-full bg-background/80 backdrop-blur-sm border-b border-border z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex-shrink-0 font-bold text-xl text-primary"
          >
            Embiggen Eyes
          </motion.div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-4">
            {menuItems.map((item) => (
              <motion.a
                key={item.label}
                href={item.href}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center space-x-2 text-foreground/80 hover:text-primary transition-colors"
              >
                {item.icon}
                <span>{item.label}</span>
              </motion.a>
            ))}

            {/* Kids Mode toggle */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={toggleKids}
              className={`px-3 py-2 rounded-full flex items-center gap-2 ${kidsOn ? 'bg-accent text-accent-foreground' : 'hover:bg-foreground/10'}`}
              aria-pressed={kidsOn}
              aria-label="Activer le Mode Enfants"
              title={kidsOn ? 'Mode Enfants activé' : 'Activer le Mode Enfants'}
            >
              <Smile size={18} />
              <span className="text-sm font-semibold hidden lg:inline">Mode Enfants</span>
            </motion.button>
            
            {/* Theme Toggle */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onThemeToggle}
              className="p-2 rounded-full hover:bg-foreground/10"
            >
              {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
            </motion.button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center gap-2">
            <button
              onClick={toggleKids}
              className={`p-2 rounded-full ${kidsOn ? 'bg-accent text-accent-foreground' : 'hover:bg-foreground/10'}`}
              aria-pressed={kidsOn}
              aria-label="Basculer Mode Enfants"
            >
              <Smile size={20} />
            </button>
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 rounded-md hover:bg-foreground/10"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden border-t border-border"
          >
            <div className="px-2 pt-2 pb-3 space-y-1">
              {menuItems.map((item) => (
                <a
                  key={item.label}
                  href={item.href}
                  className="flex items-center space-x-2 px-3 py-2 rounded-md text-foreground/80 hover:text-primary hover:bg-foreground/10"
                  onClick={() => setIsOpen(false)}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </a>
              ))}
              
              <button
                onClick={() => {
                  onThemeToggle();
                  setIsOpen(false);
                }}
                className="flex items-center space-x-2 w-full px-3 py-2 rounded-md text-foreground/80 hover:text-primary hover:bg-foreground/10"
              >
                {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
                <span>Thème {isDarkMode ? 'Clair' : 'Sombre'}</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Parental Gate */}
      <ParentalGate
        open={askGate}
        onClose={() => setAskGate(false)}
        onPassed={() => {
          updateSettings({ kidsMode: false });
          const url = new URL(window.location.href);
          url.searchParams.delete('kids');
          window.history.replaceState({}, '', url.toString());
          setAskGate(false);
        }}
      />
    </nav>
  );
};