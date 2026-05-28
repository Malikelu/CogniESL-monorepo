import { Hero } from "@/components/sections/Hero";
import { Problem } from "@/components/sections/Problem";
import { HowItWorks } from "@/components/sections/HowItWorks";
import { Features } from "@/components/sections/Features";
import { L1Explorer } from "@/components/sections/L1Explorer";
import { Samples } from "@/components/sections/Samples";
import { BlogPreview } from "@/components/sections/BlogPreview";
import { Pricing } from "@/components/sections/Pricing";
import { FAQ } from "@/components/sections/FAQ";
import { Waitlist } from "@/components/sections/Waitlist";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Hero />
      <Problem />
      <HowItWorks />
      <L1Explorer />
      <Features />
      <Samples />
      <BlogPreview />
      <Pricing />
      <FAQ />
      <Waitlist />
    </main>
  );
}
