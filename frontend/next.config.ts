import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ['@radix-ui/react-slot'],
  reactStrictMode: true,
  images: {
    domains: ["localhost"],
  },
  webpack: (config) => { // 타입 명시
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    };
    return config;
  },
};

export default nextConfig;
