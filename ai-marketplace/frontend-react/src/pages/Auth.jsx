import { useState } from "react";
import API from "../services/api";

export default function Auth({ setIsAuth }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async () => {
    try {
      const url = isLogin ? "/login" : "/signup";

      const res = await API.post(url, null, {
        params: { username, password },
      });

      if (res.data.token) {
        localStorage.setItem("token", res.data.token);
        setIsAuth(true);
      } else {
        alert(res.data.msg || res.data.error);
      }
    } catch {
      alert("Error connecting backend");
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-950 text-white">
      <div className="bg-white/5 p-6 rounded-xl w-80 border border-white/10">
        <h2 className="text-xl font-bold mb-4 text-center">
          {isLogin ? "Login" : "Signup"}
        </h2>

        <input
          className="w-full p-2 mb-3 bg-gray-800 rounded"
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          className="w-full p-2 mb-3 bg-gray-800 rounded"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleSubmit}
          className="w-full bg-green-500 py-2 rounded"
        >
          {isLogin ? "Login" : "Signup"}
        </button>

        <p
          className="text-sm text-center mt-3 cursor-pointer text-gray-400"
          onClick={() => setIsLogin(!isLogin)}
        >
          {isLogin ? "Create account" : "Already have account?"}
        </p>
      </div>
    </div>
  );
}