# ConnectGlobal

> Intelligent job matching and professional networking — final project

## Project overview

ConnectGlobal is a prototype platform that matches job seekers to relevant job postings and suggests professional connections. It combines keyword-based retrieval (TF‑IDF), semantic embeddings (Sentence‑BERT), and graph/network analytics to produce ranked job and networking recommendations.

Key features
- Resume / profile text upload and extraction (TXT / PDF)
- TF‑IDF and BERT‑based candidate retrieval
- Graph-based connection recommendations (skill overlap + country boost)
- Simple API (FastAPI) and React frontend demo

## Repository structure

Top-level layout (important files/folders):

- `src/` — backend Python code (matching, preprocessing, APIs)
- `connectglobal-frontend/` — React UI for uploading resumes and showing matches
- `data/` — `raw/` and `processed/` CSV datasets (not committed if large)
- `requirements.txt` — Python dependencies
- `README.md` — this file

## Setup instructions (local development)

1. Clone the repo (after creating remote):

```bash
git clone git@github.com:<your-username>/ConnectGlobal.git
cd ConnectGlobal
```

2. Create and activate Python virtualenv (macOS / Linux):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. Frontend (React) setup

```bash
cd connectglobal-frontend
npm install
npm run start
```

4. Run backend API (from repository root):

```bash
source .venv/bin/activate
cd src
uvicorn main:app --reload
# or python preprocessing.py / job_matcher.py for offline runs
```

Notes
- Some heavy ML models (sentence-transformers, torch) will download model weights on first run — ensure you have network access and sufficient disk space.
- For reproducibility, pin the Python interpreter version (this project used Python 3.11+).

## Usage guide

1. Start backend API and frontend as above.
2. Open the frontend (usually `http://localhost:3000`), upload a resume (PDF or TXT) and click `Run Match`.
3. Frontend will call the backend endpoint and show TF‑IDF and BERT top matches, plus networking suggestions.

## AI models, libraries and tools used

- Sentence‑Transformers (SBERT) — `sentence-transformers` (embeddings, default: `all-MiniLM-L6-v2`)
- scikit-learn — `TfidfVectorizer` and cosine similarity
- networkx — graph creation and traversal for networking recommendations
- FastAPI / Uvicorn — backend API
- React — frontend UI

See `requirements.txt` for exact pinned versions used during development.

## Notes on data and privacy

- Do not commit real PII or resumes into the repository. Keep `data/raw` out of version control if it contains personal data.
- Add `.env` for secrets (none required for the demo). If you add API keys, store them in environment variables and list them in `.env.example`.

## How to publish this repo to GitHub

If you haven't created a remote repository yet, you can use GitHub CLI or the web UI. Example (recommended, using `gh` CLI):

```bash
# from repo root
git init
git add .
git commit -m "Initial commit - ConnectGlobal"
gh repo create lukegordos/ConnectGlobal --public --source=. --remote=origin
git push -u origin main
```

If you don't have `gh` installed, create an empty repo at `https://github.com/lukegordos` → `New repository`, then:

```bash
git remote add origin git@github.com:lukegordos/ConnectGlobal.git
git branch -M main
git push -u origin main
```

## Recommended next steps before pushing

- Review `.gitignore` (this repository contains a template file). Make sure large model files, data with PII, and virtualenvs are ignored.
- Optionally enable `git lfs` for any large artifacts.

## Troubleshooting

- If the React app fails due to pdf.js worker issues, check `connectglobal-frontend/src/pages/JobMatches.jsx` for the robust worker setup. The file attempts local import, then CDN fallback, then disables the worker as last resort.
- If you run into dependency version issues, you can create a clean environment and install a minimal set of packages required for your current workflow.

## License

Add a LICENSE file if you want to release with a particular license (e.g., MIT).

---
If you'd like, I can: (1) generate a `LICENSE` file, (2) create a `CONTRIBUTING.md`, (3) add a minimal GitHub Actions CI workflow to run lint/tests on push.
