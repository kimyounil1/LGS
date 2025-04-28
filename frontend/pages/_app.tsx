import { AppProps } from "next/app";
import "@/styles/globals.css";  // 글로벌 CSS 파일 import

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
