# =============================================================
# knowledge-mining-evaluations | LuxDev
# Script 03 : Tableau de bord — Rapport HTML synthétique
# Auteur : Serge-Alain NYAMSIN | github.com/sanyamsin
# Date : Avril 2026
# =============================================================
# Objectif : Générer un rapport HTML interactif synthétisant
# les leçons apprises et recommandations extraites
# =============================================================

import json
import pandas as pd
import numpy as np
import os

print("🔄 Génération du tableau de bord...")

# --- Chargement des données ----------------------------------
with open("data/rapports_evaluation.json", "r",
          encoding="utf-8") as f:
    rapports = json.load(f)

df_meta   = pd.read_csv("data/metadonnees_rapports.csv")
df_lecons = pd.read_csv("data/lecons_analysees.csv")

# --- Calculs synthétiques ------------------------------------
nb_rapports    = len(rapports)
nb_pays        = df_meta["pays"].nunique()
nb_secteurs    = df_meta["secteur"].nunique()
budget_total   = df_meta["budget_eur"].sum()
score_global   = df_meta["score_moyen"].mean()
nb_lecons      = len(df_lecons)

# Top leçons par secteur
top_lecons = {}
for secteur in df_lecons["secteur"].unique():
    lecons_secteur = df_lecons[df_lecons["secteur"] == secteur]["lecon"].tolist()
    top_lecons[secteur] = lecons_secteur[:3]

# Recommandations fréquentes
toutes_recommands = []
for r in rapports:
    toutes_recommands.extend(r["recommandations"])

from collections import Counter
recommands_freq = Counter(toutes_recommands).most_common(5)

# Scores OCDE/CAD moyens
scores_ocde = {
    "Impact":     np.mean([r["scores_ocde_cad"]["impact"]     for r in rapports]),
    "Efficience": np.mean([r["scores_ocde_cad"]["efficience"] for r in rapports]),
    "Pertinence": np.mean([r["scores_ocde_cad"]["pertinence"] for r in rapports]),
    "Durabilité": np.mean([r["scores_ocde_cad"]["durabilite"] for r in rapports]),
}

# --- Génération HTML -----------------------------------------
def score_color(score):
    if score >= 7:
        return "#27ae60"
    elif score >= 5:
        return "#f39c12"
    else:
        return "#e74c3c"

def score_bar(score, max_score=10):
    pct = (score / max_score) * 100
    color = score_color(score)
    return f"""
    <div style="background:#ecf0f1;border-radius:4px;height:12px;width:100%;">
        <div style="background:{color};width:{pct:.0f}%;height:12px;
                    border-radius:4px;"></div>
    </div>
    <small style="color:{color};font-weight:bold;">{score:.1f}/10</small>
    """

