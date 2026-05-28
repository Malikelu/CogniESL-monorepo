import Link from "next/link";
import { Button } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-50 dark:bg-neutral-950 px-4">
      <div className="text-center max-w-md">
        <div className="text-6xl mb-6">🔍</div>
        <h1 className="font-heading text-3xl font-bold text-neutral-900 dark:text-neutral-50 mb-3">
          Page Not Found
        </h1>
        <p className="text-neutral-600 dark:text-neutral-400 mb-8 leading-relaxed">
          Sorry, we couldn&apos;t find the page you&apos;re looking for. It might have been moved or doesn&apos;t exist.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button size="lg" asChild>
            <Link href="/">Go Home</Link>
          </Button>
          <Button variant="outline" size="lg" asChild>
            <Link href="/blog">Read the Blog</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
