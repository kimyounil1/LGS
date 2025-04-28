import Sidebar from "@/components/Sidebar";
import ChatBox from "@/components/ChatBox";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import api, { setAuthToken } from "@/lib/api";

export default function ChatPage() {
  const router = useRouter();
  const { persona } = router.query;
  const [personas, setPersonas] = useState([]);
  const [selectedPersona, setSelectedPersona] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) setAuthToken(token);

    api.get("/persona/list").then((res) => {
      setPersonas(res.data);
      if (persona) {
        const found = res.data.find((p: any) => p.id === Number(persona));
        if (found) setSelectedPersona(found);
      }
    });
  }, [persona]);
  
  return (
    <div className="flex h-screen">
      {/* 🔹 좌측 고정 사이드바 */}
      <Sidebar personas={personas} />

      {/* 🔹 우측 채팅 영역 전체 */}
      <div className="flex flex-col flex-1 overflow-hidden">
        {/* 상단 캐릭터 이름 */}
        <div className="p-4 bg-white shadow text-xl font-semibold border-b">
          {selectedPersona ? selectedPersona.name : "캐릭터를 선택해주세요"}
        </div>

        {/* 채팅 박스 */}
        <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
          <ChatBox persona={selectedPersona} />
        </div>

      </div>
    </div>
  );
}
