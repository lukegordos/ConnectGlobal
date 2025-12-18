export default function JobCard({ title, company, visa, score }) {
  return (
    <div className="job-card">
      <h3>{title}</h3>
      <p><strong>Company:</strong> {company}</p>
      <p><strong>Visa Sponsorship:</strong> {visa ? visa : "Unknown"}</p>
      {score !== undefined && <p><strong>Match Score:</strong> {score}</p>}
    </div>
  );
}
