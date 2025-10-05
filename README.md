# Embiggen Your Eyes — Plateforme Web d’Exploration d’Images NASA à Très Haute Résolution

Ce dépôt héberge notre prototype pour le défi NASA Space Apps « Embiggen Your Eyes ».

Objectif: offrir une expérience fluide pour explorer, annoter et comparer des images gigan‑/tera‑pixels issues de missions NASA (Terre, Lune, Mars, astrophysique), avec un zoom profond, des superpositions thématiques et une timeline pour les séries temporelles.

Sommaire
- Pourquoi ce projet
- Cas d’usage cibles
- Fonctionnalités clés (MVP → ++)
- Architecture & choix techniques
- Données, formats et performances
- Démonstration prévue
- Roadmap hackathon
- Démarrage rapide (dev)
- Accessibilité, i18n et qualité
- Limites, risques et plans B

Pourquoi ce projet
Les images « géantes » (gigapixel/terapixel) sont difficiles à explorer avec des outils généralistes. Nous proposons une interface moderne qui:
- charge uniquement les tuiles nécessaires au niveau de zoom et à la zone affichée,
- permet d’annoter et de partager des découvertes,
- aligne et compare des images multi‑sources/multi‑bandes/multi‑dates.

Cas d’usage cibles
- Enfants/jeunes (8–14 ans): ateliers, missions guidées « Trouve la tempête », « Chasse aux cratères », mini‑jeux de repérage et quizz.
- Public curieux: zoomer dans Andromède (Hubble) ou une tempête de poussière sur Mars.
- Éducateurs/musées: créer des visites guidées avec points d’intérêt annotés et storytelling.
- Chercheurs/étudiants: comparer la même zone à différentes dates, bandes spectrales ou instruments (changements, corrélations).

Fonctionnalités clés
MVP (itération 1)
- Visionneuse Deep Zoom: zoom/pan ultra fluide via OpenSeadragon (OSD).
- Gestion de tuiles IIIF / Deep Zoom (DZI): chargement adaptatif côté client.
- Annotations: points/rectangles/polygones, étiquettes et métadonnées (auteur, date, tags), export/import WebAnnotation JSON.
- Superpositions (overlays) d’images: bascule simple de couches, réglage d’opacité, mode swipe (rideau) et loupe.
- Barre de recherche: par nom de feature, coordonnées (lon/lat, lignes/colonnes), ID d’image.
- Timeline simple: sélectionner une date/version pour une zone (time‑series).
- Partage deep‑link: URL encode l’état (vue, couches, niveau de zoom, sélection de date).
- Mode Enfants (activable):
  - UI simplifiée avec gros boutons et pictos, 3 actions principales: Zoomer, Explorer, Noter. 
  - Missions guidées (« Trouve la tempête », « Chasse aux cratères ») avec indices visuels.
  - Récompenses ludiques: stickers/badges à débloquer en terminant une mission.
  - Audio‑guide et bulles d’explications adaptées (FR/EN), glossaire illustré.
  - Sélection de datasets « safe & wow » (Andromède, Lune, ouragans vus de l’espace) pré‑curés.

Itération 2+
- Alignement/registration basique d’images (translation/scale) pour instruments différents.
- Mesures: distance, aire, profil d’intensité, statistiques par région.
- Contraste/false color: LUTs, combinaisons RGB de bandes, stretch dynamique.
- Recherche augmentée: suggestions sémantiques via modèle CLIP/open‑source (si temps/compute le permet) — optionnelle.
- Collaboration: sessions en temps réel (CRDT / WebSocket) pour co‑annotation.
- Kids+: 
  - Puzzles (réassembler une tuile), jeu « Où est‑ce? » avec minuteur.
  - Mode classe: tableau de bord enseignant, partage de missions, suivi simple (local/compte invité).

Architecture & choix techniques
Front‑end (lead): React + OpenSeadragon
- UI: React + Tailwind CSS (déjà présent). Composants contrôlant OSD, panneau couches, timeline, panneau annotations.
- Viewer: OpenSeadragon pour l’imagerie tuilée (DZI/IIIF). Plugins utiles: openseadragon-annotations, openseadragon-filtering, openseadragon-scalebar.
- État & routing: Zustand/Redux léger + React Router. Deep‑links via query params.

Données & intégration API
- Sources: NASA/USGS/ESA exposant des pyramides de tuiles (IIIF), ou nos propres DZI générés.
- Proxy/Backend minimal (Node/Express):
  - proxy des tuiles vers domaines externes (CORS, rate control),
  - service annotations (CRUD) + export WebAnnotation,
  - catalogue d’assets (liste datasets, métadonnées, emprise, bandes, timeline).
- Stockage: fichiers JSON/SQLite pour le hackathon; passage à Postgres/S3 si besoin.

Formats de tuilage recommandés
- Deep Zoom Image (DZI): simple, parfaitement supporté par OSD.
- IIIF Image API v2/v3: standard musées/archives; compatible OSD; idéal si la source publie déjà IIIF.
- Cloud‑Optimized GeoTIFF (COG): si données géo; servi via titiler/cog‑server pour générer des tuiles à la volée.

