# knowledge-mining-evaluations 🧠

## 📊 Analyse interactive — Notebook

[![Notebook](https://img.shields.io/badge/Analyse-Jupyter%20Notebook-orange)](notebooks/knowledge_mining_analysis.ipynb)

**[→ Voir l'analyse complète](notebooks/knowledge_mining_analysis.ipynb)**

Le notebook couvre :
- **50 rapports d'évaluation** : 6 pays, 5 secteurs, ~150 leçons apprises
- **Analyse TF-IDF** : extraction automatique des mots-clés dominants
- **Clustering K-Means** : 5 thèmes transversaux identifiés automatiquement
- **Visualisation PCA** : cartographie des leçons dans l'espace thématique
- **Synthèse actionnable** : recommandations pour les équipes de formulation

> Accessible à tous les publics, chargés de programme, équipes MEL, bailleurs.
> Extraction automatique de leçons apprises depuis des rapports d'évaluation
> de projets de développement - Pipeline NLP & Gestion des connaissances

Développé par **Serge-Alain NYAMSIN** - Expert Évaluation & Data Science  
🔗 [github.com/sanyamsin](https://github.com/sanyamsin)

---

## 🎯 Objectif

Ce projet démontre comment la **data science et le NLP** peuvent transformer
la gestion des connaissances dans la coopération au développement.

Il simule un pipeline complet d'extraction et d'analyse de leçons apprises
depuis 50 rapports d'évaluation couvrant 5 secteurs d'intervention LuxDev :
Education & Emploi, Eau & Assainissement, Santé, Gouvernance, Environnement.

---

## 🗂️ Structure du projet

    knowledge-mining-evaluations/
    ├── data/
    │   ├── rapports_evaluation.json     # 50 rapports simulés
    │   ├── metadonnees_rapports.csv     # Métadonnées des rapports
    │   └── lecons_analysees.csv        # Leçons extraites et clusterisées
    ├── src/
    │   ├── 01_generate_reports.py      # Génération des rapports simulés
    │   ├── 02_nlp_analysis.py          # Analyse NLP & clustering
    │   └── 03_dashboard.py             # Tableau de bord HTML
    ├── reports/
    │   ├── dashboard.html              # Tableau de bord interactif
    │   ├── wordcloud_lecons.png        # WordCloud des mots-clés
    │   ├── lecons_par_secteur.png      # Distribution par secteur
    │   └── clustering_lecons.png       # Clustering thématique PCA
    ├── requirements.txt
    └── README.md

---

## 🔬 Pipeline NLP

### Étape 1 — Génération des données
Simulation de 50 rapports d'évaluation couvrant 6 pays du Sahel
et d'Afrique centrale avec leçons apprises et scores OCDE/CAD.

### Étape 2 — Analyse TF-IDF
Extraction automatique des mots-clés et expressions récurrentes
depuis les leçons apprises. Identification des thèmes dominants.

### Étape 3 — Clustering K-Means
Regroupement automatique des leçons en 5 thèmes transversaux
visualisés par réduction dimensionnelle (PCA).

### Étape 4 — Tableau de bord HTML
Rapport interactif synthétisant les résultats, scores OCDE/CAD,
leçons par secteur et recommandations les plus fréquentes.

---

## 📈 Résultats clés

| Indicateur | Valeur |
|------------|--------|
| Rapports analysés | 50 |
| Leçons extraites | ~150 |
| Pays couverts | 6 |
| Secteurs analysés | 5 |
| Thèmes identifiés | 5 |

---

## 🛠️ Technologies utilisées

- **Python 3.12** - Pipeline principal
- **NLTK** - Traitement du langage naturel
- **Scikit-learn** - F-IDF, K-Means, PCA
- **WordCloud** - Visualisation des mots-clés
- **Pandas / NumPy** - Manipulation des données
- **Matplotlib / Seaborn** - Visualisations

---

## 🚀 Reproduire l'analyse

```bash
# 1. Cloner le repo
git clone https://github.com/sanyamsin/knowledge-mining-evaluations.git
cd knowledge-mining-evaluations

# 2. Créer l'environnement virtuel
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Exécuter le pipeline
python src/01_generate_reports.py
python src/02_nlp_analysis.py
python src/03_dashboard.py

# 5. Ouvrir le tableau de bord
start reports/dashboard.html
```

---

## 🌍 Pertinence pour la coopération au développement

Ce projet répond à un besoin réel identifié dans les agences de développement :
les leçons apprises restent souvent enfouies dans des rapports PDF non exploités.
Ce pipeline permet de les extraire, classer et restituer automatiquement
aux équipes de formulation - améliorant ainsi l'apprentissage organisationnel.

---

## 👤 Auteur

**Serg-alain NYAMSIN**  
MSc Data Science & AI - DSTI Paris  
12+ ans en coopération au développement (Sahel, Afrique centrale)  
🔗 [github.com/sanyamsin](https://github.com/sanyamsin)

---

*Ce projet s'inscrit dans une démarche de modernisation de la gestion
des connaissances dans la coopération au développement.*
