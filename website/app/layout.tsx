import type { Metadata, Viewport } from "next";
import { inter, nunito } from "@/lib/fonts";
import { Providers } from "@/components/Providers";
import "./globals.css";

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#FAFAF9" },
    { media: "(prefers-color-scheme: dark)", color: "#0C0A09" },
  ],
};

export const metadata: Metadata = {
  metadataBase: new URL("https://www.cogniesl.com"),
  title: {
    default: "CogniESL — AI-Powered ESL Teaching Materials",
    template: "%s | CogniESL",
  },
  description:
    "Create custom ESL lesson materials in seconds. CogniESL uses AI with L1 interference intelligence to generate slides, worksheets, and activity guides — tailored to your students' native language.",
  keywords: [
    "ESL teaching materials", "ESL lesson planner", "AI for ESL teachers",
    "L1 interference", "ESL worksheets generator", "ESL slides generator",
    "TEFL tools", "TESOL resources", "ESL teacher AI",
    "English as a second language", "ESL activities", "ESL grammar",
  ],
  authors: [{ name: "CogniESL" }],
  creator: "CogniESL",
  publisher: "CogniESL",
  category: "Education",
  robots: {
    index: false,
    follow: false,
    noarchive: true,
    nosnippet: true,
    googleBot: {
      index: false,
      follow: false,
      noarchive: true,
      nosnippet: true,
    },
  },
  openGraph: {
    type: "website", locale: "en_US", url: "https://www.cogniesl.com",
    siteName: "CogniESL",
    title: "CogniESL — AI-Powered ESL Teaching Materials",
    description: "Create custom ESL lesson materials in seconds. AI with L1 interference intelligence.",
    images: [{ url: "/og-image.svg", width: 1200, height: 630, alt: "CogniESL — AI-Powered ESL Teaching Materials" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "CogniESL — AI-Powered ESL Teaching Materials",
    description: "Create custom ESL lesson materials in seconds. AI with L1 interference intelligence.",
    images: ["/og-image.svg"],
  },
  alternates: { canonical: "https://www.cogniesl.com" },
};

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "CogniESL",
  url: "https://www.cogniesl.com",
  logo: "https://www.cogniesl.com/icons/icon-512.svg",
  description: "AI-powered ESL teaching materials with L1 interference intelligence",
  foundingDate: "2025",
  industry: "Education Technology",
  sameAs: [],
};

const productJsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "CogniESL",
  applicationCategory: "EducationalApplication",
  operatingSystem: "Web",
  description: "AI-powered ESL teaching materials generator with L1 interference intelligence",
  offers: {
    "@type": "AggregateOffer",
    priceCurrency: "USD",
    lowPrice: "0",
    highPrice: "12",
    offerCount: "3",
  },
  aggregateRating: {
    "@type": "AggregateRating",
    ratingValue: "4.9",
    ratingCount: "0",
  },
};

const faqJsonLd = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: [
    {
      "@type": "Question",
      name: "How is CogniESL different from ChatGPT?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "CogniESL is purpose-built for ESL teachers. It understands L1 interference patterns, creates formatted classroom materials (PPTX, printable worksheets), and knows the specific challenges speakers of different languages face when learning English.",
      },
    },
    {
      "@type": "Question",
      name: "What does L1 interference mean?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "L1 interference (or language transfer) is when a student's native language affects how they learn English. CogniESL identifies these patterns and creates materials that specifically address them.",
      },
    },
    {
      "@type": "Question",
      name: "Do I need to know my students' native language?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "No! You just tell CogniESL what language your students speak, and it handles the rest. You'll learn about L1 interference patterns as you use the tool.",
      },
    },
    {
      "@type": "Question",
      name: "What L1 languages are supported?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "CogniESL supports 36 L1 languages including Spanish, Korean, Arabic, Mandarin, Japanese, Portuguese, Russian, Vietnamese, Hindi, French, German, and Tagalog.",
      },
    },
    {
      "@type": "Question",
      name: "Is CogniESL FERPA compliant?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Yes. CogniESL does not collect, store, or process any student personal information. No student data is ever transmitted.",
      },
    },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${nunito.variable}`} suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/favicon.svg" />
        <link rel="manifest" href="/manifest.json" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(productJsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
        />
      </head>
      <body className="font-body bg-neutral-50 text-neutral-900 antialiased">
        <script dangerouslySetInnerHTML={{ __html: `
(function() {
  var key = 'cogniesl_auth';
  var hash = 'd8e8fca2dc0f896fd7cb4cb0031ba249';
  try {
    if (localStorage.getItem(key) === hash) return;
  } catch(e) {}
  var pw = prompt('CogniESL - Private Site\\n\\nEnter password:');
  if (pw && pw.toLowerCase().trim() === 'cogniesl') {
    try { localStorage.setItem(key, hash); } catch(e) {}
    location.reload();
  } else {
    document.body.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100vh;background:#0a0a0a;color:#fafafa;font-family:system-ui,sans-serif;text-align:center;padding:2rem"><div><h1 style="font-size:1.5rem;font-weight:800;margin-bottom:1rem"><span style="color:#1cc">Cogni</span><span style="color:#2e8">ESL</span></h1><p style="color:rgba(250,250,250,.5)">Private site.<br>You need a password to access this website.</p></div></div>';
  }
})();
` }} />
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
