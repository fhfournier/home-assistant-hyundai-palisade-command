# 🚀 Setup GitHub Repository - Guide Complet

## 📋 Fichiers dans le Repository

Voici ce qui est **gardé** dans `addon-hyundai-bluelink/`:

```
addon-hyundai-bluelink/
├── .gitignore              ✅ Nouveau - Exclut fichiers temporaires
├── CHANGELOG.md            ✅ Historique des versions
├── Dockerfile              ✅ Image Docker avec UV
├── README.md               ✅ Documentation de l'add-on
├── config.yaml             ✅ Configuration de l'add-on HA
├── pyproject.toml          ✅ Dépendances Python (UV)
└── rootfs/
    └── app/
        └── server.py       ✅ Serveur Flask API
```

### ❌ Fichiers supprimés (obsolètes):
- ~~`config.json`~~ (on garde seulement `config.yaml`)
- ~~`rootfs/app/requirements.txt`~~ (remplacé par `pyproject.toml`)
- ~~`rootfs/app/run.sh`~~ (on utilise `uv run` maintenant)

---

## 🔐 Étape 1: Créer le Repository GitHub Privé

### 1.1 Créer le repo

1. Allez sur https://github.com/new
2. **Repository name**: `addon-hyundai-bluelink` (ou autre nom)
3. **Description**: "Home Assistant add-on for Hyundai Bluelink vehicle control"
4. **Visibility**: 🔒 **Private** (important pour vos credentials!)
5. **Initialize**: Ne cochez RIEN (on push le code existant)
6. Cliquez **Create repository**

### 1.2 Initialiser Git et pusher

```bash
cd addon-hyundai-bluelink

# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit - Hyundai Bluelink Add-on v1.0.0"

# Ajouter le remote (remplacez USERNAME par votre nom d'utilisateur GitHub)
git remote add origin https://github.com/USERNAME/addon-hyundai-bluelink.git

# Push vers GitHub
git branch -M main
git push -u origin main
```

---

## 🔑 Étape 2: Créer un Fine-Grained Personal Access Token

### 2.1 Créer le token

1. Allez sur https://github.com/settings/tokens?type=beta
2. Cliquez **Generate new token** → **Fine-grained token**
3. **Token name**: `HomeAssistant-Addon-Access`
4. **Expiration**: 90 jours (ou custom)
5. **Repository access**: 
   - Sélectionnez **Only select repositories**
   - Choisissez `addon-hyundai-bluelink`

6. **Permissions** → **Repository permissions**:
   - **Contents**: Read-only (pour télécharger l'add-on)
   - **Metadata**: Read-only (automatique)

7. Cliquez **Generate token**
8. **COPIEZ LE TOKEN IMMÉDIATEMENT** (vous ne le verrez qu'une fois!)

```
github_pat_11AXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 2.2 Sauvegarder le token de manière sécurisée

**Option 1: Dans un gestionnaire de mots de passe**
- 1Password
- Bitwarden
- LastPass

**Option 2: Dans Home Assistant secrets.yaml**
```yaml
github_token: github_pat_11AXXXXXXXXXXXXX
```

---

## 🏠 Étape 3: Installer l'Add-on dans Home Assistant

### 3.1 Ajouter le repository privé

1. Ouvrez Home Assistant
2. **Paramètres** > **Modules complémentaires** > **Boutique des modules complémentaires**
3. **⋮** (menu) > **Dépôts**
4. Ajoutez votre URL:

```
https://github.com/USERNAME/addon-hyundai-bluelink
```

5. **IMPORTANT**: Si le repo est privé, vous devrez peut-être:
   - Utiliser une URL avec token: `https://TOKEN@github.com/USERNAME/addon-hyundai-bluelink`
   - OU configurer SSH keys

### 3.2 Installation via URL avec Token (Méthode Privée)

Pour un repo privé, utilisez cette URL:

```
https://github_pat_11AXXXXXXXXXXXXX@github.com/USERNAME/addon-hyundai-bluelink
```

Remplacez:
- `github_pat_11AXXXXXXXXXXXXX` par votre token
- `USERNAME` par votre nom d'utilisateur GitHub

### 3.3 Installer l'add-on

1. L'add-on **"Hyundai Bluelink Control"** apparaîtra dans la boutique
2. Cliquez dessus
3. **Install**
4. Configurez (voir README.md)
5. **Start**

---

## 🔄 Étape 4: Mises à Jour

### Pour pousser des mises à jour:

```bash
cd addon-hyundai-bluelink

# Modifier la version dans config.yaml
# version: "1.1.0"

# Ajouter l'entrée dans CHANGELOG.md

# Commit et push
git add .
git commit -m "v1.1.0: Description des changements"
git tag v1.1.0
git push origin main --tags
```

### Pour mettre à jour dans Home Assistant:

1. **Paramètres** > **Modules complémentaires**
2. Trouvez **Hyundai Bluelink Control**
3. Si une mise à jour est disponible, cliquez **Update**

---

## 🌐 Alternative: Repository Public (si vous voulez partager)

Si vous décidez de rendre le repo **public** plus tard:

### ⚠️ AVANT de rendre public:

1. **Vérifiez qu'il n'y a AUCUN credential dans le code**
2. Retirez tous exemples avec vos vrais identifiants
3. Ajoutez un `config_example.yaml` avec des exemples fictifs

```yaml
# config_example.yaml
username: "your-email@example.com"
password: "your-password"
pin: "1234"
vehicle_id: "get-from-status-command"
```

### Pour rendre public:

1. GitHub Repository > **Settings**
2. **Danger Zone** > **Change visibility**
3. **Make public**

Ensuite, plus besoin de token! L'URL simple fonctionne:
```
https://github.com/USERNAME/addon-hyundai-bluelink
```

---

## 📊 Structure Recommandée du README.md

Votre `README.md` devrait contenir:

- ✅ Description de l'add-on
- ✅ Instructions d'installation
- ✅ Configuration requise
- ✅ Endpoints API disponibles
- ✅ Exemples de configuration Home Assistant
- ✅ Troubleshooting
- ❌ PAS de credentials réels!

---

## 🎯 Checklist Finale Avant Push

- [ ] `.gitignore` créé
- [ ] Aucun credential dans le code
- [ ] `config.yaml` contient la bonne version
- [ ] `CHANGELOG.md` à jour
- [ ] `README.md` complet
- [ ] Tests locaux passés
- [ ] Repository GitHub créé (privé)
- [ ] Fine-grained token créé et sauvegardé
- [ ] Premier commit et push effectués

---

## 🚀 Vous êtes prêt!

Votre add-on est maintenant:
- ✅ Propre et organisé
- ✅ Prêt pour GitHub
- ✅ Sécurisé (privé)
- ✅ Facilement installable dans Home Assistant

**À vous de jouer!** 🎉
