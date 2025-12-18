const BASE_URL = "http://127.0.0.1:8000";

export async function getNetworkingRecommendations(studentId) {
  const res = await fetch(`${BASE_URL}/network/${studentId}`);
  return res.json();
}

export async function getAllProfiles() {
  const res = await fetch(`${BASE_URL}/profiles`);
  return res.json();
}

export async function getNetworkingMatchesFromProfile(myProfile) {
  const res = await fetch(`${BASE_URL}/network/from_profile`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(myProfile)
  });

  return res.json();
}