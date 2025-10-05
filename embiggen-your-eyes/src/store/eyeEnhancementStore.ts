import { create } from 'zustand';

interface EyeEnhancementState {
  // État des images
  originalImage: string | null;
  processedImage: string | null;
  isProcessing: boolean;
  
  // Paramètres de traitement
  intensity: number;
  style: string;
  annotations: Annotation[];
  
  // Actions
  setOriginalImage: (image: string) => void;
  setProcessedImage: (image: string) => void;
  setIntensity: (value: number) => void;
  setStyle: (style: string) => void;
  addAnnotation: (annotation: Annotation) => void;
  updateAnnotation: (id: string, updates: Partial<Annotation>) => void;
  removeAnnotation: (id: string) => void;
  setProcessing: (status: boolean) => void;
}

interface Annotation {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  type: 'eye' | 'face';
  style?: string;
  intensity?: number;
}

const useEyeEnhancementStore = create<EyeEnhancementState>((set) => ({
  // État initial
  originalImage: null,
  processedImage: null,
  isProcessing: false,
  intensity: 50,
  style: 'natural',
  annotations: [],
  
  // Actions
  setOriginalImage: (image) => set({ originalImage: image }),
  setProcessedImage: (image) => set({ processedImage: image }),
  setIntensity: (value) => set({ intensity: value }),
  setStyle: (style) => set({ style }),
  
  addAnnotation: (annotation) => 
    set((state) => ({
      annotations: [...state.annotations, annotation]
    })),
    
  updateAnnotation: (id, updates) =>
    set((state) => ({
      annotations: state.annotations.map((ann) =>
        ann.id === id ? { ...ann, ...updates } : ann
      )
    })),
    
  removeAnnotation: (id) =>
    set((state) => ({
      annotations: state.annotations.filter((ann) => ann.id !== id)
    })),
    
  setProcessing: (status) => set({ isProcessing: status })
}));

export default useEyeEnhancementStore;