export default function ProfileCard({ name, company, country, skills, score }) {
  return (
    <div className="profile-card">
      <h3>{name}</h3>
      <p><strong>Company:</strong> {company}</p>
      <p><strong>Country:</strong> {country}</p>
      <p><strong>Skills:</strong> {skills}</p>

      {score !== undefined && (
        <p><strong>Score:</strong> {score}</p>
      )}
    </div>
  );
}
