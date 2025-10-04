import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';

interface ProcessImageParams {
  image: File | string;
  style: string;
  intensity: number;
  annotations: Array<{
    x: number;
    y: number;
    width: number;
    height: number;
    type: 'eye' | 'face';
  }>;
}

export const api = {
  // Traitement d'image
  async processImage({ image, style, intensity, annotations }: ProcessImageParams) {
    const formData = new FormData();
    
    if (image instanceof File) {
      formData.append('image', image);
    } else {
      formData.append('imageUrl', image);
    }
    
    formData.append('style', style);
    formData.append('intensity', intensity.toString());
    formData.append('annotations', JSON.stringify(annotations));

    const response = await axios.post(`${API_BASE_URL}/process`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  // Détection automatique des yeux
  async detectEyes(image: File | string) {
    const formData = new FormData();
    
    if (image instanceof File) {
      formData.append('image', image);
    } else {
      formData.append('imageUrl', image);
    }

    const response = await axios.post(`${API_BASE_URL}/detect-eyes`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  // Récupération des styles disponibles
  async getStyles() {
    const response = await axios.get(`${API_BASE_URL}/styles`);
    return response.data;
  },

  // Sauvegarde d'un style personnalisé
  async saveCustomStyle(style: any) {
    const response = await axios.post(`${API_BASE_URL}/styles`, style);
    return response.data;
  }
};