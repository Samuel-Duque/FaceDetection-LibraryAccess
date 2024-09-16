import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

const geistInter = localFont({
  src: "./fonts/sentic/SenticTextBold.otf",
  variable: "--font-sentic-bold",
  // weight: "100 900",
});
const geistSentic = localFont({
  src: "./fonts/sentic/SenticTextBold.otf",
  variable: "--font-sentic-bold",
  // weight: "100 900",
});

export const metadata: Metadata = {
  title: "Reconhecimento Facial",
  description: "Uma aplicação de reconhecimento facial para bibilioteca",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistInter.variable} antialiased`}>{children}</body>
    </html>
  );
}
