import { motion } from 'framer-motion';
import { Search, ZoomIn, Pencil } from 'lucide-react';

interface KidsToolbarProps {
  onZoom?: () => void;
  onExplore?: () => void;
  onNote?: () => void;
}

export const KidsToolbar = ({ onZoom, onExplore, onNote }: KidsToolbarProps) => {
  const Button = ({ icon, label, onClick }: { icon: JSX.Element; label: string; onClick?: () => void }) => (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className="kids-tool"
      aria-label={label}
    >
      {icon}
      <span>{label}</span>
    </motion.button>
  );

  return (
    <div className="kids-tools-container">
      <Button icon={<ZoomIn className="w-7 h-7" />} label="Zoomer" onClick={onZoom} />
      <Button icon={<Search className="w-7 h-7" />} label="Explorer" onClick={onExplore} />
      <Button icon={<Pencil className="w-7 h-7" />} label="Noter" onClick={onNote} />
    </div>
  );
};
