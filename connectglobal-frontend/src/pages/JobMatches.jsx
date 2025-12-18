import React, { useState } from "react";
import { runMatchFromText } from "../api/jobApi";

export default function JobMatches() {
  const [resumeFile, setResumeFile] = useState(null);
  const [results, setResults] = useState(null);

  // Extract text from PDF or TXT
  const extractText = (file) => {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.readAsText(file);
    });
  };

  const handleRun = async () => {
    if (!resumeFile) {
      alert("Upload a resume first!");
      return;
    }

    let text = await extractText(resumeFile);
    const response = await runMatchFromText(text);

    setResults(response);
  };

  return (
    <div className="page-container">
      <h1>Upload Resume to Find Matching Jobs</h1>

      <input
        type="file"
        accept=".pdf,.txt"
        onChange={(e) => setResumeFile(e.target.files[0])}
      />

      <button onClick={handleRun} style={{ marginLeft: "10px" }}>
        Run Match
      </button>

      <hr />

      {results && (
        <div>
            <h2>TF-IDF Matches</h2>
            {results.tfidf.map((job, i) => (
            <div key={i} className="job-card">
                <h3>{job.job_title}</h3>
                <p>{job.company_name}</p>
                <p>Sponsorship: {job.visa_sponsorship}</p>
                <p>Score: {job.similarity_score.toFixed(3)}</p>
            </div>
            ))}

            <h2>BERT Matches</h2>
            {results.bert.map((job, i) => (
            <div key={i} className="job-card">
                <h3>{job.job_title}</h3>
                <p>{job.company_name}</p>
                <p>Sponsorship: {job.visa_sponsorship}</p>
                <p>Score: {job.similarity_score.toFixed(3)}</p>
            </div>
            ))}
        </div>
        )}

    </div>
  );
}
