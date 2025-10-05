import OpenSeadragon from 'openseadragon';
import { useEffect, useRef } from 'react';

interface ImageViewerProps {
  image: string; // peut être URL d'image simple ou URL/chemin DZI
  overlayImageUrl?: string; // PNG RGBA heatmap à superposer
  overlayOpacity?: number; // 0..1
  onLevelChange?: (level: number) => void; // niveau pyramidal approx selon zoom
  annotations?: Annotation[];
  onAnnotationAdd?: (annotation: Annotation) => void;
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
  overlayImageUrl,
  overlayOpacity = 0.6,
  annotations = [],
  onAnnotationAdd,
  onLevelChange
}: ImageViewerProps) => {
  const viewerRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const heatmapElRef = useRef<HTMLImageElement | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Initialisation du viewer OpenSeadragon
    const viewer = OpenSeadragon({
      element: containerRef.current,
      tileSources: image.endsWith('.dzi') || image.includes('.dzi')
        ? image
        : { type: 'image', url: image },
      showNavigationControl: true,
      showRotationControl: true,
      gestureSettingsMouse: {
        clickToZoom: false,
        dblClickToZoom: true
      },
      debugMode: false
    });
    viewerRef.current = viewer;

    // Informe du niveau au chargement et sur zoom
    const reportLevel = () => {
      if (!onLevelChange) return;
      const item = viewer.world.getItemAt(0);
      if (!item) return;
      // approx: map zoom (imageSpace) vers niveau pyramidal (log2)
      const zoom = viewer.viewport.getZoom(true);
      const approxLevel = Math.max(0, Math.min(8, Math.round(Math.log2(Math.max(zoom, 1e-6)))));
      onLevelChange(approxLevel);
    };
    const onOpen = () => reportLevel();
    const onZoom = () => reportLevel();
    const onAnimFinish = () => reportLevel();
    viewer.addHandler('open', onOpen);
    viewer.addHandler('zoom', onZoom);
    viewer.addHandler('animation-finish', onAnimFinish);

    // Ajout des overlays pour les annotations
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
      viewer.removeHandler('open', onOpen);
      viewer.removeHandler('zoom', onZoom);
      viewer.removeHandler('animation-finish', onAnimFinish);
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

  // Ajout/Mise à jour de l'overlay heatmap
  useEffect(() => {
    const viewer = viewerRef.current;
    if (!viewer) return;
    if (!overlayImageUrl) {
      // retire l'overlay si présent
      if (heatmapElRef.current) {
        try { viewer.removeOverlay(heatmapElRef.current); } catch {}
        heatmapElRef.current = null;
      }
      return;
    }

    const world = viewer.world;
    const item = world.getItemAt(0);
    if (!item) return;
    const contentSize = item.getContentSize();
    const rect = item.imageToViewportRectangle(0, 0, contentSize.x, contentSize.y);

    // Crée ou met à jour l'élément IMG overlay
    let img = heatmapElRef.current;
    if (!img) {
      img = document.createElement('img');
      img.style.width = '100%';
      img.style.height = '100%';
      img.style.opacity = String(overlayOpacity);
      img.style.pointerEvents = 'none';
      heatmapElRef.current = img;
      viewer.addOverlay({ element: img, location: rect, placement: OpenSeadragon.OverlayPlacement.CENTER });
    }
    img.src = overlayImageUrl;
    img.style.opacity = String(overlayOpacity);
  }, [overlayImageUrl, overlayOpacity]);

  return (
    <div className="relative w-full h-[70vh]">
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