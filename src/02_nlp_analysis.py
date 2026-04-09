# =============================================================
# knowledge-mining-evaluations | LuxDev
# Script 02 : Analyse NLP — Extraction des leçons apprises
# Auteur : Trésor Sany | github.com/sanyamsin
# Date : Avril 2026
# =============================================================
# Objectif : Extraire automatiquement les thèmes récurrents
# et les leçons apprises depuis les rapports d'évaluation
# Méthodes : TF-IDF, clustering K-Means, WordCloud
# =============================================================

import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import nltk
import warnings
warnings.filterwarnings('ignore')

# --- Téléchargement ressources NLTK --------------------------
nltk.download('stopwords', quiet=True)
nltk.download('punkt',     quiet=True)
from nltk.corpus import stopwords

print("🔄 Chargement des rapports d'évaluation...")

# --- Chargement des données ----------------------------------
with open("data/rapports_evaluation.json", "r",
          encoding="utf-8") as f:
    rapports = json.load(f)

df_meta = pd.read_csv("data/metadonnees_rapports.csv")

print(f"✅ {len(rapports)} rapports chargés\n")

# --- 1. Extraction des leçons apprises ----------------------
print("═══════════════════════════════════════")
print("1. EXTRACTION DES LEÇONS APPRISES")
print("═══════════════════════════════════════")

lecons_data = []
for r in rapports:
    for lecon in r["lecons_apprises"]:
        lecons_data.append({
            "id_rapport": r["id"],
            "pays":       r["pays"],
            "secteur":    r["secteur"],
            "bailleur":   r["bailleur"],
            "lecon":      lecon,
            "score_moyen": r["scores_ocde_cad"]["moyenne"]
        })

df_lecons = pd.DataFrame(lecons_data)
print(f"✅ {len(df_lecons)} leçons apprises extraites")
print(f"   Moyenne par rapport : {len(df_lecons)/len(rapports):.1f} leçons\n")

# --- 2. Analyse TF-IDF --------------------------------------
print("═══════════════════════════════════════")
print("2. ANALYSE TF-IDF — MOTS CLÉS")
print("═══════════════════════════════════════")

stop_fr = list(stopwords.words('french')) + [
    "les", "des", "est", "une", "pour", "par", "sur",
    "dans", "avec", "plus", "sont", "ont", "été", "cette",
    "tout", "tous", "aux", "leur", "leurs", "programme",
    "projet", "intervention"
]

vectorizer = TfidfVectorizer(
    stop_words  = stop_fr,
    max_features= 100,
    ngram_range = (1, 2)
)

tfidf_matrix = vectorizer.fit_transform(df_lecons["lecon"])
feature_names = vectorizer.get_feature_names_out()

# Top 15 mots clés globaux
scores_globaux = np.array(tfidf_matrix.mean(axis=0)).flatten()
top_indices    = scores_globaux.argsort()[-15:][::-1]
top_mots       = [(feature_names[i], round(scores_globaux[i], 4))
                  for i in top_indices]

print("\nTop 15 mots-clés des leçons apprises :")
for mot, score in top_mots:
    print(f"  {mot:<30} {score:.4f}")

# --- 3. Clustering thématique K-Means -----------------------
print("\n═══════════════════════════════════════")
print("3. CLUSTERING THÉMATIQUE")
print("═══════════════════════════════════════")

n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(tfidf_matrix)
df_lecons["cluster"] = clusters

print(f"\n{n_clusters} thèmes identifiés :\n")
for c in range(n_clusters):
    lecons_cluster = df_lecons[df_lecons["cluster"] == c]["lecon"]
    # Mots clés du cluster
    tfidf_cluster  = vectorizer.transform(lecons_cluster)
    scores_cluster = np.array(tfidf_cluster.mean(axis=0)).flatten()
    top_cluster    = scores_cluster.argsort()[-5:][::-1]
    mots_cluster   = [feature_names[i] for i in top_cluster]

    print(f"  Thème {c+1} ({len(lecons_cluster)} leçons) : "
          f"{' | '.join(mots_cluster)}")

# --- 4. Analyse par secteur ---------------------------------
print("\n═══════════════════════════════════════")
print("4. LEÇONS PAR SECTEUR")
print("═══════════════════════════════════════")

synthese = df_lecons.groupby("secteur").agg(
    nb_lecons    = ("lecon", "count"),
    score_moyen  = ("score_moyen", "mean")
).round(2).sort_values("nb_lecons", ascending=False)

print(f"\n{synthese.to_string()}\n")

# Sauvegarde
df_lecons.to_csv("data/lecons_analysees.csv", index=False)
print("✅ Leçons analysées sauvegardées dans data/")

# --- 5. Visualisations --------------------------------------
print("\n🔄 Génération des visualisations...")
os.makedirs("reports", exist_ok=True)

# Graphique 1 : WordCloud global
texte_global = " ".join(df_lecons["lecon"].tolist())
wc = WordCloud(
    width           = 1200,
    height          = 600,
    background_color= "white",
    stopwords       = set(stop_fr),
    colormap        = "Blues",
    max_words       = 80
).generate(texte_global)

plt.figure(figsize=(14, 7))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title("Mots-clés des leçons apprises — Rapports d'évaluation",
          fontsize=16, fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig("reports/wordcloud_lecons.png", dpi=150,
            bbox_inches="tight")
plt.close()
print("✅ WordCloud sauvegardé")

# Graphique 2 : Leçons par secteur
fig, ax = plt.subplots(figsize=(10, 6))
synthese["nb_lecons"].sort_values().plot(
    kind    = "barh",
    ax      = ax,
    color   = "#1F4E79",
    alpha   = 0.8
)
ax.set_xlabel("Nombre de leçons apprises", fontsize=12)
ax.set_title("Distribution des leçons apprises par secteur",
             fontsize=14, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("reports/lecons_par_secteur.png", dpi=150,
            bbox_inches="tight")
plt.close()
print("✅ Graphique secteurs sauvegardé")

# Graphique 3 : Clusters PCA
pca    = PCA(n_components=2, random_state=42)
coords = pca.fit_transform(tfidf_matrix.toarray())

fig, ax = plt.subplots(figsize=(10, 7))
colors  = ["#1F4E79", "#2E86AB", "#A23B72", "#F18F01", "#C73E1D"]
for c in range(n_clusters):
    mask = clusters == c
    ax.scatter(coords[mask, 0], coords[mask, 1],
               c=colors[c], label=f"Thème {c+1}",
               alpha=0.7, s=60)

ax.set_title("Clustering thématique des leçons apprises (PCA)",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Composante principale 1")
ax.set_ylabel("Composante principale 2")
ax.legend(title="Thèmes", bbox_to_anchor=(1.05, 1))
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("reports/clustering_lecons.png", dpi=150,
            bbox_inches="tight")
plt.close()
print("✅ Graphique clustering sauvegardé")

print("\n✅ Script 02 NLP terminé avec succès !")
print(f"📁 Visualisations dans reports/")