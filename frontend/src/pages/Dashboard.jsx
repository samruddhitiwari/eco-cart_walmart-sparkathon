import api from "@/services/api";
import {
  PieChart, Pie, Cell,
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  LineChart, Line, CartesianGrid, Legend
} from 'recharts';

import { useEffect, useState } from 'react';
import { motion } from "framer-motion";

const COLORS = ['#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

function Dashboard() {
  const [stats, setStats] = useState(null);

 useEffect(() => {
  const stored = localStorage.getItem("ecoCart");
  const cartItems = stored ? JSON.parse(stored).map((item) => item.name) : [];

  fetch("https://eco-cart-api.onrender.com/analyze-cart", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ cart: cartItems }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("404 or other error");
      return res.json();
    })
    .then((data) => setStats(data))
    .catch((err) => {
      console.error("Failed to load dashboard stats:", err);
    });
}, []);



  if (!stats) return <p className="p-4 text-center">Loading dashboard data...</p>;

 const co2Data = stats.details.reduce((acc, item) => {
  const existing = acc.find((d) => d.name === item.category);
  if (existing) existing.value += item.carbon;
  else acc.push({ name: item.category, value: item.carbon });
  return acc;
}, []);


 const waterData = [
  { name: "Water", value: stats.waterUsage },
  { name: "Packaging", value: stats.packagingWaste },
];


  const scoreTrend = stats.details.map((item, i) => ({
  day: `Item ${i + 1}`,
  score: 100 - item.carbon / 10,
}));


  return (
    <motion.div
      className="min-h-screen bg-gradient-to-br from-green-50 to-white px-4 py-6 md:px-8 md:py-10 space-y-10"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <h2 className="text-3xl font-bold text-center text-green-800">
        📊 Sustainability Dashboard
      </h2>

      {/* Pie Chart: CO2 by category */}
      <div className="bg-white rounded-2xl shadow-md p-5 space-y-2">
        <h3 className="text-lg font-semibold text-center text-gray-800">CO₂ Contribution by Category</h3>
        <div className="w-full h-72">
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={co2Data}
                dataKey="value"
                nameKey="name"
                outerRadius={80}
                label
              >
                {co2Data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Bar Chart: Avg Water + Packaging */}
      {/* Bar Chart: Water & Packaging (Per Cart) */}
      <div className="bg-white rounded-2xl shadow-md p-5 space-y-2">
        <h3 className="text-lg font-semibold text-center text-gray-800">
          💧 Water & Packaging Impact (Your Cart)
        </h3>
        <div className="w-full h-72">
          <ResponsiveContainer>
            <BarChart data={waterData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#34D399" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>


      {/* Line Chart: Green Score Over Days */}
      <div className="bg-white rounded-2xl shadow-md p-5 space-y-2">
        <h3 className="text-lg font-semibold text-center text-gray-800">📈 Average Green Score Trend</h3>
        <div className="w-full h-72">
          <ResponsiveContainer>
            <LineChart data={scoreTrend}>
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Legend />
              <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
              <Line type="monotone" dataKey="score" stroke="#4F46E5" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </motion.div>
  );
}

export default Dashboard;
