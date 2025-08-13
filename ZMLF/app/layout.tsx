import type { Metadata } from "next";
import { Orbitron, Righteous } from "next/font/google";
import Script from 'next/script';
import "./globals.css";

const orbitron = Orbitron({ subsets: ["latin"] });
const righteous = Righteous({ 
  weight: '400',
  subsets: ["latin"],
  variable: '--font-righteous',
});

export const metadata: Metadata = {
  title: "Vita HealthInsight | AI",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${righteous.variable}`}>
      <head>
        <Script
          src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID}`}
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID}');
          `}
        </Script>
      </head>
      <body className={orbitron.className}>{children}</body>
    </html>
  );
} 