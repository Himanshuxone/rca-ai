// src/pages/Events.jsx
import React, { useEffect, useState } from "react";
import { fetchEvents } from "../services/api";

const Events = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const loadEvents = async () => {
      try {
        const data = await fetchEvents();
        console.log(data)
        setEvents(data);
      } catch (error) {
        console.error("Events API Error:", error.message);
      }
    };
    loadEvents();
  }, []);

  return (
    <div>
      <h2>Events</h2>
      {events.length === 0 ? (
        <p>No events found.</p>
      ) : (
        <ul>
          {events.map((evt) => (
            <li key={evt.id}>{evt.action}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Events;
