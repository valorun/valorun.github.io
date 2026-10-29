# Valorun OÜ — Ingénierie IA & conseil

Site vitrine statique bilingue de **Valorun OÜ**, conçu pour GitHub Pages. **Aucune compilation, installation Node ou dépendance JavaScript.**

- Français : `index.html`
- Anglais : `en/index.html`
- Mise en page et ressources partagées : `assets/`
- Contact : `valorun@proton.me`
- Projets cités : [Corvus](https://valorun.github.io/corvus-website/index.html) et les [robots de la Confrérie du boulon](https://clarius-robot.com/)

## Voir le site en local

Depuis ce dossier :

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Ouvrir <http://localhost:8000/> ou <http://localhost:8000/en/>. Utiliser un serveur local plutôt que de double-cliquer sur le HTML, notamment pour charger les illustrations SVG partagées.

## Vérifier le site

Python 3.12 ou plus récent, sans bibliothèque supplémentaire :

```sh
python3 tests/check_site.py
```

Le contrôle vérifie les liens et ancres internes, les fichiers, les deux langues, le destinataire des emails, les métadonnées, certaines bases d’accessibilité et l’absence de ressources de rendu distantes. Les liens externes ne sont pas sollicités par ce contrôle.

Pour une modification de présentation, vérifier également les deux langues sur mobile et ordinateur, la navigation avec Tab et le changement de langue. L’ensemble du site doit rester utilisable sans JavaScript.

## Publier sur GitHub Pages

1. Créer un dépôt GitHub, public si nécessaire selon l’offre GitHub utilisée, puis y envoyer les fichiers de ce dossier. Conserver `index.html`, `en/`, `assets/` et `.nojekyll` à la racine.
2. Dans le dépôt, ouvrir **Settings → Pages → Build and deployment**.
3. Choisir **Deploy from a branch**, puis la branche contenant le site, généralement `main`, et le dossier **/ (root)**.
4. Enregistrer et attendre la fin du déploiement. GitHub affiche l’adresse du site dans cette même page.

Par exemple, un dépôt nommé `vitrine` sur le compte `valorun` aurait normalement pour adresse `https://valorun.github.io/vitrine/`, avec sa version anglaise dans `en/`. Un dépôt `valorun.github.io` utiliserait la racine du domaine. Les chemins relatifs du site permettent les deux configurations.

Le fichier `.nojekyll` désactive le traitement Jekyll : aucun thème ni workflow personnalisé n’est nécessaire. Le dépôt et sa publication ne sont pas créés automatiquement par ce projet.

### Avant publication commerciale

- **Compléter les informations légales de Valorun OÜ dans les deux pages.** Les éléments actuellement présents se limitent aux informations connues et ne constituent pas des mentions légales complètes. Ajouter les renseignements applicables à la société : forme et adresse du siège, numéro d’immatriculation, TVA le cas échéant, et coordonnées légales de l’hébergeur retenu. Voir les [informations officielles sur les mentions obligatoires](https://entreprendre.service-public.gouv.fr/vosdroits/F31228).
- Vérifier les conditions d’utilisation des informations et du logo Corvus, puis confirmer que les projets et les domaines d’expérience présentés peuvent être publiés à ce niveau de détail. Aucun employeur n’est associé à ces exemples dans la section « Projets » ; MindTitan apparaît uniquement dans le parcours.
- Une fois l’adresse définitive connue, ajouter une URL canonique et `og:url` propres à chaque langue. Remplacer également les trois liens `rel="alternate"` de chaque en-tête par les URLs HTTPS absolues correspondantes : les moteurs de recherche les attendent pour `hreflang`. Conserver les liens de navigation FR/EN relatifs. Une image de partage peut aussi être ajoutée avec une URL absolue. Aucune adresse de publication n’a été supposée dans le HTML.
- Mettre à jour la formulation sur l’hébergement dans les informations légales une fois le site réellement déployé.

Le contact est un lien `mailto:` : il ouvre le logiciel de messagerie du visiteur. L’adresse reste visible et copiable si aucun logiciel n’est configuré. Aucun formulaire ne collecte de données sur le site.

## Modifier le contenu

Les deux pages sont du HTML explicite et partagent une seule feuille de style. Pour conserver leur cohérence :

- reporter chaque modification éditoriale dans les deux langues ;
- conserver les mêmes identifiants de sections ;
- garder le préfixe `../assets/` pour les ressources de la page anglaise ;
- utiliser des liens relatifs plutôt que des chemins commençant par `/` ;
- relancer le contrôle après modification.

Les couleurs et les polices sont regroupées au début de `assets/styles.css`. Les illustrations et icônes sont dans `assets/icons.svg`.

## Ressources et confidentialité

Le logo original fourni est conservé intact dans le dossier. `assets/logo.webp` en est une version recadrée et optimisée ; les icônes de navigateur en sont dérivées. Le logo du projet Corvus est repris dans `assets/corvus-logo.webp` depuis le site public du projet.

Les polices **DM Sans** et **Instrument Serif** sont hébergées localement sous licence SIL Open Font License. Leurs licences sont incluses dans `assets/fonts/`. Aucun appel à Google Fonts n’est effectué par le site.

Le site ne charge aucun outil d’analyse d’audience, traceur, formulaire tiers ou script d’exécution. Les liens externes ne sont ouverts que lorsque le visiteur les suit ; l’hébergement GitHub Pages reste soumis aux politiques de GitHub.