html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tableau de bord — Gestion des Connaissances Évaluation</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #f5f7fa;
            color: #2c3e50;
        }}
        header {{
            background: linear-gradient(135deg, #1F4E79, #2E86AB);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        header h1 {{ font-size: 2em; margin-bottom: 8px; }}
        header p  {{ opacity: 0.85; font-size: 1.05em; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 30px 20px; }}

        /* KPI Cards */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .kpi-card {{
            background: white;
            border-radius: 10px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-top: 4px solid #1F4E79;
        }}
        .kpi-card .value {{
            font-size: 2.2em;
            font-weight: bold;
            color: #1F4E79;
        }}
        .kpi-card .label {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 6px;
        }}

        /* Sections */
        .section {{
            background: white;
            border-radius: 10px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .section h2 {{
            color: #1F4E79;
            font-size: 1.3em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #D6E4F0;
        }}

        /* Scores OCDE */
        .scores-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}
        .score-item {{ padding: 10px 0; }}
        .score-item label {{
            font-weight: 600;
            display: block;
            margin-bottom: 6px;
            color: #2c3e50;
        }}

        /* Leçons */
        .secteur-block {{ margin-bottom: 24px; }}
        .secteur-titre {{
            background: #D6E4F0;
            color: #1F4E79;
            padding: 8px 14px;
            border-radius: 6px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .lecon-item {{
            background: #f8f9fa;
            border-left: 4px solid #1F4E79;
            padding: 10px 14px;
            margin-bottom: 8px;
            border-radius: 0 6px 6px 0;
            font-size: 0.95em;
            line-height: 1.5;
        }}

        /* Recommandations */
        .recommand-item {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 6px;
            margin-bottom: 10px;
        }}
        .recommand-num {{
            background: #1F4E79;
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.85em;
            flex-shrink: 0;
        }}

        /* Images */
        .viz-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .viz-grid img {{
            width: 100%;
            border-radius: 8px;
            border: 1px solid #ecf0f1;
        }}

        footer {{
            text-align: center;
            padding: 30px;
            color: #95a5a6;
            font-size: 0.9em;
        }}
        footer a {{ color: #1F4E79; text-decoration: none; }}
    </style>
</head>
<body>

<header>
    <h1>🧠 Gestion des Connaissances — Évaluation</h1>
    <p>Extraction automatique de leçons apprises depuis les rapports d'évaluation</p>
    <p style="margin-top:8px; opacity:0.7;">
        Serge-Alain NYAMSIN | Expert Évaluation & Data Science |
        <a href="https://github.com/sanyamsin"
           style="color:#BDD7EE;">github.com/sanyamsin</a>
    </p>
</header>

<div class="container">

    <!-- KPI Cards -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="value">{nb_rapports}</div>
            <div class="label">Rapports analysés</div>
        </div>
        <div class="kpi-card">
            <div class="value">{nb_lecons}</div>
            <div class="label">Leçons extraites</div>
        </div>
        <div class="kpi-card">
            <div class="value">{nb_pays}</div>
            <div class="label">Pays couverts</div>
        </div>
        <div class="kpi-card">
            <div class="value">{nb_secteurs}</div>
            <div class="label">Secteurs analysés</div>
        </div>
        <div class="kpi-card">
            <div class="value">{score_global:.1f}/10</div>
            <div class="label">Score OCDE/CAD moyen</div>
        </div>
        <div class="kpi-card">
            <div class="value">{budget_total/1e6:.1f}M€</div>
            <div class="label">Budget total analysé</div>
        </div>
    </div>

    <!-- Scores OCDE/CAD -->
    <div class="section">
        <h2>📊 Scores OCDE/CAD moyens</h2>
        <div class="scores-grid">
            {''.join(f"""
            <div class="score-item">
                <label>{critere}</label>
                {score_bar(score)}
            </div>
            """ for critere, score in scores_ocde.items())}
        </div>
    </div>

    <!-- Leçons apprises par secteur -->
    <div class="section">
        <h2>💡 Leçons apprises par secteur</h2>
        {''.join(f"""
        <div class="secteur-block">
            <div class="secteur-titre">📁 {secteur}</div>
            {''.join(f'<div class="lecon-item">✓ {lecon}</div>'
                     for lecon in lecons)}
        </div>
        """ for secteur, lecons in top_lecons.items())}
    </div>

    <!-- Recommandations fréquentes -->
    <div class="section">
        <h2>🎯 Recommandations les plus fréquentes</h2>
        {''.join(f"""
        <div class="recommand-item">
            <div class="recommand-num">{i+1}</div>
            <div>{recommand} <span style="color:#95a5a6;">
                ({freq}x)</span></div>
        </div>
        """ for i, (recommand, freq) in enumerate(recommands_freq))}
    </div>

    <!-- Visualisations -->
    <div class="section">
        <h2>📈 Visualisations</h2>
        <div class="viz-grid">
            <div>
                <p style="font-weight:600;margin-bottom:10px;">
                    WordCloud — Mots-clés</p>
                <img src="wordcloud_lecons.png"
                     alt="WordCloud leçons apprises">
            </div>
            <div>
                <p style="font-weight:600;margin-bottom:10px;">
                    Leçons par secteur</p>
                <img src="lecons_par_secteur.png"
                     alt="Leçons par secteur">
            </div>
            <div>
                <p style="font-weight:600;margin-bottom:10px;">
                    Clustering thématique</p>
                <img src="clustering_lecons.png"
                     alt="Clustering thématique">
            </div>
        </div>
    </div>

</div>

<footer>
    <p>Généré automatiquement avec Python & NLP |
       Serge-Alain NYAMSIN —
       <a href="https://github.com/sanyamsin">github.com/sanyamsin</a>
    </p>
</footer>

</body>
</html>
"""

# --- Sauvegarde ----------------------------------------------
os.makedirs("reports", exist_ok=True)
with open("reports/dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Tableau de bord HTML généré : reports/dashboard.html")
print("✅ Script 03 terminé avec succès !")