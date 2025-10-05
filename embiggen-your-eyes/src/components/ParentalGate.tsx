import { useEffect, useMemo, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';

interface ParentalGateProps {
  open: boolean;
  onClose: () => void;
  onPassed: () => void;
}

// Very simple math gate suitable as a minimal parental confirmation
export const ParentalGate = ({ open, onClose, onPassed }: ParentalGateProps) => {
  const [answer, setAnswer] = useState('');
  const [error, setError] = useState<string | null>(null);

  const challenge = useMemo(() => {
    const a = Math.floor(5 + Math.random() * 5); // 5..9
    const b = Math.floor(5 + Math.random() * 5); // 5..9
    return { a, b, sum: a + b };
  }, [open]);

  useEffect(() => {
    if (!open) {
      setAnswer('');
      setError(null);
    }
  }, [open]);

  const verify = () => {
    if (parseInt(answer, 10) === challenge.sum) {
      onPassed();
      setAnswer('');
      setError(null);
    } else {
      setError('Oups, ce n\'est pas la bonne réponse. Réessaie.');
    }
  };

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="exit-dialog"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          role="dialog"
          aria-modal="true"
          aria-labelledby="parental-gate-title"
        >
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="exit-dialog-content"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 id="parental-gate-title" className="text-lg font-semibold">Vérification adulte</h2>
              <button className="p-2 rounded-md hover:bg-foreground/10" onClick={onClose} aria-label="Fermer">
                <X className="h-5 w-5" />
              </button>
            </div>
            <p className="text-sm text-foreground/80 mb-4">
              Pour quitter le Mode Enfants, un adulte doit résoudre ce petit calcul.
            </p>

            <div className="flex items-center gap-2 mb-3">
              <span className="text-xl font-bold" aria-live="polite">{challenge.a} + {challenge.b} =</span>
              <input
                className="input w-24 text-center text-xl"
                inputMode="numeric"
                aria-label="Réponse au calcul"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
              />
            </div>
            {error && <p className="text-sm text-destructive mb-3">{error}</p>}

            <div className="flex justify-end gap-2">
              <button className="btn btn-secondary" onClick={onClose}>Annuler</button>
              <button className="btn btn-primary" onClick={verify}>Valider</button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
