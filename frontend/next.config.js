const rawBackend = process.env.BACKEND_INTERNAL_URL || "http://127.0.0.1:8000";
const backendUrl =
  rawBackend.startsWith("http://") || rawBackend.startsWith("https://")
    ? rawBackend
    : `https://${rawBackend}`;

const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: `${backendUrl}/api/v1/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
