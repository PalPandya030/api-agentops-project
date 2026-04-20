// ========================== IMPORTS ==========================
import { useState, useEffect } from "react";
import API from "./services/api";
import Auth from "./pages/Auth";
import { motion } from "framer-motion";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
} from "recharts";

// ========================== MAIN APP ==========================
export default function App() {

  // ========================== AUTH ==========================
  const [isAuth, setIsAuth] = useState(
    !!localStorage.getItem("token")
  );

  // ========================== UI STATES ==========================
  const [page, setPage] = useState("dashboard");
  const [theme, setTheme] = useState("dark");
  const [showChat, setShowChat] = useState(false);

  // ========================== DATA STATES ==========================
  const [input, setInput] = useState("");
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [analyticsData, setAnalyticsData] = useState([]);

  // ========================== CHAT STATES ==========================
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState([]);

  // ========================== HISTORY POLLING ==========================
  useEffect(() => {
  const interval = setInterval(async () => {
    try {
      const res = await API.get("/analytics");
      setAnalyticsData(res.data);
    } catch {}
  }, 2000); // live updates every 2s

  return () => clearInterval(interval);
  }, []);
  // ========================== ANALYSIS ==========================
  const handleSubmit = async () => {
    if (!input) return;

    setLoading(true);

    try {
      const res = await API.post(
        "/negotiate",
        null,
        { params: { user_input: input } }
      );
      setData(res.data);
    } catch {
      alert("Backend error");
    }

    setTimeout(() => setLoading(false), 800);
  };

  // ========================== CHAT FUNCTION ==========================
  const sendMessage = async () => {
    if (!chatInput) return;

    const userMsg = { role: "user", text: chatInput };

    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await API.post("/chat", {
        message: chatInput,
      });

      setMessages((prev) => [
        ...prev,
        { role: "ai", text: res.data.reply },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: "⚠️ AI error" },
      ]);
    }

    setChatInput("");
  };

  // ========================== AUTH CHECK ==========================
  if (!isAuth) return <Auth setIsAuth={setIsAuth} />;

  // ========================== UI ==========================
  return (
    <div
      className={`flex h-screen transition ${
        theme === "dark"
          ? "bg-gradient-to-br from-black via-gray-900 to-gray-950 text-white"
          : "bg-gray-100 text-black"
      }`}
    >

      {/* ========================== SIDEBAR ========================== */}
      <div className="w-64 p-6 bg-white/5 backdrop-blur-xl border-r border-white/10 flex flex-col justify-between">

        <div>
          <h2 className="text-2xl font-bold text-green-400 mb-8">
            AI Market
          </h2>

          <nav className="space-y-2">
            <button onClick={() => setPage("dashboard")}
              className={`w-full text-left p-2 rounded ${
                page === "dashboard"
                  ? "bg-green-500/20 text-green-400"
                  : "hover:bg-white/10"
              }`}
            >
              🧠 Dashboard
            </button>

            <button onClick={() => setPage("analytics")}
              className={`w-full text-left p-2 rounded ${
                page === "analytics"
                  ? "bg-green-500/20 text-green-400"
                  : "hover:bg-white/10"
              }`}
            >
              📊 Analytics
            </button>

            <button onClick={() => setPage("profile")}
              className={`w-full text-left p-2 rounded ${
                page === "profile"
                  ? "bg-green-500/20 text-green-400"
                  : "hover:bg-white/10"
              }`}
            >
              👤 Profile
            </button>
          </nav>

          {/* HISTORY */}
          <div className="mt-10">
            <h3 className="text-gray-400 mb-2">Recent Activity</h3>
            {history.length === 0 ? (
              <p className="text-xs text-gray-500">No activity</p>
            ) : (
              history.slice(0, 5).map((item, i) => (
                <div key={i} className="text-xs p-2 bg-white/5 rounded mb-2">
                  {item.selected_api} - ${item.final_price}
                </div>
              ))
            )}
          </div>
        </div>

        <button
          onClick={() => {
            localStorage.removeItem("token");
            setIsAuth(false);
          }}
          className="text-red-400"
        >
          Logout
        </button>
      </div>

      {/* ========================== MAIN ========================== */}
      <div className="flex-1 p-8 overflow-y-auto">

        {/* HEADER */}
        <div className="flex justify-between mb-6">
          <h1 className="text-3xl font-bold">AI Marketplace</h1>

          <div className="flex gap-3">
            <button
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              className="px-3 py-1 bg-white/10 rounded"
            >
              {theme === "dark" ? "🌞" : "🌙"}
            </button>

            <button
              onClick={() => setShowChat(!showChat)}
              className="bg-blue-500 px-3 py-1 rounded"
            >
              🤖 AI
            </button>
          </div>
        </div>

        {/* ========================== DASHBOARD ========================== */}
        {page === "dashboard" && (
          <>
            <input
              className="w-full p-3 bg-white/10 rounded mb-3"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="cheap fast api in india"
            />

            <button
              onClick={handleSubmit}
              className="bg-green-500 px-4 py-2 rounded"
            >
              Run Analysis
            </button>

            {/* LOADING */}
            {loading && (
              <div className="animate-pulse mt-4 space-y-3">
                <div className="h-20 bg-white/10 rounded"></div>
                <div className="h-20 bg-white/10 rounded"></div>
              </div>
            )}

            {/* RESULTS */}
            {data && !loading && (
              <>
                <div className="grid grid-cols-3 gap-4 mt-6">
                  {data.top_apis.map((api, i) => (
                    <motion.div key={i} whileHover={{ scale: 1.05 }}
                      className={`p-4 rounded ${
                        i === 0 ? "bg-green-500/20" : "bg-white/5"
                      }`}
                    >
                      {api.name} ⭐
                      <p>${api.price}</p>
                      <p>{api.latency} ms</p>
                    </motion.div>
                  ))}
                </div>

                <LineChart width={500} height={250} data={data.top_apis}>
                  <CartesianGrid stroke="#444" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Line dataKey="price" stroke="#22c55e" />
                </LineChart>

                <div className="mt-4 bg-white/5 p-4 rounded">
                  🤖 {data.explanation}
                </div>
              </>
            )}
          </>
        )}

        {/* ========================== ANALYTICS ========================== */}
{page === "analytics" && (
  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
    {!data ? (
      <p className="text-gray-400">
        Run analysis first to see analytics 📊
      </p>
    ) : (
      <>
        <h2 className="text-2xl font-bold mb-6">
          📊 Advanced Analytics Dashboard
        </h2>

        {/* ================= KPI CARDS ================= */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          <div className="p-5 bg-white/5 rounded-xl">
            <p className="text-gray-400 text-sm">Avg Price</p>
            <h2 className="text-2xl font-bold">
              $
              {Math.round(
                data.top_apis.reduce((a, b) => a + b.price, 0) /
                  data.top_apis.length
              )}
            </h2>
          </div>

          <div className="p-5 bg-white/5 rounded-xl">
            <p className="text-gray-400 text-sm">Best API</p>
            <h2 className="text-xl font-bold">
              {data.selected_api}
            </h2>
          </div>

          <div className="p-5 bg-white/5 rounded-xl">
            <p className="text-gray-400 text-sm">Fastest API</p>
            <h2 className="text-xl font-bold">
              {
                [...data.top_apis].sort(
                  (a, b) => a.latency - b.latency
                )[0].name
              }
            </h2>
          </div>

          <div className="p-5 bg-white/5 rounded-xl">
            <p className="text-gray-400 text-sm">Best Accuracy</p>
            <h2 className="text-xl font-bold">
              {Math.max(
                ...data.top_apis.map((a) => a.accuracy)
              )}
              %
            </h2>
          </div>
        </div>

        {/* ================= CHARTS ================= */}
        <div className="grid grid-cols-2 gap-6 mb-8">

          {/* PRICE TREND */}
          <div className="bg-white/5 p-4 rounded-xl">
            <h3 className="mb-2 text-sm text-gray-400">
              💰 Price Comparison
            </h3>

            <LineChart width={350} height={250} data={data.top_apis}>
              <CartesianGrid stroke="#444" />
              <XAxis dataKey="name" stroke="#aaa" />
              <YAxis stroke="#aaa" />
              <Tooltip />
              <Line dataKey="price" stroke="#22c55e" />
            </LineChart>
          </div>

          {/* LATENCY */}
          <div className="bg-white/5 p-4 rounded-xl">
            <h3 className="mb-2 text-sm text-gray-400">
              ⚡ Latency Comparison
            </h3>

            <BarChart width={350} height={250} data={data.top_apis}>
              <CartesianGrid stroke="#444" />
              <XAxis dataKey="name" stroke="#aaa" />
              <YAxis stroke="#aaa" />
              <Tooltip />
              <Bar dataKey="latency" fill="#3b82f6" />
            </BarChart>
          </div>
        </div>

        {/* ================= EXTRA CHART ================= */}
        <div className="bg-white/5 p-4 rounded-xl mb-8">
          <h3 className="mb-2 text-sm text-gray-400">
            🎯 Accuracy Distribution
          </h3>

          <BarChart width={700} height={250} data={data.top_apis}>
            <CartesianGrid stroke="#444" />
            <XAxis dataKey="name" stroke="#aaa" />
            <YAxis stroke="#aaa" />
            <Tooltip />
            <Bar dataKey="accuracy" fill="#f59e0b" />
          </BarChart>
        </div>

        {/* ================= SMART INSIGHTS ================= */}
        <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 p-6 rounded-xl border border-white/10">
          <h3 className="text-lg font-bold mb-3">
            🧠 Insights
          </h3>

          <ul className="text-sm space-y-2 text-gray-300">
            <li>
              • {data.selected_api} is the best overall API based on your requirements
            </li>

            <li>
              • Cheapest API:{" "}
              {
                [...data.top_apis].sort(
                  (a, b) => a.price - b.price
                )[0].name
              }
            </li>

            <li>
              • Fastest API:
              {
                [...data.top_apis].sort(
                  (a, b) => a.latency - b.latency
                )[0].name
              }
            </li>

            <li>
              • Most accurate API:
              {
                [...data.top_apis].sort(
                  (a, b) => b.accuracy - a.accuracy
                )[0].name
              }
            </li>
          </ul>
        </div>
      </>
    )}
  </motion.div>
)}
{/* ====================== PROFILE ====================== */}
{page === "profile" && (
  <div className="space-y-6">

    {/* HEADER */}
    <div>
      <h2 className="text-2xl font-bold">👤 Profile</h2>
      <p className="text-gray-400 text-sm">
        Manage your account & settings
      </p>
    </div>

    {/* USER CARD */}
    <div className="bg-white/5 p-6 rounded-xl border border-white/10 flex items-center gap-4">
      <div className="w-14 h-14 bg-green-500 rounded-full flex items-center justify-center text-lg font-bold">
        U
      </div>

      <div>
        <p className="font-semibold text-lg">User Name</p>
        <p className="text-gray-400 text-sm">user@example.com</p>
        <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded mt-1 inline-block">
          Free Plan
        </span>
      </div>
    </div>

    {/* STATS */}
    <div className="grid grid-cols-3 gap-4">

      <div className="bg-white/5 p-4 rounded-xl">
        <p className="text-gray-400 text-sm">Total Requests</p>
        <h2 className="text-xl font-bold">
          {analyticsData?.requests ?? 0}
        </h2>
      </div>

      <div className="bg-white/5 p-4 rounded-xl">
        <p className="text-gray-400 text-sm">Total Spend</p>
        <h2 className="text-xl font-bold text-green-400">
          ${analyticsData?.revenue ?? 0}
        </h2>
      </div>

      <div className="bg-white/5 p-4 rounded-xl">
        <p className="text-gray-400 text-sm">Top API</p>
        <h2 className="text-lg font-bold">
          {analyticsData?.usage
            ? Object.keys(analyticsData.usage)[0]
            : "N/A"}
        </h2>
      </div>

    </div>

    {/* SETTINGS */}
    <div className="bg-white/5 p-6 rounded-xl border border-white/10 space-y-4">

      <h3 className="font-semibold">⚙️ Settings</h3>

      {/* THEME */}
      <div className="flex justify-between items-center">
        <span>Theme</span>
        <button
          onClick={() =>
            setTheme(theme === "dark" ? "light" : "dark")
          }
          className="bg-white/10 px-3 py-1 rounded hover:bg-white/20"
        >
          {theme === "dark" ? "🌞 Light" : "🌙 Dark"}
        </button>
      </div>

      {/* UPGRADE */}
      <div className="flex justify-between items-center">
        <span>Upgrade Plan</span>
        <button className="bg-green-500 px-3 py-1 rounded hover:bg-green-600">
          Upgrade
        </button>
      </div>

      {/* LOGOUT */}
      <div className="flex justify-between items-center">
        <span>Logout</span>
        <button
          onClick={() => {
            localStorage.removeItem("token");
            setIsAuth(false);
          }}
          className="bg-red-500 px-3 py-1 rounded hover:bg-red-600"
        >
          Logout
        </button>
      </div>

    </div>

    {/* ACTIVITY */}
    <div className="bg-white/5 p-6 rounded-xl border border-white/10">
      <h3 className="font-semibold mb-3">📜 Recent Activity</h3>

      {analyticsData?.history && analyticsData.history.length > 0 ? (
        analyticsData.history.map((item, i) => (
          <div
            key={i}
            className="text-sm border-b border-white/10 py-2"
          >
            {item.query} → {item.selected_api} (${item.final_price})
          </div>
        ))
      ) : (
        <p className="text-gray-400 text-sm">
          No recent activity
        </p>
      )}
    </div>

  </div>
)}

      {/* ========================== CHAT PANEL ========================== */}
      {showChat && (
        <div className="fixed right-0 top-0 h-full w-80 bg-black border-l border-white/10 p-4 flex flex-col">

          {/* HEADER */}
          <div className="flex justify-between mb-3">
            <h2 className="font-bold">🤖 AI Assistant</h2>
            <button onClick={() => setShowChat(false)}>✖</button>
          </div>

          {/* MESSAGES */}
          <div className="flex-1 overflow-y-auto space-y-2">
            {messages.map((msg, i) => (
              <div key={i}
                className={`p-2 rounded ${
                  msg.role === "user"
                    ? "bg-green-500 ml-auto"
                    : "bg-white/10"
                }`}
              >
                {msg.text}
              </div>
            ))}
          </div>

          <input
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            className="mt-2 p-2 bg-white/10 rounded"
          />

          <button
            onClick={sendMessage}
            className="mt-2 bg-green-500 p-2 rounded"
          >
            Send
          </button>
        </div>
            )}

    </div>   
  </div>     

  );
}