import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar">
      <h2 className="logo">ConnectGlobal</h2>
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/job-matches">Job Matches</Link>
        <Link to="/networking">Networking</Link>
        <Link to="/profile">My Profile</Link>
      </div>
    </nav>
  );
}
