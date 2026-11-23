#!/usr/bin/env bash
# Crée tout le dépôt GitHub du projet Dawri : dépôt, labels, milestones, issues (UC),
# branches par UC, CI, tags de phase.
#
# Prérequis : git et GitHub CLI (gh) installés, puis  gh auth login  (une seule fois).
# Utilisation (depuis le dossier du projet) :  bash scripts/setup_github.sh [nom-du-depot]
set -euo pipefail
cd "$(dirname "$0")/.."

REPO_NAME="${1:-dawri-poste}"

command -v git >/dev/null || { echo "git n'est pas installé."; exit 1; }
command -v gh  >/dev/null || { echo "GitHub CLI (gh) n'est pas installé : https://cli.github.com"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Connecte-toi d'abord avec : gh auth login"; exit 1; }
[ -n "$(git config user.name || true)" ] && [ -n "$(git config user.email || true)" ] || {
  echo 'Configure git d abord :'
  echo '  git config --global user.name "Ton Nom"'
  echo '  git config --global user.email "ton.email@exemple.com"'
  exit 1
}

OWNER="$(gh api user --jq .login)"
REPO="$OWNER/$REPO_NAME"
echo ">>> Dépôt cible : $REPO"

# ---------------------------------------------------------------- 1. Inception
[ -d .git ] || git init -b main
git add README.md .gitignore docs/vision.md docs/priorisation-planning.md docs/uc \
        docs/REVUE_CROISEE.md docs/GUIDE_GITHUB.md docs/uml/cycle_en_y.puml docs/uml/cycle_en_y.png \
        .github/PULL_REQUEST_TEMPLATE.md scripts
git commit -m "Inception : vision, acteurs, fiches UC, priorisation et planning"

gh repo create "$REPO" --public --source=. --remote=origin --push \
   --description "Dawri : gestion des files d'attente de la Poste tunisienne (projet Processus unifié)"
git tag -a v0.0-inception -m "Jalon Inception (LCO) : vision, UC et planning validés"
git push origin v0.0-inception

# ---------------------------------------------------------------- 2. Labels et milestones
gh label create "UC"           --repo "$REPO" --color 0E8A16 --description "Cas d'utilisation" --force
gh label create "risque"       --repo "$REPO" --color D93F0B --description "UC à risque technique" --force
gh label create "architecture" --repo "$REPO" --color 1D76DB --description "Architecture et CI" --force
gh label create "documentation" --repo "$REPO" --color 5319E7 --description "Documents et diagrammes" --force
gh label create "qualité"      --repo "$REPO" --color FBCA04 --description "Tests, revue, recette" --force

new_milestone() {  # titre, description -> numéro
  gh api "repos/$REPO/milestones" -f title="$1" -f description="$2" --jq .number
}
M1=$(new_milestone "1 - Inception"    "Vision, UC, priorisation. Tag v0.0-inception")
M2=$(new_milestone "2 - Elaboration"  "Architecture de base exécutable, route UC1 testée en CI. Tag v0.1-elaboration")
M3=$(new_milestone "3 - Construction" "UC2, UC3, UC4. Tag v0.5-construction")
M4=$(new_milestone "4 - Transition"   "UC5, UC6, revue croisée, recette. Tag v1.0-transition")

# ---------------------------------------------------------------- 3. Issues (une par UC et par tâche majeure)
issue() {  # titre, labels, milestone, fichier-ou-texte -> numéro
  local title="$1" labels="$2" milestone="$3" body="$4" url
  if [ -f "$body" ]; then
    url=$(gh issue create --repo "$REPO" --title "$title" --label "$labels" --milestone "$milestone" --body-file "$body")
  else
    url=$(gh issue create --repo "$REPO" --title "$title" --label "$labels" --milestone "$milestone" --body "$body")
  fi
  echo "${url##*/}"
}
I_VISION=$(issue "Vision et acteurs" "documentation" "1 - Inception" "Rédiger la vision en 5 lignes et identifier les acteurs (docs/vision.md).")
gh issue close "$I_VISION" --repo "$REPO" --comment "Fait dans le commit d'inception."
I_UC1=$(issue "UC1 Prendre un ticket virtuel" "UC,risque" "2 - Elaboration" docs/uc/UC1_prendre_ticket.md)
I_ARCH=$(issue "Architecture de base et CI (route UC1)" "architecture" "2 - Elaboration" "Route de bout en bout (contrôleur, service, accès aux données) pour UC1, avec un test automatisé qui passe en CI.")
I_DIAG=$(issue "Diagramme de cas d'utilisation en PlantUML" "documentation" "2 - Elaboration" "Créer docs/uml/use_cases.puml et le committer.")
I_UC2=$(issue "UC2 Suivre sa position et son attente estimée" "UC" "3 - Construction" docs/uc/UC2_suivre_position.md)
I_UC3=$(issue "UC3 Être notifié quand son tour approche" "UC,risque" "3 - Construction" docs/uc/UC3_notification_tour.md)
I_UC4=$(issue "UC4 Appeler le client suivant" "UC" "3 - Construction" docs/uc/UC4_appeler_client_suivant.md)
I_UC5=$(issue "UC5 Annuler ou reporter son ticket" "UC" "4 - Transition" docs/uc/UC5_annuler_reporter.md)
I_UC6=$(issue "UC6 Consulter les statistiques d'affluence" "UC" "4 - Transition" docs/uc/UC6_statistiques_affluence.md)
I_REV=$(issue "Revue croisée par une autre équipe" "qualité" "4 - Transition" "Faire relire la pull request de UC1 par une autre équipe (grille : docs/REVUE_CROISEE.md).")
issue "Recette et mise en pilote" "qualité" "4 - Transition" "Valider l'ensemble des UC avec un scénario de recette, puis tag v1.0-transition." >/dev/null

# ---------------------------------------------------------------- 4. Élaboration : branche UC1
git checkout -b feature/uc1-prendre-ticket
git add docs/uml/use_cases.puml docs/uml/use_cases.png
git commit -m "Diagramme de cas d'utilisation en PlantUML (#$I_DIAG)"
git add app tests requirements.txt .github/workflows/ci.yml
git commit -m "Architecture de base : route POST /tickets (UC1) de bout en bout, tests et CI (#$I_ARCH, #$I_UC1)"
git push -u origin feature/uc1-prendre-ticket

PR_URL=$(gh pr create --repo "$REPO" --base main --head feature/uc1-prendre-ticket \
  --title "UC1 Prendre un ticket virtuel : architecture de base" \
  --body "Closes #$I_UC1
Closes #$I_ARCH
Closes #$I_DIAG

Route POST /tickets de bout en bout (contrôleur, service, accès aux données) avec attribution atomique du numéro, tests unitaires, tests d'intégration et test de concurrence (50 clients simultanés).")

echo ">>> Attente de la CI (GitHub Actions)..."
for _ in $(seq 1 24); do
  out=$(gh pr checks "$PR_URL" --repo "$REPO" 2>&1 || true)
  echo "$out" | grep -qi "no checks reported" || break
  sleep 5
done
gh pr checks "$PR_URL" --repo "$REPO" --watch --interval 5
gh pr merge "$PR_URL" --repo "$REPO" --merge

git checkout main
git pull origin main
git tag -a v0.1-elaboration -m "Jalon Elaboration (LCA) : architecture de base exécutable, UC1 testé en CI"
git push origin v0.1-elaboration
gh api -X PATCH "repos/$REPO/milestones/$M2" -f state=closed >/dev/null
gh api -X PATCH "repos/$REPO/milestones/$M1" -f state=closed >/dev/null
echo ">>> Milestones Inception et Elaboration fermés."

# ---------------------------------------------------------------- 5. Une branche par UC
for b in uc2-suivre-position uc3-notification-tour uc4-appeler-client-suivant uc5-annuler-reporter uc6-statistiques-affluence; do
  git branch "feature/$b" main
  git push origin "feature/$b"
done

# ---------------------------------------------------------------- 6. Partie 2 : conception UC1 et revue croisée
git checkout -b feature/uc1-conception-classes-sequence
git add docs/uml/class_uc1.puml docs/uml/class_uc1.png docs/uml/sequence_uc1.puml docs/uml/sequence_uc1.png
git commit -m "Conception UC1 : diagramme de classes et diagramme de séquence (PlantUML)"
git push -u origin feature/uc1-conception-classes-sequence
gh pr create --repo "$REPO" --base main --head feature/uc1-conception-classes-sequence \
  --title "UC1 : diagrammes de classes et de séquence (à relire par une autre équipe)" \
  --body "Refs #$I_UC1
Closes #$I_REV après la revue croisée.

À relire avec la grille docs/REVUE_CROISEE.md."
git checkout main

echo
echo ">>> Terminé. Vérifie sur https://github.com/$REPO : Issues, Milestones, Branches, Tags, onglet Actions."
echo ">>> Il reste : demander à une autre équipe de relire la dernière pull request (revue croisée)."
