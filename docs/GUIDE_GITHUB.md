# Guide GitHub pas à pas (TP1)

## Ce que le TP1 demande, et où le trouver sur GitHub

| Demande de l'énoncé | Où le voir sur GitHub |
|---|---|
| Dépôt Git et GitHub | La page du dépôt |
| Les UC saisis comme tickets | Onglet **Issues** (une issue par UC) |
| 4 milestones = les 4 phases | Onglet **Issues**, bouton **Milestones** |
| Chaque UC a sa branche | Menu **branches** (`feature/uc1-...`, `feature/uc2-...`) |
| Les jalons de phase sont des tags | Onglet **Releases / Tags** (`v0.0-inception`, `v0.1-elaboration`) |
| Diagramme de cas d'utilisation PlantUML | Fichier `docs/uml/use_cases.puml` |
| Architecture qui tourne + test en CI | Dossier `app/` et onglet **Actions** (coche verte) |
| Tag `v0.1-elaboration` et milestone fermé | Tags et Milestones (état Closed) |
| Partie 2 : classes, séquence, tests, revue croisée | `docs/uml/class_uc1.puml`, `sequence_uc1.puml`, `tests/`, pull request relue |

## Méthode rapide (le script fait tout)

1. Installer **git** (https://git-scm.com) et **GitHub CLI** (https://cli.github.com).
2. Dans un terminal, une seule fois :
   ```
   git config --global user.name "Zaineb Kchaou"
   git config --global user.email "ton.email@exemple.com"
   gh auth login
   ```
   Choisis GitHub.com, HTTPS, puis connexion par navigateur avec le compte Zaineb-Kchaou.
3. Dézipper le projet, ouvrir un terminal dans le dossier, puis :
   ```
   bash scripts/setup_github.sh dawri-poste
   ```
   Sous Windows, utilise **Git Bash** (installé avec git).
4. Le script attend que la CI passe au vert, fusionne la pull request de UC1, pose le tag `v0.1-elaboration` et ferme les milestones.
5. Ouvre https://github.com/Zaineb-Kchaou/dawri-poste et passe la checklist du tableau ci-dessus.

Si la CI échoue (croix rouge dans l'onglet Actions), ouvre le détail du job, lis l'erreur et envoie-la-moi.

## Revue croisée (partie 2)

Le script ouvre une pull request « UC1 : diagrammes de classes et de séquence ». Donne son lien à une autre équipe,
qui la relit avec la grille `docs/REVUE_CROISEE.md` (commentaires puis « Approve »). Note leur retour dans ce fichier.

## Si le script pose problème : méthode manuelle (interface web)

1. github.com, **New repository**, nom `dawri-poste`, public.
2. **Add file > Upload files** : glisser le contenu du dossier du projet, puis **Commit**.
3. **Issues > Milestones > New milestone** : créer `1 - Inception`, `2 - Elaboration`, `3 - Construction`, `4 - Transition`.
4. **Issues > New issue** : une issue par UC (copier le contenu de `docs/uc/UCx_....md`), avec son milestone.
5. Branches : menu des branches, taper `feature/uc1-prendre-ticket`, **Create branch**. Idem pour UC2 à UC6.
6. Tags : **Releases > Draft a new release > Choose a tag**, taper `v0.1-elaboration`, **Publish release**.
7. Actions : le fichier `.github/workflows/ci.yml` lance les tests à chaque commit.

## Commandes Git à connaître pour la validation

| Commande | Rôle |
|---|---|
| `git status` | Voir les fichiers modifiés |
| `git add fichier` | Préparer un fichier pour le commit |
| `git commit -m "message"` | Enregistrer une version |
| `git checkout -b feature/ucX-nom` | Créer une branche pour un UC |
| `git push -u origin feature/ucX-nom` | Envoyer la branche sur GitHub |
| `git tag -a v0.1-elaboration -m "..."` | Poser un jalon |
| `git log --oneline --graph --all` | Voir l'historique |
