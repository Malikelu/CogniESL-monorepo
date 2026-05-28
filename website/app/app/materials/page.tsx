"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";
import { Container } from "@/components/ui/Container";

const API_URL = "https://cogniesl-production.up.railway.app";

interface Material {
  id: string;
  project_name: string;
  grammar_point: string;
  l1_languages: string;
  age_group: string;
  formats: string;
  slide_count: number;
  pptx_path: string | null;
  worksheet_pdf_path: string | null;
  worksheet_docx_path: string | null;
  activity_pdf_path: string | null;
  activity_docx_path: string | null;
  created_at: string;
  job_id: string | null;
}

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
                  <div>
                    <h2 className="font-semibold text-neutral-900 dark:text-neutral-50">{mat.project_name || mat.grammar_point}</h2>
                    <div className="flex flex-wrap gap-2 mt-1.5">
                      {mat.grammar_point && (
                        <span className="text-xs bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 rounded-full px-2.5 py-0.5">{mat.grammar_point}</span>
                      )}
                      {mat.l1_languages && (
                        <span className="text-xs bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400 rounded-full px-2.5 py-0.5">{mat.l1_languages}</span>
                      )}
                      {mat.age_group && (
                        <span className="text-xs bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400 rounded-full px-2.5 py-0.5">{mat.age_group}</span>
                      )}
                    </div>
                  </div>
                  <span className="text-xs text-neutral-400 shrink-0">{formatDate(mat.created_at)}</span>
                </div>
                {mat.job_id && (
                  <div className="flex flex-wrap gap-2 mt-3">
                    {mat.pptx_path && (
                      <a href={`${API_URL}/download/${mat.job_id}/${mat.pptx_path.split("/").pop()}`} className="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline">
                        📊 Slides (.pptx)
                      </a>
                    )}
                    {mat.worksheet_pdf_path && (
                      <a href={`${API_URL}/download/${mat.job_id}/${mat.worksheet_pdf_path.split("/").pop()}`} className="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline">
                        📄 Worksheet (.pdf)
                      </a>
                    )}
                    {mat.activity_pdf_path && (
                      <a href={`${API_URL}/download/${mat.job_id}/${mat.activity_pdf_path.split("/").pop()}`} className="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline">
                        🎮 Activity (.pdf)
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
