# =============================================================
# knowledge-mining-evaluations | LuxDev
# Script 01 : Génération de rapports d'évaluation simulés
# Auteur : Serge-Alain NYAMSIN | github.com/sanyamsin
# Date : Avril 2026
# =============================================================
# Objectif : Simuler des rapports d'évaluation de projets
# de développement pour alimenter le pipeline NLP
# Secteurs : Education, WASH, Gouvernance, Santé
# =============================================================

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# --- Données de base -----------------------------------------
PAYS = ["Niger", "Mali", "Burkina Faso", "Sénégal", "Mauritanie", "RCA"]
SECTEURS = ["Education & Emploi", "Eau & Assainissement",
            "Santé", "Gouvernance", "Environnement"]
BAILLEURS = ["LuxDev", "AFD", "UE/FED", "UNICEF", "ECHO", "Banque Mondiale"]
ORGANISATIONS = ["Action Contre la Faim", "Croix-Rouge",
                 "Handicap International", "CARE", "Oxfam"]

# --- Leçons apprises par secteur -----------------------------
LECONS_PAR_SECTEUR = {
    "Education & Emploi": [
        "L'implication des communautés locales dans la conception du programme a significativement amélioré le taux de participation.",
        "Le partenariat avec le secteur privé local a facilité l'insertion professionnelle des bénéficiaires.",
        "Les formations en compétences numériques ont augmenté l'employabilité des jeunes de 35%.",
        "L'approche genre a permis d'augmenter la participation des filles de 20 points de pourcentage.",
        "Le suivi post-formation est essentiel pour mesurer l'insertion durable à 12 mois.",
        "Les modules de formation doivent être adaptés aux réalités du marché du travail local.",
    ],
    "Eau & Assainissement": [
        "La maintenance communautaire des infrastructures est clé pour la durabilité des interventions.",
        "L'hygiène menstruelle doit être intégrée dans tous les programmes WASH scolaires.",
        "Les comités de gestion de l'eau formés localement assurent une meilleure pérennité.",
        "L'accès à l'eau potable réduit de 40% les maladies hydriques dans les zones d'intervention.",
        "La qualité de l'eau doit être testée régulièrement — les résultats doivent être partagés avec les communautés.",
    ],
    "Santé": [
        "Les agents de santé communautaires sont les maillons essentiels de la chaîne de santé primaire.",
        "L'intégration des services de santé maternelle et infantile améliore les taux de consultation.",
        "La rupture de stock en médicaments essentiels reste le principal obstacle à la qualité des soins.",
        "Les campagnes de vaccination mobiles atteignent mieux les populations nomades.",
        "Le renforcement des capacités du personnel soignant local assure la durabilité des résultats.",
    ],
    "Gouvernance": [
        "La transparence budgétaire renforce la confiance des citoyens envers les institutions locales.",
        "La décentralisation effective nécessite un transfert de ressources et pas seulement de compétences.",
        "Les mécanismes de redevabilité sociale renforcent la participation citoyenne.",
        "La formation des élus locaux améliore la qualité des services publics délivrés.",
        "Le dialogue entre société civile et autorités locales est un facteur clé de succès.",
    ],
    "Environnement": [
        "La reforestation participative avec les communautés assure une meilleure survie des plants.",
        "Les pratiques agro-écologiques améliorent les rendements tout en préservant les sols.",
        "L'adaptation au changement climatique doit être intégrée dès la formulation des projets.",
        "Les femmes sont les principales gardiennes des ressources naturelles dans les zones rurales.",
        "Les systèmes d'alerte précoce sécheresse réduisent significativement les pertes agricoles.",
    ],
}

RECOMMANDATIONS = [
    "Renforcer les mécanismes de suivi-évaluation participatif.",
    "Intégrer une approche genre systématique dès la conception.",
    "Développer des partenariats avec les autorités locales.",
    "Assurer la continuité du financement pour garantir la durabilité.",
    "Capitaliser les bonnes pratiques et les diffuser aux autres projets.",
    "Mettre en place un système de gestion des connaissances.",
    "Renforcer les capacités des équipes locales.",
    "Améliorer la coordination entre les acteurs humanitaires.",
]

