import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UserSettings {
  fontSize: number;
  contrast: number;
  reducedMotion: boolean;
  highContrast: boolean;
  animationSpeed: number;
  darkMode: boolean;
}

interface UserPreferences {
  settings: UserSettings;
  updateSettings: (settings: Partial<UserSettings>) => void;
  resetSettings: () => void;
}

const defaultSettings: UserSettings = {
  fontSize: 16,
  contrast: 100,
  reducedMotion: false,
  highContrast: false,
  animationSpeed: 1,
  darkMode: false,
};

export const useUserPreferences = create<UserPreferences>()(
  persist(
    (set) => ({
      settings: defaultSettings,
      updateSettings: (newSettings) =>
        set((state) => ({
          settings: { ...state.settings, ...newSettings },
        })),
      resetSettings: () => set({ settings: defaultSettings }),
    }),
    {
      name: 'user-preferences',
    }
  )
);