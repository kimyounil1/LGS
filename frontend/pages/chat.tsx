import Sidebar from "@/components/Sidebar";
import ChatBox from "@/components/ChatBox";
<<<<<<< HEAD
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import api, { setAuthToken } from "@/lib/api";
import Image from "next/image";

export default function ChatPage() {
  const router = useRouter();
  const [showAnalysis, setShowAnalysis] = useState(false);
=======
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import api, { setAuthToken } from "@/lib/api";

export default function ChatPage() {
  const router = useRouter();
>>>>>>> origin/master
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
<<<<<<< HEAD
        <div className="flex p-4 bg-white shadow text-xl font-semibold border-b">
          <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <button onClick={() => setShowAnalysis(true)} className="mr-2">
                <Image src="/analyze-icon.svg" alt="분석" width={24} height={24} />
              </button>
            </TooltipTrigger>
            <TooltipContent>대화 분석하기</TooltipContent>
          </Tooltip>
        </TooltipProvider>
          {selectedPersona ? selectedPersona.name : "캐릭터를 선택해주세요"}
          <a href="/upload" className="text-center ml-auto">
            캐릭터 추가하기
          </a>
          <Sheet open={showAnalysis} onOpenChange={setShowAnalysis}>
            <SheetContent side="right" className="w-[400px]">
              <SheetHeader>
                <SheetTitle>대화 분석</SheetTitle>
                <SheetDescription>
                  최근 대화를 업로드하거나 분석 결과를 확인하세요.
                </SheetDescription>
              </SheetHeader>

              <Textarea placeholder="대화 내용을 붙여넣거나 파일을 업로드하세요..." className="mt-4" />
              <Button className="mt-4 w-full">분석 시작</Button>
            </SheetContent>
        </Sheet>
=======
        <div className="p-4 bg-white shadow text-xl font-semibold border-b">
          {selectedPersona ? selectedPersona.name : "캐릭터를 선택해주세요"}
>>>>>>> origin/master
        </div>

        {/* 채팅 박스 */}
        <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
          <ChatBox persona={selectedPersona} />
        </div>

      </div>
    </div>
  );
}
