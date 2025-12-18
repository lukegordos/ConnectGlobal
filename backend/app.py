from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from src.job_matcher import match_from_text, tfidf_similarity, bert_similarity
from src.networking import build_network, recommend_connections
from pydantic import BaseModel

# -----------------------------------------------------------
# CREATE APP FIRST, ADD CORS BEFORE ANYTHING ELSE
# -----------------------------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------
# LOAD DATASETS
# -----------------------------------------------------------

print("Loading data...")
jobs_df = pd.read_csv("data/job_postings_us_with_visa.csv")
resumes_df = pd.read_csv("data/resumes.csv")
profiles_df = pd.read_csv("data/network_profiles.csv")

G = build_network(profiles_df)

# -----------------------------------------------------------
# ROUTES
# -----------------------------------------------------------

@app.get("/")
def home():
    return {"message": "ConnectGlobal API is running!"}

@app.get("/jobs")
def get_all_jobs():
    return jobs_df.to_dict(orient="records")

@app.get("/profiles")
def get_all_profiles():
    return profiles_df.to_dict(orient="records")

@app.get("/match/tfidf/{resume_id}")
def match_tfidf(resume_id: int, top_n: int = 5):
    return tfidf_similarity(jobs_df, resumes_df, resume_id, top_n)

@app.get("/match/bert/{resume_id}")
def match_bert(resume_id: int, top_n: int = 5):
    return bert_similarity(jobs_df, resumes_df, resume_id, top_n)

@app.get("/network/{student_id}")
def get_network_recommendations(student_id: int, top_n: int = 5):
    return recommend_connections(G, profiles_df, student_id, top_n)

class ResumeText(BaseModel):
    resume_text: str

@app.post("/match/from_text")
def match_from_text_endpoint(payload: ResumeText, top_n: int = 5):
    return match_from_text(jobs_df, payload.resume_text, top_n)

class CustomProfile(BaseModel):
    name: str
    country: str
    skills: list[str]


@app.post("/network/from_profile")
def match_custom_profile(profile: CustomProfile, top_n: int = 5):
    """
    Jaccard similarity between the custom user and all profiles.
    PLUS +0.3 bonus if same country.
    """
    import math

    # clean input skills
    user_skills = {s.strip().lower() for s in profile.skills}
    user_country = profile.country.strip().lower()

    matches = []

    for _, row in profiles_df.iterrows():
        other_skills = {s.strip().lower() for s in row["skills"].split(",")}
        other_country = row["country"].strip().lower()

        # jaccard skill similarity
        intersection = user_skills & other_skills
        union = user_skills | other_skills
        skill_score = len(intersection) / len(union) if len(union) > 0 else 0.0

        # country bonus
        country_bonus = 0.3 if user_country == other_country else 0.0

        final_score = round(skill_score + country_bonus, 3)

        matches.append({
            "name": row["name"],
            "company": row["company"],
            "country": row["country"],
            "skills": row["skills"],
            "score": final_score
        })

    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:top_n]
