import pandas as pd
from job_matcher import tfidf_similarity 
from networking import load_profiles, build_network, recommend_connections

def evaluate_job_matcher():
    jobs = pd.read_csv("../data/processed/job_postings_us_with_visa.csv")
    resumes = pd.read_csv("../data/raw/Resumes.csv")
    results = tfidf_similarity(jobs, resumes)

    print("Job Matcher Evaluation:\n")
    print(f" - Processed {len(jobs)} job postings\n")
    print(f" - Evaluated {len(resumes)} resumes\n")
    top_jobs = results.get(0, {}).get('top_jobs', [])
    if top_jobs:
        print(" - Example Output:\n", pd.DataFrame(top_jobs))
    else:
        print(" - Example Output: no matches found")

def evaluate_networking():
    df = load_profiles("../data/raw/fake_profiles.csv")
    G = build_network(df)

    print("Networking Evaluation:\n")
    print(f" - {G.number_of_nodes()} profiles\n")
    print(f" - {G.number_of_edges()} connections\n")

    recommendations = recommend_connections(G, df, student_id = 1)
    print(pd.DataFrame(recommendations))

if __name__ == "__main__":
        evaluate_job_matcher()
        evaluate_networking()
