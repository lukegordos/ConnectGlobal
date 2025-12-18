import myProfile from "../data/myProfile";

export default function Profile() {
  return (
    <div className="page-container">
      <h1>Your Profile</h1>

      <div className="profile-section">
        <h2>{myProfile.name}</h2>
        <p><strong>Email:</strong> {myProfile.email}</p>
        <p><strong>Country:</strong> {myProfile.country}</p>

        <h3>About Me</h3>
        <p>{myProfile.summary}</p>

        <h3>Skills</h3>
        <ul>
          {myProfile.skills.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>

        <h3>Experience</h3>
        <ul>
          {myProfile.experience.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>

      </div>
    </div>
  );
}
