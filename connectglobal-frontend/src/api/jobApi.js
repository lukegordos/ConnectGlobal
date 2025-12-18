// src/api/jobApi.js
const API_BASE = "http://127.0.0.1:8000";

export async function runMatchFromText(resumeText, topN = 5) {
  const res = await fetch(`${API_BASE}/match/from_text?top_n=${topN}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ resume_text: resumeText }),
  });

  if (!res.ok) {
    const text = await res.text();
    console.error("Backend error:", res.status, text);
    throw new Error(`Backend error ${res.status}: ${text}`);
  }

  return res.json();
}


