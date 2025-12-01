# Cahier de Tests - Todo-list App

## Tests Automatisés (Unit Tests)

### 1. Test d'accès aux pages principales
- **Objectif** : Vérifier que les pages principales sont accessibles
- **URLs testées** : /, /create/, /update/<id>/, /delete/<id>/
- **Attendu** : Code HTTP 200 pour les pages accessibles, 404 pour les IDs inexistants

### 2. Test de création d'une tâche
- **Objectif** : Vérifier qu'une nouvelle tâche peut être créée
- **Actions** : POST avec données valides
- **Attendu** : Tâche créée en base, redirection vers la liste

### 3. Test de mise à jour d'une tâche
- **Objectif** : Vérifier qu'une tâche existante peut être modifiée
- **Actions** : POST avec nouvelles données
- **Attendu** : Tâche modifiée, redirection vers la liste

### 4. Test de suppression d'une tâche
- **Objectif** : Vérifier qu'une tâche peut être supprimée
- **Actions** : POST sur l'URL de suppression
- **Attendu** : Tâche supprimée de la base, redirection

### 5. Test de validation des formulaires
- **Objectif** : Vérifier la validation côté serveur
- **Scénarios** : Titre vide, titre trop long, dates invalides
- **Attendu** : Messages d'erreur appropriés

### 6. Test des modèles (Models)
- **Objectif** : Vérifier le comportement des modèles
- **Tests** : Création, sauvegarde, méthodes __str__, relations
- **Attendu** : Comportement conforme aux spécifications

### 7. Test de l'ordre d'affichage
- **Objectif** : Vérifier que les tâches sont dans le bon ordre
- **Critères** : Par date de création, par statut (complété/non complété)
- **Attendu** : Ordre correct dans le template

## Tests Manuels

### 8. Test d'expérience utilisateur (UX)
- **Objectif** : Vérifier la facilité d'utilisation
- **Actions** : Parcourir toutes les fonctionnalités
- **Vérifications** : Boutons accessibles, messages clairs, retours visuels

### 9. Test de responsive design
- **Objectif** : Vérifier l'adaptation aux différentes tailles d'écran
- **Devices** : Mobile (360px), tablette (768px), desktop (1200px)
- **Vérifications** : Pas de débordement, lisibilité, interactions

### 10. Test de navigation clavier
- **Objectif** : Vérifier l'accessibilité clavier
- **Actions** : Tab, Enter, Espace, raccourcis
- **Attendu** : Toutes les fonctionnalités accessibles au clavier

### 11. Test de performance
- **Objectif** : Vérifier les temps de réponse
- **Métriques** : Temps de chargement page (< 3s), temps réponse serveur (< 500ms)
- **Outils** : Chrome DevTools, Lighthouse

### 12. Test de sécurité
- **Objectif** : Vérifier les aspects sécurité
- **Points** : Protection CSRF, validation inputs, injection SQL
- **Outils** : Vérification manuelle, extensions sécurité

## Tests Visuels

### 13. Test de cohérence visuelle
- **Objectif** : Vérifier la cohérence du design
- **Éléments** : Couleurs, polices, espacements, icônes
- **Méthode** : Comparaison avec maquettes, checklist

### 14. Test d'affichage des données
- **Objectif** : Vérifier que les données s'affichent correctement
- **Cas** : Titres longs, descriptions multilignes, dates formatées
- **Vérifications** : Pas de coupure indésirable, formatage correct

### 15. Test d'états différents
- **Objectif** : Vérifier les différents états de l'interface
- **États** : Liste vide, liste pleine, filtres actifs, recherche
- **Attendu** : Messages appropriés (ex: "Aucune tâche" pour liste vide)

## Tests d'Intégration

### Bonus - Tests cross-browser
- **Objectif** : Vérifier la compatibilité navigateurs
- **Navigateurs** : Chrome, Firefox, Edge, Safari
- **Fonctionnalités** : Toutes les principales

### Bonus - Tests de déploiement
- **Objectif** : Vérifier le processus de déploiement
- **Étapes** : Build, déploiement, rollback
- **Vérifications** : Variables d'environnement, migrations, static files