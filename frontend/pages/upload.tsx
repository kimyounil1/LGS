import { useState } from "react";
import api, { setAuthToken } from "@/lib/api";
import { useRouter } from "next/router";

export default function UploadPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [mbti, setMbti] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const [profile, setProfile] = useState<File | null>(null);

  const handleUpload = async () => {
    if (!name || !file) {
      setError("이름과 파일은 필수입니다.");
      return;
    }

    const formData = new FormData();
    if (profile) formData.append("profile", profile);
    formData.append("name", name);
    if (mbti) formData.append("mbti", mbti);
    formData.append("file", file);

    try {
      const token = localStorage.getItem("token");
      if (token) setAuthToken(token);

      await api.post("/persona/upload", formData);
      alert("캐릭터 업로드 완료!");
      router.push("/chat");
    } catch (err: any) {
      setError(err.response?.data?.detail || "업로드 실패");
    }
  };
  

  return (
    <div className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">캐릭터 업로드</h1>

      {error && <p className="text-red-500 mb-2">{error}</p>}

      <input
        type="text"
        placeholder="이름 (예: 지은)"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="border p-2 mb-2 w-full"
      />
      <input
        type="text"
        placeholder="MBTI (선택)"
        value={mbti}
        onChange={(e) => setMbti(e.target.value)}
        className="border p-2 mb-2 w-full"
      />
      <p className="font-semibold">카카오톡 내역 추가하기(필수)</p>
      <input
        type="file"
        accept=".txt"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-4"
      />
      <p className="font-semibold">프로필 이미지 업로드(선택)</p>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setProfile(e.target.files?.[0] || null)}
        className="mb-4"
        />
        <br></br>
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 w-full rounded"
      >
        캐릭터 생성하기
      </button>
    </div>
  );
}
