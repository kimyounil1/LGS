import type { NextConfig } from "next";
<<<<<<< HEAD

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
=======
module.exports = {
  images: {
    domains: ["localhost"],
  },
};
const nextConfig: NextConfig = {
  /* config options here */
>>>>>>> origin/master
};

export default nextConfig;
