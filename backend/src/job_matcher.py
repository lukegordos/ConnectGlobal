import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from pathlib import Path


# ------------------------------------------
# SAFE STRING CLEANER
# ------------------------------------------
def safe_str(val):
    """Convert None, NaN, float nan, or 'nan' strings into clean empty strings."""
    if val is None:
        return ""
    if isinstance(val, float) and np.isnan(val):
        return ""
    if str(val).lower() == "nan":
        return ""
    return str(val)


# ------------------------------------------
# NORMALIZATION FUNCTION
# ------------------------------------------
def normalize_scores(scores):
    scores = np.array(scores, dtype=float)

    # Replace invalid values BEFORE normalization
    scores = np.nan_to_num(scores, nan=0.0, posinf=0.0, neginf=0.0)

    max_val = scores.max()
    min_val = scores.min()

    # Avoid divide-by-zero
    if max_val == min_val:
        return np.ones(len(scores)).tolist()

    norm = (scores - min_val) / (max_val - min_val)
    norm = np.nan_to_num(norm, nan=0.0)

    return norm.tolist()


# ------------------------------------------
# LOAD DATA
# ------------------------------------------
def load_data(jobs_path, resumes_path):
    jobs = pd.read_csv(jobs_path)
    resumes = pd.read_csv(resumes_path)

    # Build combined job text
    jobs["job_text"] = (
        jobs[["company_description", "job_description_text"]]
        .astype(str)
        .agg(" ".join, axis=1)
    )

    # Build combined resume text if missing
    if "text" not in resumes.columns:
        resumes["text"] = resumes[["skills", "education", "experience"]].astype(str).agg(
            " ".join, axis=1
        )

    return jobs, resumes


# ------------------------------------------
# TF-IDF MATCHING
# ------------------------------------------
def tfidf_similarity(jobs_df, resumes_df, resume_id=0, top_n=5):
    job_texts = jobs_df["job_text"].fillna("").tolist()
    resume_text = safe_str(resumes_df.iloc[resume_id]["text"])

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text] + job_texts)

    resume_vec = vectors[0]
    job_vecs = vectors[1:]

    sims = cosine_similarity(resume_vec, job_vecs)[0]
    sims = np.nan_to_num(sims, nan=0.0, posinf=0.0, neginf=0.0)
    sims = normalize_scores(sims)

    top_idx = np.argsort(sims)[::-1][:top_n]

    results = []
    for idx in top_idx:
        row = jobs_df.iloc[idx]
        results.append({
            "job_title": safe_str(row.get("job_title")),
            "company_name": safe_str(row.get("company_name")),
            "visa_sponsorship": safe_str(row.get("visa_sponsorship")),
            "similarity_score": float(sims[idx])
        })

    return results


# ------------------------------------------
# BERT MATCHING
# ------------------------------------------
def bert_similarity(jobs_df, resumes_df, resume_id=0, top_n=5):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    resume_emb = model.encode([safe_str(resumes_df.loc[resume_id, "text"])])[0]
    job_embs = model.encode(jobs_df["job_text"].astype(str).tolist())

    sims = cosine_similarity([resume_emb], job_embs)[0]
    sims = np.nan_to_num(sims, nan=0.0, posinf=0.0, neginf=0.0)
    sims = normalize_scores(sims)

    top_idx = np.argsort(sims)[::-1][:top_n]

    results = []
    for idx in top_idx:
        row = jobs_df.iloc[idx]
        results.append({
            "job_title": safe_str(row.get("job_title")),
            "company_name": safe_str(row.get("company_name")),
            "visa_sponsorship": safe_str(row.get("visa_sponsorship")),
            "similarity_score": float(sims[idx])
        })

    return results


# ------------------------------------------
# MATCH FROM FREE-TEXT INPUT
# ------------------------------------------
def match_from_text(jobs_df, resume_text, top_n=5):
    temp = pd.DataFrame([{"text": resume_text}])

    tfidf_res = tfidf_similarity(jobs_df, temp, 0, top_n)
    bert_res = bert_similarity(jobs_df, temp, 0, top_n)

    return {"tfidf": tfidf_res, "bert": bert_res}


# ------------------------------------------
# SELF-TEST
# ------------------------------------------
if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"

    jobs, resumes = load_data(
        DATA_DIR / "job_postings_us_with_visa.csv",
        DATA_DIR / "resumes.csv",
    )

    print(match_from_text(jobs, "Python SQL machine learning"))
