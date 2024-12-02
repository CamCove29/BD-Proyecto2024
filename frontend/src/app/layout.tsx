import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "App Recuperando Música",
  description: "App Recuperando Música",
  icons: {
    icon: "/icons/icon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="bg-gray-900">{children}</body>
    </html>
  );
}


