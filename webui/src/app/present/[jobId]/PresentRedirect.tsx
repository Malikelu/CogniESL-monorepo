"use client";
import { useEffect } from "react";
import { useParams } from "next/navigation";

export default function PresentRedirect() {
  const params = useParams();
  useEffect(() => {
    const jobId = params?.jobId;
    if (jobId && jobId !== "_") {
      window.location.replace(`/present?jobId=${jobId}`);
    }
  }, [params]);
  return (
    <div className="flex items-center justify-center h-screen bg-black text-gray-400 text-sm">
      Loading…
    </div>
  );
}
