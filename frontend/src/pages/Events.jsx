import React, { useEffect, useState } from "react";
import { fetchEvents } from "../services/api";
import {
  CalendarDays,
  Globe,
  Shield,
  Hash,
  Clock,
  FileText,
  Package,
} from "lucide-react";

const getCardColors = (action) => {
  switch (action) {
    case "ACCEPT":
      return {
        border: "border-green-500",
        badge: "bg-green-600",
        shadow: "shadow-green-500/30",
      };
    case "REJECT":
      return {
        border: "border-red-500",
        badge: "bg-red-600",
        shadow: "shadow-red-500/30",
      };
    case "DROP":
      return {
        border: "border-yellow-500",
        badge: "bg-yellow-600",
        shadow: "shadow-yellow-500/30",
      };
    default:
      return {
        border: "border-gray-500",
        badge: "bg-gray-600",
        shadow: "shadow-gray-500/30",
      };
  }
};

const badgeHover = {
  ACCEPT: "hover:bg-green-700",
  REJECT: "hover:bg-red-700",
  DROP: "hover:bg-yellow-600",
};

const getBadgeClass = (action) => {
  switch (action) {
    case 'ACCEPT':
      return 'badge accept';
    case 'REJECT':
      return 'badge reject';
    case 'DROP':
      return 'badge drop';
    default:
      return 'badge default';
  }
};


const Events = () => {
  const [events, setEvents] = useState([]);
  const [filteredEvents, setFilteredEvents] = useState([]);
  const [filterAction, setFilterAction] = useState("all");

  useEffect(() => {
    const loadEvents = async () => {
      try {
        const data = await fetchEvents();
        setEvents(data);
        setFilteredEvents(data);
      } catch (error) {
        console.error("Events API Error:", error.message);
      }
    };
    loadEvents();
  }, []);

  useEffect(() => {
    if (filterAction === "all") {
      setFilteredEvents(events);
    } else {
      const filtered = events.filter((evt) => evt.action === filterAction);
      setFilteredEvents(filtered);
    }
  }, [filterAction, events]);

  return (
    <div className="min-h-screen px-6 py-12 bg-gradient-to-br from-gray-950 to-gray-800 text-white">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
          <h2 className="text-4xl font-extrabold flex items-center gap-3">
            <CalendarDays className="w-10 h-10 text-cyan-400" />
            Event Logs
          </h2>

          <select
            value={filterAction}
            onChange={(e) => setFilterAction(e.target.value)}
            className="bg-gray-800 border-2 border-cyan-600 text-lg text-cyan-200 px-5 py-3 rounded-xl shadow-lg hover:border-cyan-400 focus:outline-none focus:ring focus:ring-cyan-500 transition duration-300"
          >
            <option value="all">🌐 All Actions</option>
            <option value="ACCEPT">✅ ACCEPT</option>
            <option value="REJECT">⛔ REJECT</option>
            <option value="DROP">🟡 DROP</option>
          </select>
        </div>

        {filteredEvents.length === 0 ? (
          <div className="text-xl text-gray-300 text-center mt-20">🚫 No events found.</div>
        ) : (
          <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredEvents.map((evt) => {
              const { border, badge, shadow } = getCardColors(evt.action);
              return (
                <li
                  key={evt.id}
                  className={`bg-gray-900 p-6 rounded-2xl border-l-4 ${border} shadow-xl ${shadow} hover:scale-[1.02] transform transition-all duration-300`}
                >
                  <div className="flex justify-between items-center mb-4">
                    <span className="text-2xl font-bold text-white">Event #{evt.id}</span>
                    <span className={getBadgeClass(evt.action)}>
                      {evt.action}
                    </span>
                  </div>
                  <div className="space-y-3 text-lg text-gray-200">
                    <p className="flex items-center gap-3">
                      <Globe className="w-6 h-6 text-cyan-400" />
                      <span className="font-semibold text-white">Source:</span> {evt.srcaddr}:{evt.srcport}
                    </p>
                    <p className="flex items-center gap-3">
                      <Globe className="w-6 h-6 text-cyan-400" />
                      <span className="font-semibold text-white">Destination:</span> {evt.dstaddr}:{evt.dstport}
                    </p>
                    <p className="flex items-center gap-3">
                      <Shield className="w-6 h-6 text-cyan-400" />
                      <span className="font-semibold text-white">Log Status:</span> {evt.log_status}
                    </p>
                    <p className="flex items-center gap-3">
                      <Package className="w-6 h-6 text-cyan-400" />
                      <span className="font-semibold text-white">Version:</span> {evt.version}
                    </p>
                    <p className="flex items-center gap-3">
                      <Clock className="w-6 h-6 text-cyan-400" />
                      <span className="font-semibold text-white">Start Time:</span> {new Date(evt.start_time).toLocaleString()}
                    </p>
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Events;
