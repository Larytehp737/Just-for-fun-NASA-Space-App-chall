import React, { useEffect } from 'react'
import OpenSeadragon from 'openseadragon'
export default function Viewer(){
  useEffect(()=>{
    const v = OpenSeadragon({
      id: 'osd',
      prefixUrl: 'https://openseadragon.github.io/openseadragon/images/',
      tileSources: 'http://localhost:8000/static/image.dzi',
      maxZoomPixelRatio: 2,
      crossOriginPolicy: 'Anonymous',
      showNavigationControl: true
    })
    return ()=> v.destroy()
  },[])
  return null
}
