import { useState } from "react";
import api from "@/lib/api";
import { useRouter } from "next/router";

export default function SignupPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSignup = async () => {
    try {
      await api.post("/auth/signup", { email, password });
      alert("회원가입 완료! 로그인 해주세요.");
      router.push("/");  // 로그인 페이지로 이동
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || "회원가입 실패");
    }
  };

  return (
    <div className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">회원가입</h1>

      {error && <p className="text-red-500 mb-2">{error}</p>}

      <input
        type="email"
        placeholder="이메일"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="border p-2 mb-2 w-full"
      />
      <input
        type="password"
        placeholder="비밀번호"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="border p-2 mb-4 w-full"
      />
      <button
        onClick={handleSignup}
        className="bg-blue-600 text-white px-4 py-2 w-full rounded"
      >
        회원가입
      </button>
    </div>
  );
}
