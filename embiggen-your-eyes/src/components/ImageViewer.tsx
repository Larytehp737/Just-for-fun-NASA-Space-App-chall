import OpenSeadragon from 'openseadragon';
import { useEffect, useRef } from 'react';

interface ImageViewerProps {
  image: string;
  annotations?: Annotation[];
  onAnnotationAdd?: (annotation: Annotation) => void;
  onAnnotationUpdate?: (annotation: Annotation) => void;
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

export const ImageViewer = ({ 
  image, 
  annotations = [],
  onAnnotationAdd,
  onAnnotationUpdate 
}: ImageViewerProps) => {
  const viewerRef = useRef<OpenSeadragon.Viewer | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Initialisation du viewer OpenSeadragon
    viewerRef.current = OpenSeadragon({
      element: containerRef.current,
      tileSources: {
        type: 'image',
        url: image
      },
      showNavigationControl: true,
      showRotationControl: true,
      gestureSettingsMouse: {
        clickToZoom: false,
        dblClickToZoom: true
      },
      debugMode: false
    });

    // Ajout des overlays pour les annotations
    const viewer = viewerRef.current;
    
    annotations.forEach(annotation => {
      const element = document.createElement('div');
      element.className = 'annotation-overlay';
      element.dataset.id = annotation.id;
      
      viewer.addOverlay({
        element,
        location: new OpenSeadragon.Rect(
          annotation.x,
          annotation.y,
          annotation.width,
          annotation.height
        )
      });
    });

    return () => {
      viewer.destroy();
    };
  }, [image]);

  // Mise à jour des annotations
  useEffect(() => {
    if (!viewerRef.current) return;

    const viewer = viewerRef.current;
    
    // Supprime les anciens overlays
    viewer.clearOverlays();
    
    // Ajoute les nouveaux
    annotations.forEach(annotation => {
      const element = document.createElement('div');
      element.className = `annotation-overlay ${annotation.type}`;
      element.dataset.id = annotation.id;
      
      viewer.addOverlay({
        element,
        location: new OpenSeadragon.Rect(
          annotation.x,
          annotation.y,
          annotation.width,
          annotation.height
        )
      });
    });
  }, [annotations]);

  return (
    <div className="relative w-full aspect-video">
      <div ref={containerRef} className="absolute inset-0" />
      
      {/* Contrôles d'annotation */}
      <div className="absolute top-4 right-4 space-x-2">
        <button
          className="px-3 py-1 bg-primary text-white rounded-md text-sm"
          onClick={() => onAnnotationAdd?.({
            id: Math.random().toString(),
            x: 0.5,
            y: 0.5,
            width: 0.1,
            height: 0.1,
            type: 'eye'
          })}
        >
          + Ajouter yeux
        </button>
        <button
          className="px-3 py-1 bg-primary text-white rounded-md text-sm"
          onClick={() => onAnnotationAdd?.({
            id: Math.random().toString(),
            x: 0.4,
            y: 0.4,
            width: 0.2,
            height: 0.3,
            type: 'face'
          })}
        >
          + Ajouter visage
        </button>
      </div>
    </div>
  );
};