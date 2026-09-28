import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Trade Command Center",
  description: "Automated trading operations dashboard"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

