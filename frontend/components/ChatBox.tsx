import { useEffect, useState } from "react";
import api from "@/lib/api";
import Image from "next/image";

type Props = {
  persona: {
    id: number;
    name: string;
    personality_summary?: string;
    profile_url?: string;
  } | null;
};

type Message = {
  id: number;
  sender: string;
  content: string;
  created_at: string;
};

export default function ChatBox({ persona }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [showSummary, setShowSummary] = useState(false);

  useEffect(() => {
    if (!persona) return;
    api
      .get(`/chat/history?persona_id=${persona.id}`)
      .then((res) => setMessages(res.data))
      .catch(() => setMessages([]));
  }, [persona]);

  const handleSend = async () => {
    if (!input.trim() || !persona) return;
    const res = await api.post("/chat/send", {
      persona_id: persona.id,
      sender: "user",
      content: input,
    });
    setMessages((prev) => [...prev, ...res.data]);
    setInput("");
  };

  return (
    <div className="h-full flex flex-col">
      {/* 🔹 상단 - 프로필 정보 */}
      <div className="flex items-center justify-between px-4 py-2 border-b bg-white shadow">
        <div className="flex items-center gap-3">
          <Image
            src={persona?.profile_url || "/default-profile.png"}
            width={40}
            height={40}
            alt="profile"
            className="rounded-full object-cover hover:bg-gray-500"
            onClick={() => setShowSummary(true)}
          />
          <p className="font-semibold">{persona?.name}</p>
        </div>
      </div>

      {/* 🔹 채팅 메시지 영역 */}
      <div className="flex-1 overflow-y-auto px-4 py-2 space-y-3 bg-gray-50">
        {persona ? (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${
                msg.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-sm px-3 py-2 rounded-lg ${
                  msg.sender === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200 text-black"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))
        ) : (
          <p className="text-center text-gray-400">캐릭터를 선택해주세요.</p>
        )}
      </div>

      {/* 🔹 하단 입력창 */}
      {persona && (
        <div className="p-4 border-t bg-white flex gap-2">
          <input
            className="flex-1 border rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
            placeholder="메시지를 입력하세요"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            onClick={handleSend}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg"
          >
            보내기
          </button>
        </div>
      )}

      {/* 🔹 성격 요약 팝업 */}
      {showSummary && persona && (
        <div className="absolute top-16 right-4 bg-white shadow-xl border rounded p-4 max-w-sm z-50 bg-white dark:bg-black">
          <div className="flex justify-between mb-2">
            <p className="font-semibold">성격 요약</p>
            <button onClick={() => setShowSummary(false)}>❌</button>
          </div>
          <p className="text-sm text-gray-700 whitespace-pre-wrap">
            {persona.personality_summary || "요약 정보가 없습니다."}
          </p>
        </div>
      )}
    </div>
  );
}