Performances
- Chargement paresseux des tuiles + cache navigateur.
- Pré‑génération de pyramides (dzi/iiif) pour les assets de démo.
- Limiter le sur‑dessin: simplification de polygones et clustering d’annotations.
- Web Workers pour calculs coûteux (mesures, histogrammes). Optionnel: WebGL shaders (filtrage/false color).

Sécurité, vie privée et contrôle parental
- Clés d’API chargées côté serveur (proxy).
- Rate limiting de l’accès aux endpoints externes si nécessaire.
- Mode Enfants: pas de collecte de données personnelles; progrès et badges conservés en local (localStorage) uniquement.
- Partage/publication: requiert une « passerelle parent/enseignant » (consentement explicite) et une modération minimale.
- Parental gate: pour quitter le Mode Enfants ou ouvrir des liens externes, petite vérification adulte (ex: calcul simple + indice audio).
- Conformité: viser les principes COPPA/GDPR‑K (pas de publicité, minimisation des données). À valider avant déploiement public.

Démonstration prévue (exemple concret)
Dataset de démo minimal (local ou public):
- Andromeda (Hubble) en DZI/IIIF.
- Mosaïque lunaire LRO (tuile/IIIF) — au moins un extrait.
- Série temporelle Terre (MODIS/VIIRS) 3–5 dates pour une même emprise.

Parcours démo:
1) Activer le Mode Enfants via le commutateur dans la barre supérieure.
2) Lancer la mission « Chasse aux cratères » (Lune): zoomer jusqu’à trouver une « crater chain », placer une épingle; gagner un sticker.
3) Audio‑guide: écouter une courte explication sur ce qu’est un cratère et comment il se forme.
4) Explorer Andromède avec la loupe: repérer un amas d’étoiles brillant; valider la mission et débloquer un badge.
5) Partager l’URL — recharger la page reproduit la vue, le mode actif (Enfants) et la progression locale.
6) Optionnel (mode avancé): superposer 2 dates MODIS, comparer via swipe et timeline; montrer les fonctionnalités « adultes ».

Roadmap hackathon
- T0 (2–3 h):
  - Scaffold React (vite/create‑react‑app déjà présent) + OSD de base. ✓
  - Page Viewer avec un dataset DZI local pour valider la chaîne. 
- T1 (demi‑journée):
  - Panneau couches + opacité + swipe. 
  - Annotations points/rectangles + sauvegarde locale (localStorage). 
  - Commutateur « Mode Enfants » + UI simplifiée (gros boutons, 3 actions).
  - Datasets enfants curés (Andromède, Lune, Terre) chargés via DZI/IIIF.
- T2 (demi‑journée):
  - Timeline + deep‑links (query params). 
  - Export/import WebAnnotation JSON. 
  - 1 mission scriptée (JSON) + 3 stickers/badges débloquables.
  - Audio‑guide simple (fichiers audio locaux) + glossaire modal.
  - Parental gate minimal (écran de vérification pour quitter le Mode Enfants).
- T3 (optionnel):
  - Petit serveur Node/Express: proxy tuiles + REST annotations. 
  - Déploiement (Vercel/Netlify) + stockage annotations JSON sur GitHub Gist/S3. 
  - Mode classe (alpha): partage de missions via URL + compteur de missions réalisées (local).

Démarrage rapide (dev)
Prérequis
- Node 18+

Installation
- cd embiggen-your-eyes
- npm install
- npm run dev

Données d’exemple
- Placer un DZI dans public/datasets/andromeda/andromeda.dzi (ou utiliser une URL IIIF publique). 
- Dans le viewer, fournir l’URL du manifest (DZI/IIIF) pour charger l’image.

Accessibilité, i18n et qualité
- A11y: contraste élevé, commandes clavier pour zoom/pan, focus visibles, descriptions ARIA, tailles de cibles tactiles ≥ 44px, palettes daltonisme‑friendly.
- Option police adaptée (ex: OpenDyslexic) activable en Mode Enfants; narrations audio avec sous‑titres, contrôle de vitesse.
- i18n: FR/EN via i18next (clé‑valeur); textes enfants adaptés (phrases courtes, vocabulaire simple), fichiers JSON.
- Tests: smoke tests sur composants clés (viewer, annotations), ESLint/Prettier; tests de flux « mission enfant » (détection, validation, badge).

Limites, risques et plans B
- Données géoréférencées: OSD n’est pas « map‑aware ». Si nécessaire: OpenLayers/Leaflet + COG/WMTS.
- Aspects ML (recherche sémantique): optionnels; garder le cœur (exploration/annotations) robuste.
- Très grands ensembles privés: prévoir un mode offline avec jeux de tuiles locaux.

Sommes‑nous sur la bonne voie ?
Oui. Le choix React + OpenSeadragon est pertinent pour un viewer haute résolution, extensible, rapide à livrer pendant un hackathon. L’utilisation de DZI/IIIF garantit la scalabilité côté client. En ajoutant un petit proxy et un service d’annotations simple, on couvre l’essentiel des besoins du défi tout en gardant une implémentation réaliste.

Prochaines étapes immédiates
- Intégrer un jeu de données DZI/IIIF de test et valider le zoom/pan.
- Implémenter le panneau de couches + opacité, puis annotations simples.
- Exposer l’état via l’URL (deep‑links) pour les partages et la démo.
