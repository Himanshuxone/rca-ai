import { useEffect, useState } from "react";

export default function DarkModeToggle() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const storedTheme = localStorage.getItem("theme");
    if (storedTheme === "dark") {
      document.body.classList.add("dark");
      setDarkMode(true);
    }
  }, []);

  const toggleTheme = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    document.body.classList.toggle("dark", newMode);
    localStorage.setItem("theme", newMode ? "dark" : "light");
  };

  return (
    <button onClick={toggleTheme} className="dark-toggle">
      {darkMode ? "🌙 Dark Mode" : "☀️ Light Mode"}
    </button>
  );
}

const styles = {
  button: {
    padding: "0.5rem 1rem",
    backgroundColor: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: "0.5rem",
    cursor: "pointer",
    fontWeight: 600,
    marginBottom: "1rem",
  },
};
