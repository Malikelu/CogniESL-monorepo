import type { Metadata } from "next";
import { Inter, Nunito } from "next/font/google";
import Script from "next/script";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const nunito = Nunito({
  variable: "--font-nunito",
  subsets: ["latin"],
  weight: ["400", "600", "700"],
});

const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL || "https://cogniesl.com";

export const metadata: Metadata = {
  title: "CogniESL — AI-Powered ESL Teaching Materials",
  description: "Generate professional ESL teaching materials (slides, worksheets, activities) tailored to your students' language background.",
  openGraph: {
    title: "CogniESL — AI-Powered ESL Teaching Materials",
    description: "Generate slides, worksheets, and activities tailored to your students' native language in minutes.",
    url: BASE_URL,
    siteName: "CogniESL",
    images: [
      {
        url: `${BASE_URL}/og-image.png`,
        width: 1200,
        height: 630,
        alt: "CogniESL — AI-Powered ESL Teaching Materials",
      },
    ],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "CogniESL — AI-Powered ESL Teaching Materials",
    description: "Generate slides, worksheets, and activities tailored to your students' native language in minutes.",
    images: [`${BASE_URL}/og-image.png`],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${nunito.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        {children}
        {/* Plausible analytics — only active when NEXT_PUBLIC_PLAUSIBLE_DOMAIN is set */}
        {process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN && (
          <Script
            defer
            data-domain={process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN}
            src="https://plausible.io/js/script.js"
            strategy="afterInteractive"
          />
        )}
      </body>
    </html>
  );
}
