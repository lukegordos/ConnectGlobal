import { useEffect, useState } from "react";
import { getNetworkingMatchesFromProfile, getAllProfiles } from "../api/networkingApi";
import ProfileCard from "../components/ProfileCard";
import myProfile from "../data/myProfile";

export default function Networking() {

  const [matches, setMatches] = useState([]);
  const [allProfiles, setAllProfiles] = useState([]);

  useEffect(() => {
    async function loadEverything() {
      try {
        // Get top matches based on your hard-coded profile
        const recommended = await getNetworkingMatchesFromProfile(myProfile);
        setMatches(recommended);

        // Load entire directory
        const profiles = await getAllProfiles();
        setAllProfiles(profiles);

      } catch (error) {
        console.error("Networking API error:", error);
      }
    }

    loadEverything();
  }, []);

  return (
    <div className="page-container">
      <h1>Professional Networking</h1>
      <p>Your strongest networking matches and the full professional directory.</p>

      <hr />

      <h2>⭐ Your Top Matches</h2>
      <div className="list-container">
        {matches.length > 0 ? (
          matches.map((p, i) => (
            <ProfileCard
              key={i}
              name={p.name}
              company={p.company}
              country={p.country}
              skills={p.skills}
              score={p.score}
            />
          ))
        ) : (
          <p>No matches found yet.</p>
        )}
      </div>

      <hr />

      <h2>📘 All Profiles</h2>
      <div className="list-container">
        {allProfiles.length > 0 ? (
          allProfiles.map((p, i) => (
            <ProfileCard
              key={i}
              name={p.name}
              company={p.company}
              country={p.country}
              skills={p.skills}
              score={p.score}
            />
          ))
        ) : (
          <p>Loading profiles...</p>
        )}
      </div>
    </div>
  );
}
