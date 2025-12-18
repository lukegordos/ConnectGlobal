import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import JobMatches from "./pages/JobMatches";
import Networking from "./pages/Networking";
import Profile from "./pages/Profile";

import "./styles.css";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/job-matches" element={<JobMatches />} />
        <Route path="/networking" element={<Networking />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </BrowserRouter>
  );
}
