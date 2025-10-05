import axios from 'axios';

// In Vite, environment variables are exposed on import.meta.env and must be prefixed with VITE_
const API_BASE_URL = (import.meta as any).env?.VITE_API_URL ?? 'http://localhost:8000';



export const api = {
  // Détection d'anomalies (correspond au backend FastAPI)
  async detectAnomalies(level: number = 0) {
    const response = await axios.get(`${API_BASE_URL}/detect?level=${level}`);
    return response.data;
  },

  // Récupération des annotations
  async getAnnotations() {
    const response = await axios.get(`${API_BASE_URL}/annotations`);
    return response.data;
  },

  // Ajout d'une annotation
  async addAnnotation(annotation: any) {
    const response = await axios.post(`${API_BASE_URL}/annotations`, annotation);
    return response.data;
  },

  // Suppression des annotations
  async clearAnnotations() {
    const response = await axios.delete(`${API_BASE_URL}/annotations`);
    return response.data;
  },

  // Upload d'image pour traitement
  async uploadImage(image: File) {
    const formData = new FormData();
    formData.append('image', image);

    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  // Génération de tuiles DZI
  async generateTiles(imagePath: string) {
    const response = await axios.post(`${API_BASE_URL}/generate-tiles`, {
      image_path: imagePath
    });
    return response.data;
  },

  // Détection sur un chemin donné (retourne un Blob PNG)
  async detectOnPath(imagePath: string, level: number = 0): Promise<Blob> {
    const response = await axios.post(
      `${API_BASE_URL}/detect-on-path?level=${level}`,
      { image_path: imagePath },
      { responseType: 'blob' }
    );
    return response.data as Blob;
  },

  // Health check
  async healthCheck() {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  }
};