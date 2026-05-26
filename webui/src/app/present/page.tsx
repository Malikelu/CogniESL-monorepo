import { Suspense } from "react";
import PresentClient from "./PresentClient";

export default function PresentPage() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center h-screen bg-black text-gray-400 text-sm">
        Loading…
      </div>
    }>
      <PresentClient />
    </Suspense>
  );
}
