import { useRouter } from "next/router";
import Image from "next/image";

type Props = {
  personas: {
    id: number;
    name: string;
    mbti?: string;
    personality_summary?: string;
    profile_url?: string; // 이미지 URL
  }[];
};

export default function Sidebar({ personas }: Props) {
  const router = useRouter();
  const selectedId = Number(router.query.persona);

  const handleClick = (id: number) => {
    router.push(`/chat?persona=${id}`);
  };

  return (
    <div className="w-64 bg-gray-100 p-4 overflow-y-auto border-r">
      <h2 className="text-lg font-semibold mb-4">내 캐릭터</h2>

      {personas.length === 0 ? (
        <div className="text-gray-500">
          캐릭터가 없습니다. <br />
          <a href="/upload" className="text-blue-500 underline">
            캐릭터 만들기
          </a>
        </div>
      ) : (
        <ul className="space-y-2">
          {personas.map((p) => (
            <li
              key={p.id}
              onClick={() => handleClick(p.id)}
              className={`flex items-center gap-3 min-h-[48px] hover:bg-sky-200 p-1 rounded cursor-pointer ${
                selectedId === p.id ? "bg-blue-200" : "hover:bg-blue-100"
              }`}
            >
              <Image
                src={p.profile_url || "/default-profile.png"} // 없으면 기본 이미지
                alt={p.name}
                width={40}
                height={40}
                className="mx-auto block h-24 rounded-full sm:mx-0 sm:shrink-0"
              />
              <div>
                <p className="font-medium">{p.name} {p.mbti ?? "MBTI 미정"}</p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
