import { useState } from "react";
import api, { setAuthToken } from "@/lib/api";
import { useRouter } from "next/router";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await api.post("/auth/login", { email, password });
      const token = res.data.access_token;
      localStorage.setItem("token", token);
      setAuthToken(token);
      router.push("/chat");
    } catch (err) {
      alert("로그인 실패");
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl mb-4">로그인</h1>
      <input
        type="email"
        placeholder="이메일"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="border p-2 mb-2 block"
      />
      <input
        type="password"
        placeholder="비밀번호"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="border p-2 mb-4 block"
      />
      <button onClick={handleLogin} className="bg-blue-500 text-white px-4 py-2">
        로그인
      </button>
      <p className="text-sm mt-2">
        아직 계정이 없나요?{" "}
        <a href="/signup" className="text-blue-500 underline">
            회원가입
        </a>
      </p>
    </div>
    
  );
}
