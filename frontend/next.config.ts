import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
    async rewrites() {
      return [
        {
          source: "/api/:path*",
          destination: "http://backend:8000/:path*"
        }
      ]
    }
};

export default nextConfig;