# --- Génération des rapports ---------------------------------
def generer_rapport(id_rapport):
    secteur  = random.choice(SECTEURS)
    pays     = random.choice(PAYS)
    bailleur = random.choice(BAILLEURS)
    org      = random.choice(ORGANISATIONS)

    date_debut = datetime(2018, 1, 1) + timedelta(
        days=random.randint(0, 1500))
    duree_mois = random.randint(12, 48)
    budget_eur = random.randint(500000, 5000000)

    lecons      = random.sample(LECONS_PAR_SECTEUR[secteur],
                                k=random.randint(2, 4))
    recommands  = random.sample(RECOMMANDATIONS,
                                k=random.randint(2, 4))

    score_impact     = round(random.uniform(3.0, 9.5), 1)
    score_efficience = round(random.uniform(3.0, 9.5), 1)
    score_pertinence = round(random.uniform(5.0, 10.0), 1)
    score_durabilite = round(random.uniform(2.0, 8.0), 1)

    rapport = {
        "id":               id_rapport,
        "titre":            f"Évaluation {random.choice(['finale', 'mi-parcours', 'thématique'])} — "
                            f"Programme {secteur} au {pays}",
        "pays":             pays,
        "secteur":          secteur,
        "bailleur":         bailleur,
        "organisation":     org,
        "date_debut":       date_debut.strftime("%Y-%m-%d"),
        "duree_mois":       duree_mois,
        "budget_eur":       budget_eur,
        "scores_ocde_cad":  {
            "impact":       score_impact,
            "efficience":   score_efficience,
            "pertinence":   score_pertinence,
            "durabilite":   score_durabilite,
            "moyenne":      round(np.mean([score_impact, score_efficience,
                                           score_pertinence, score_durabilite]), 1)
        },
        "lecons_apprises":  lecons,
        "recommandations":  recommands,
        "texte_complet":    f"""
RAPPORT D'ÉVALUATION — {secteur.upper()} — {pays.upper()}

Bailleur : {bailleur} | Organisation : {org}
Budget : {budget_eur:,} EUR | Durée : {duree_mois} mois

LEÇONS APPRISES :
{chr(10).join(f'- {l}' for l in lecons)}

RECOMMANDATIONS :
{chr(10).join(f'- {r}' for r in recommands)}

SCORES OCDE/CAD :
- Impact : {score_impact}/10
- Efficience : {score_efficience}/10
- Pertinence : {score_pertinence}/10
- Durabilité : {score_durabilite}/10
        """.strip()
    }
    return rapport

# --- Génération de 50 rapports -------------------------------
print("🔄 Génération des rapports d'évaluation simulés...")
rapports = [generer_rapport(i+1) for i in range(50)]

# Sauvegarde JSON
os.makedirs("data", exist_ok=True)
with open("data/rapports_evaluation.json", "w",
          encoding="utf-8") as f:
    json.dump(rapports, f, ensure_ascii=False, indent=2)

# Sauvegarde CSV (métadonnées)
df = pd.DataFrame([{
    "id":           r["id"],
    "titre":        r["titre"],
    "pays":         r["pays"],
    "secteur":      r["secteur"],
    "bailleur":     r["bailleur"],
    "organisation": r["organisation"],
    "budget_eur":   r["budget_eur"],
    "duree_mois":   r["duree_mois"],
    "score_moyen":  r["scores_ocde_cad"]["moyenne"],
    "nb_lecons":    len(r["lecons_apprises"]),
    "nb_recommandations": len(r["recommandations"])
} for r in rapports])

df.to_csv("data/metadonnees_rapports.csv", index=False)

print(f"✅ {len(rapports)} rapports générés avec succès !")
print(f"📊 Secteurs couverts : {df['secteur'].nunique()}")
print(f"🌍 Pays couverts : {df['pays'].nunique()}")
print(f"💰 Budget moyen : {df['budget_eur'].mean():,.0f} EUR")
print(f"📁 Fichiers sauvegardés dans data/")