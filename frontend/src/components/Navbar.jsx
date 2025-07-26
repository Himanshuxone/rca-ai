// src/components/Navbar.jsx
import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => (
  <nav style={styles.navbar}>
    <div style={styles.logo}>TechRCA</div>
    <div style={styles.links}>
      <Link to="/" style={styles.link}>Home</Link>
      <Link to="/dashboard" style={styles.link}>Dashboard</Link>
      <Link to="/events" style={styles.link}>Events</Link>
    </div>
  </nav>
);

const styles = {
  navbar: {
    backgroundColor: "#1f1f1f",
    display: "flex",
    justifyContent: "space-between",
    padding: "1rem 2rem",
    color: "white",
    position: "sticky",
    top: 0,
    zIndex: 10,
  },
  logo: { fontSize: "1.5rem", fontWeight: "bold" },
  links: { display: "flex", gap: "1.5rem" },
  link: { color: "white", textDecoration: "none" }
};

export default Navbar;
