"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { Container } from "@/components/ui/Container";
import { type Material, getDownloadUrl } from "@/lib/api";

const API_URL = "https://cogniesl-production.up.railway.app";

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

export default function MaterialsPage() {
  const { isAuthenticated, loading: authLoading, token } = useAuth();
  const router = useRouter();
  const [materials, setMaterials] = useState<Material[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/app/signin");
    }
  }, [authLoading, isAuthenticated, router]);

  useEffect(() => {
    if (!isAuthenticated || !token) return;
    fetch(`${API_URL}/api/materials`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.ok ? r.json() : [])
      .then((data) => { setMaterials(data.materials ?? data ?? []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [isAuthenticated, token]);

  if (authLoading || (!isAuthenticated && !authLoading)) return null;

  return (
    <div className="min-h-[70vh] py-10">
      <Container size="lg">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-50">My Materials</h1>
            <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-1">All your generated teaching materials</p>
          </div>
          <Link
            href="/app"
            className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-primary-500 text-white hover:bg-primary-600 px-4 py-2 text-sm"
          >
            + New materials
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-20 text-neutral-400">Loading…</div>
        ) : materials.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-neutral-500 dark:text-neutral-400 mb-4">No materials yet.</p>
            <Link href="/app" className="text-primary-600 dark:text-primary-400 font-semibold hover:underline">
              Generate your first set →
            </Link>
          </div>
        ) : (
          <div className="grid gap-4">
            {materials.map((mat) => (
              <div key={mat.id} className="bg-white dark:bg-neutral-900 rounded-2xl border border-neutral-200 dark:border-neutral-800 p-5 shadow-sm">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <h2 className="font-semibold text-neutral-900 dark:text-neutral-50">{mat.grammar_point || mat.project_name}</h2>
                    <div className="flex flex-wrap gap-2 mt-1.5">
                      {mat.l1_languages && (
                        <span className="text-xs bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400 rounded-full px-2.5 py-0.5">{mat.l1_languages}</span>
                      )}
                      {mat.age_group && (
                        <span className="text-xs bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400 rounded-full px-2.5 py-0.5">{mat.age_group}</span>
                      )}
                      {mat.slide_count > 0 && (
                        <span className="text-xs bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 rounded-full px-2.5 py-0.5">{mat.slide_count} slides</span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <span className="text-xs text-neutral-400">{formatDate(mat.created_at)}</span>
                    <Link
                      href={`/app/materials/${mat.id}`}
                      className="inline-flex items-center gap-1.5 text-xs font-semibold bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 hover:bg-primary-100 dark:hover:bg-primary-900/40 border border-primary-200 dark:border-primary-800 rounded-lg px-3 py-1.5 transition-colors"
                    >
                      ✏️ Edit
                    </Link>
                  </div>
                </div>
                {mat.job_id && (
                  <div className="flex flex-wrap gap-3 mt-3 pt-3 border-t border-neutral-100 dark:border-neutral-800">
                    {mat.html_bundle_path && (
                      <a href={getDownloadUrl(mat.job_id, mat.html_bundle_path.split("/").pop()!)} className="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline">
                        🎬 Presentation (.html)
                      </a>
                    )}
                    {mat.pptx_path && (
                      <a href={getDownloadUrl(mat.job_id, mat.pptx_path.split("/").pop()!)} className="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline">
                        📊 Slides (.pptx)
                      </a>
                    )}
                    {mat.worksheet_pdf_path && (
                      <a href={getDownloadUrl(mat.job_id, mat.worksheet_pdf_path.split("/").pop()!)} className="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline">
                        📄 Worksheet (.pdf)
                      </a>
                    )}
                    {mat.worksheet_docx_path && (
                      <a href={getDownloadUrl(mat.job_id, mat.worksheet_docx_path.split("/").pop()!)} className="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline">
                        📄 Worksheet (.docx)
                      </a>
                    )}
                    {mat.activity_pdf_path && (
                      <a href={getDownloadUrl(mat.job_id, mat.activity_pdf_path.split("/").pop()!)} className="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline">
                        🎮 Activity (.pdf)
                      </a>
                    )}
                    {mat.flashcard_pdf_path && (
                      <a href={getDownloadUrl(mat.job_id, mat.flashcard_pdf_path.split("/").pop()!)} className="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline">
                        🃏 Flashcards (.pdf)
                      </a>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </Container>
    </div>
  );
}
