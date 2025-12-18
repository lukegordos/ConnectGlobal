import networkx as nx
import pandas as pd

print("🔥 NETWORKING MODULE LOADED:", __file__)
print("🔥 RUNNING UPDATED NETWORKING CODE")


def build_network(df):
    G = nx.Graph()

    for _, row in df.iterrows():
        skills = [s.strip().lower() for s in row["skills"].split(",")]

        G.add_node(
            row["id"],
            name=row["name"],
            company=row["company"],
            country=row["country"],
            skills=skills,
        )
    return G


def compute_similarity(profile, other):
    skills_a = set(profile["skills"])
    skills_b = set(other["skills"])

    # ----- Jaccard skill similarity -----
    union = skills_a.union(skills_b)
    shared = skills_a.intersection(skills_b)

    if len(union) == 0:
        skill_score = 0
    else:
        skill_score = len(shared) / len(union)

    # ----- Bonus for same country -----
    country_bonus = 0.3 if profile["country"].lower() == other["country"].lower() else 0

    final = round(skill_score + country_bonus, 3)

    # DEBUG print so we know it's using the new logic
    print(f"[SIM] {other['name']} | shared={shared} | skill_score={skill_score:.3f} | bonus={country_bonus} | final={final}")

    return final


def recommend_connections(G, profiles_df, user_profile, top_n=5):
    print("🔥 recommend_connections CALLED")

    # Normalize user info
    user_country_raw = str(user_profile["country"]).strip().lower()
    user_skills = {s.strip().lower() for s in user_profile["skills"]}

    # Normalization map
    country_aliases = {
        "united kingdom": "uk",
        "england": "uk",
        "scotland": "uk",
        "wales": "uk",
        "northern ireland": "uk",
        "u.k.": "uk",
        "uk": "uk",
    }

    def normalize_country(c):
        c = str(c).strip().lower()
        return country_aliases.get(c, c)

    user_country = normalize_country(user_country_raw)
    profiles_df["country_clean"] = profiles_df["country"].apply(normalize_country)

    print("DEBUG user_country:", user_country)
    print("DEBUG csv countries:", profiles_df["country_clean"].unique())

    def clean(skills):
        return {s.strip().lower() for s in skills.split(",") if s.strip()}

    profiles_df["clean_skills"] = profiles_df["skills"].apply(clean)

    def jaccard(a, b):
        return len(a & b) / len(a | b) if a and b else 0.0

    def compute_score(row):
        skill_score = jaccard(user_skills, row["clean_skills"])
        country_bonus = 0.3 if row["country_clean"] == user_country else 0.0
        final = round(skill_score + country_bonus, 3)
        print(f"[SCORE] {row['name']} | skill={skill_score:.3f} | bonus={country_bonus} | final={final}")
        return final

    profiles_df["score"] = profiles_df.apply(compute_score, axis=1)

    ranked = profiles_df.sort_values("score", ascending=False)
    return ranked.head(top_n)[["name", "company", "country", "skills", "score"]].to_dict(orient="records")
