# Company Location Finder - Algeria 🇩🇿

Un outil Python pour rechercher et localiser les agences et points de service des entreprises à travers les 58 wilayas d'Algérie.

## 📋 Description

Ce script utilise l'API Google Maps pour rechercher et collecter des informations détaillées sur les locations d'entreprises en Algérie. Il est particulièrement optimisé pour :
- Les sociétés de livraison et transport (ex: Zrexpress, Yalidine)
- La couverture des 58 wilayas
- Le support multilingue (arabe, français)
- La gestion des variations de noms d'entreprises

## ✨ Fonctionnalités

- 🔍 Recherche intelligente avec plusieurs variations de noms
- 📍 Détection précise des locations avec validation des coordonnées
- 🗺️ Couverture complète des 58 wilayas d'Algérie
- 🔄 Gestion des doublons et validation des résultats
- 📱 Collecte des numéros de téléphone et sites web
- 📍 Support des codes postaux et communes
- 💾 Export des résultats en CSV avec horodatage

## 🚀 Installation

1. Clonez le repository :
```bash
git clone <https://github.com/developing-off/algeria-company-finder>
cd <algeria-company-finder>
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Créez un fichier `.env` à la racine du projet et ajoutez votre clé API Google Maps :
```
GOOGLE_MAPS_API_KEY=votre_clé_api_ici
```

## 🛠️ Configuration requise

- Python 3.6+
- Clé API Google Maps avec les services suivants activés :
  - Places API
  - Geocoding API
  - Maps JavaScript API

## 📖 Utilisation

1. Lancez le script :
```bash
python company_finder.py
```

2. Entrez le nom de l'entreprise à rechercher

3. Choisissez la langue de recherche (fr/en/both)

4. Le script va :
   - Rechercher dans chaque wilaya
   - Afficher la progression en temps réel
   - Sauvegarder les résultats dans un fichier CSV

## 📊 Format des résultats

Le fichier CSV généré contient les informations suivantes :
- Nom de l'agence
- Adresse complète
- Wilaya et code wilaya
- Commune
- Code postal
- Numéro de téléphone
- Site web (si disponible)
- Coordonnées GPS
- Statut de l'établissement

## 🔧 Personnalisation

Le script peut être personnalisé en modifiant :
- Le rayon de recherche par wilaya
- Les variations de noms d'entreprises
- Les critères de validation des résultats
- Le format d'export des données

## ⚠️ Limitations

- Respect des quotas de l'API Google Maps
- Délai de 2 secondes entre les requêtes
- Maximum de 50 résultats par wilaya

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou problème :
1. Ouvrez une issue sur GitHub
2. Décrivez clairement le problème rencontré
3. Incluez les logs et messages d'erreur si possible
