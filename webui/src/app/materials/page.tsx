"use client";

import { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";
import { AuthModal } from "@/components/AuthModal";
import { Navbar } from "@/components/Navbar";

const API_BASE = process.env.NEXT_PUBLIC_API_URL?.replace("/cogniesl/get_response", "") ?? "";

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

function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

function getFileLinks(mat: Material): { label: string; icon: string; href: string }[] {
  const links: { label: string; icon: string; href: string }[] = [];
  if (mat.job_id) {
    if (mat.pptx_path) {
      const fname = mat.pptx_path.split("/").pop() ?? "slides.pptx";
      links.push({ label: "Slides (.pptx)", icon: "📊", href: `/download/${mat.job_id}/${fname}` });
    }
    if (mat.worksheet_pdf_path) {
      const fname = mat.worksheet_pdf_path.split("/").pop() ?? "worksheet.pdf";
      links.push({ label: "Worksheet (.pdf)", icon: "📄", href: `/download/${mat.job_id}/${fname}` });
    }
    if (mat.worksheet_docx_path) {
      const fname = mat.worksheet_docx_path.split("/").pop() ?? "worksheet.docx";
      links.push({ label: "Worksheet (.docx)", icon: "📝", href: `/download/${mat.job_id}/${fname}` });
    }
    if (mat.activity_pdf_path) {
      const fname = mat.activity_pdf_path.split("/").pop() ?? "activity.pdf";
      links.push({ label: "Activity (.pdf)", icon: "🎮", href: `/download/${mat.job_id}/${fname}` });
    }
    if (mat.activity_docx_path) {
      const fname = mat.activity_docx_path.split("/").pop() ?? "activity.docx";
      links.push({ label: "Activity (.docx)", icon: "📝", href: `/download/${mat.job_id}/${fname}` });
    }
  }
  return links;
}

const FEEDBACK_TAGS = [
  { id: "wrong_level", label: "Wrong level" },
  { id: "l1_errors", label: "L1 errors" },
  { id: "missing_content", label: "Missing content" },
  { id: "wrong_grammar", label: "Wrong grammar" },
  { id: "formatting", label: "Formatting" },
];

function MaterialCard({ mat, onDelete }: { mat: Material; onDelete: (id: string) => void }) {
  const [deleting, setDeleting] = useState(false);
  const [feedbackRating, setFeedbackRating] = useState<string | null>(null);
  const [feedbackTags, setFeedbackTags] = useState<string[]>([]);
  const [feedbackSent, setFeedbackSent] = useState(false);

  const links = getFileLinks(mat);
  const l1s = mat.l1_languages ? mat.l1_languages.split(",").map((s) => s.trim()).filter(Boolean) : [];

  const handleDelete = async () => {
    if (!confirm(`Delete "${mat.grammar_point}" materials? This cannot be undone.`)) return;
    setDeleting(true);
    try {
      const token = localStorage.getItem("cogniesl_token");
      const res = await fetch(`${API_BASE}/api/materials/${mat.id}`, {
        method: "DELETE",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (res.ok) onDelete(mat.id);
    } finally {
      setDeleting(false);
    }
  };

  const submitFeedback = async (rating: string, tags: string[] = []) => {
    const token = localStorage.getItem("cogniesl_token");
    try {
      await fetch(`${API_BASE}/api/feedback`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          rating,
          tags,
          material_id: mat.id,
          job_id: mat.job_id ?? "",
          source: "materials_card",
        }),
      });
    } catch {
      // Fire-and-forget — don't bother the teacher if feedback fails
    }
    setFeedbackSent(true);
  };

  const handleRating = (rating: string) => {
    setFeedbackRating(rating);
    if (rating !== "issues") {
      submitFeedback(rating);
    }
  };

  const handleIssueSubmit = () => {
    if (feedbackRating === "issues") {
      submitFeedback("issues", feedbackTags);
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm hover:shadow-md transition-shadow">
      {/* Header row */}
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="min-w-0">
          <h3 className="font-semibold text-gray-900 text-sm leading-tight capitalize">
            {mat.grammar_point.replace(/_/g, " ")}
          </h3>
          <p className="text-xs text-gray-500 mt-0.5 capitalize">
            {mat.age_group} · {formatDate(mat.created_at)}
          </p>
        </div>
        <button
          onClick={handleDelete}
          disabled={deleting}
          title="Delete"
          className="flex-shrink-0 text-gray-300 hover:text-red-400 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
            <path fillRule="evenodd" d="M8.75 1A2.75 2.75 0 006 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 10.23 1.482l.149-.022.841 10.518A2.75 2.75 0 007.596 19h4.807a2.75 2.75 0 002.742-2.53l.841-10.52.149.023a.75.75 0 00.23-1.482A41.03 41.03 0 0014 4.193V3.75A2.75 2.75 0 0011.25 1h-2.5zM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4zM8.58 7.72a.75.75 0 00-1.5.06l.3 7.5a.75.75 0 101.5-.06l-.3-7.5zm4.34.06a.75.75 0 10-1.5-.06l-.3 7.5a.75.75 0 101.5.06l.3-7.5z" clipRule="evenodd" />
          </svg>
        </button>
      </div>

      {/* L1 badges */}
      {l1s.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-3">
          {l1s.map((l) => (
            <span key={l} className="text-[10px] bg-teal/10 text-teal rounded-full px-2 py-0.5 font-medium">
              {l}
            </span>
          ))}
        </div>
      )}

      {/* Slide count */}
      {mat.slide_count > 0 && (
        <p className="text-xs text-gray-400 mb-3">{mat.slide_count} slides</p>
      )}

      {/* Present button — primary action */}
      {mat.job_id && mat.slide_count > 0 && (
        <a
          href={`/present?jobId=${mat.job_id}`}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-center gap-1.5 w-full bg-[#0f172a] hover:bg-[#1e293b] text-white text-xs font-semibold py-2 rounded-xl mb-2.5 transition-colors"
        >
          <span>▶</span> Present
        </a>
      )}

      {/* Download links */}
      {links.length > 0 ? (
        <div className="flex flex-wrap gap-1.5">
          {links.map(({ label, icon, href }) => (
            <a
              key={href}
              href={href}
              download
              className="inline-flex items-center gap-1 bg-teal text-white text-[11px] font-semibold px-2.5 py-1.5 rounded-lg hover:bg-teal-dark transition-colors"
            >
              {icon} {label}
            </a>
          ))}
        </div>
      ) : (
        <p className="text-xs text-gray-400 italic">Files may no longer be available</p>
      )}

      {/* Feedback widget */}
      <div className="mt-3 pt-3 border-t border-gray-100">
        {feedbackSent ? (
          <p className="text-xs text-gray-400">Thanks for the feedback! 🙏</p>
        ) : !feedbackRating ? (
          <div className="flex items-center gap-1.5">
            <span className="text-[10px] text-gray-400 mr-0.5">How were these?</span>
            <button
              onClick={() => handleRating("perfect")}
              className="text-sm hover:scale-110 transition-transform"
              title="Perfect"
            >😍</button>
            <button
              onClick={() => handleRating("good")}
              className="text-sm hover:scale-110 transition-transform"
              title="Good"
            >👍</button>
            <button
              onClick={() => handleRating("issues")}
              className="text-sm hover:scale-110 transition-transform"
              title="Had issues"
            >👎</button>
          </div>
        ) : feedbackRating === "issues" && !feedbackSent ? (
          <div className="space-y-2">
            <p className="text-[10px] text-gray-500">What went wrong?</p>
            <div className="flex flex-wrap gap-1">
              {FEEDBACK_TAGS.map((t) => (
                <button
                  key={t.id}
                  onClick={() =>
                    setFeedbackTags((prev) =>
                      prev.includes(t.id) ? prev.filter((x) => x !== t.id) : [...prev, t.id]
                    )
                  }
                  className={`text-[10px] px-2 py-0.5 rounded-full border transition-colors ${
                    feedbackTags.includes(t.id)
                      ? "bg-red-50 border-red-300 text-red-600"
                      : "border-gray-200 text-gray-500 hover:border-gray-400"
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
            <button
              onClick={handleIssueSubmit}
              className="text-[10px] text-teal hover:underline"
            >
              Submit →
            </button>
          </div>
        ) : null}
      </div>

      {/* Regenerate link */}
      <div className="mt-2">
        <Link
          href={`/?regenerate=${encodeURIComponent(mat.grammar_point)}&l1=${encodeURIComponent(mat.l1_languages)}&age=${encodeURIComponent(mat.age_group)}`}
          className="text-xs text-gray-400 hover:text-teal hover:underline"
        >
          ↩ Regenerate
        </Link>
      </div>
    </div>
  );
}

interface UsageData {
  monthly_generations: number;
  tier_limit: number;
  subscription_tier: string;
}

export default function MaterialsPage() {
  const { user, loading, saveToken } = useAuth();
  const [materials, setMaterials] = useState<Material[]>([]);
  const [fetching, setFetching] = useState(false);
  const [showAuth, setShowAuth] = useState(false);
  const [filterGrammar, setFilterGrammar] = useState("");
  const [filterL1, setFilterL1] = useState("");
  const [usage, setUsage] = useState<UsageData | null>(null);

  const fetchMaterials = useCallback(async () => {
    const token = localStorage.getItem("cogniesl_token");
    if (!token) return;
    setFetching(true);
    try {
      const params = new URLSearchParams();
      if (filterGrammar) params.set("grammar_point", filterGrammar);
      if (filterL1) params.set("l1", filterL1);
      const [matRes, usageRes] = await Promise.all([
        fetch(`${API_BASE}/api/materials?${params}`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch(`${API_BASE}/api/auth/usage`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);
      if (matRes.ok) {
        const data = await matRes.json();
        setMaterials(data.materials ?? []);
      }
      if (usageRes.ok) {
        setUsage(await usageRes.json());
      }
    } finally {
      setFetching(false);
    }
  }, [filterGrammar, filterL1]);

  useEffect(() => {
    if (user) fetchMaterials();
  }, [user, fetchMaterials]);

  const handleDelete = (id: string) => {
    setMaterials((prev) => prev.filter((m) => m.id !== id));
  };

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Navbar />

      <main className="flex-1 max-w-4xl mx-auto w-full px-4 py-6">
        {/* Page title */}
        <div className="mb-6">
          <h1 className="text-2xl font-display font-bold text-gray-900">My Materials</h1>
          <p className="text-sm text-gray-500 mt-1">Download and manage your generated teaching materials.</p>
        </div>

        {/* Not logged in */}
        {!loading && !user && (
          <div className="text-center py-20">
            <div className="text-5xl mb-4">📚</div>
            <h2 className="text-lg font-semibold text-gray-800 mb-2">Sign in to see your materials</h2>
            <p className="text-sm text-gray-500 mb-6 max-w-sm mx-auto">
              Create a free account to save all your generated slides, worksheets, and activity guides.
            </p>
            <button
              onClick={() => setShowAuth(true)}
              className="bg-teal hover:bg-teal-dark text-white font-semibold px-6 py-2.5 rounded-xl text-sm transition-colors"
            >
              Sign In or Create Account
            </button>
          </div>
        )}

        {/* Logged in */}
        {!loading && user && (
          <>
            {/* Usage meter */}
            <div className="bg-white border border-gray-200 rounded-2xl p-4 mb-5 flex items-center gap-4">
              <div className="flex-1">
                <div className="flex items-center justify-between text-xs text-gray-600 mb-1.5">
                  <span>Generations this month</span>
                  <span className="font-semibold">
                    {usage ? `${usage.monthly_generations} / ${usage.tier_limit === 9999 ? "∞" : usage.tier_limit}` : "—"}
                  </span>
                </div>
                {usage && usage.tier_limit < 9999 && (
                  <div className="w-full bg-gray-100 rounded-full h-1.5">
                    <div
                      className="bg-teal h-1.5 rounded-full transition-all"
                      style={{ width: `${Math.min(100, (usage.monthly_generations / usage.tier_limit) * 100)}%` }}
                    />
                  </div>
                )}
                {usage && usage.subscription_tier === "free" && usage.monthly_generations >= usage.tier_limit && (
                  <p className="text-xs text-red-500 mt-1.5 font-medium">
                    Limit reached — <a href="/pricing" className="underline">upgrade to Pro</a> for 20 generations/month
                  </p>
                )}
              </div>
              {(!usage || usage.subscription_tier === "free") && (
                <span className="text-xs text-gray-400 bg-gray-50 border border-gray-200 rounded-full px-3 py-1 flex-shrink-0">
                  Free tier
                </span>
              )}
              {usage && usage.subscription_tier !== "free" && (
                <span className="text-xs text-teal bg-teal/10 border border-teal/20 rounded-full px-3 py-1 font-medium flex-shrink-0">
                  Pro
                </span>
              )}
            </div>

            {/* Filters */}
            <div className="flex flex-wrap gap-2 mb-5">
              <input
                type="text"
                placeholder="Filter by grammar point…"
                value={filterGrammar}
                onChange={(e) => setFilterGrammar(e.target.value)}
                className="text-sm border border-gray-300 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-teal focus:border-transparent"
              />
              <input
                type="text"
                placeholder="Filter by L1 language…"
                value={filterL1}
                onChange={(e) => setFilterL1(e.target.value)}
                className="text-sm border border-gray-300 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-teal focus:border-transparent"
              />
              {(filterGrammar || filterL1) && (
                <button
                  onClick={() => { setFilterGrammar(""); setFilterL1(""); }}
                  className="text-xs text-gray-500 hover:text-gray-700 px-3 py-2 rounded-xl hover:bg-gray-100 transition-colors"
                >
                  Clear filters
                </button>
              )}
            </div>

            {/* Grid */}
            {fetching && (
              <div className="flex justify-center py-12">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-teal rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-coral rounded-full animate-bounce [animation-delay:0.1s]" />
                  <div className="w-2 h-2 bg-gold rounded-full animate-bounce [animation-delay:0.2s]" />
                </div>
              </div>
            )}

            {!fetching && materials.length === 0 && (
              <div className="text-center py-16">
                <div className="text-4xl mb-3">✨</div>
                <h3 className="text-base font-semibold text-gray-700 mb-2">No materials yet</h3>
                <p className="text-sm text-gray-500 mb-5">
                  {filterGrammar || filterL1 ? "No materials match your filters." : "Generate your first set of teaching materials to see them here."}
                </p>
                <Link
                  href="/"
                  className="bg-teal hover:bg-teal-dark text-white font-semibold px-5 py-2.5 rounded-xl text-sm transition-colors"
                >
                  Generate Materials
                </Link>
              </div>
            )}

            {!fetching && materials.length > 0 && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {materials.map((mat) => (
                  <MaterialCard key={mat.id} mat={mat} onDelete={handleDelete} />
                ))}
              </div>
            )}
          </>
        )}
      </main>

      {showAuth && (
        <AuthModal
          onSuccess={(token, userData) => {
            saveToken(token, userData);
            setShowAuth(false);
          }}
          onClose={() => setShowAuth(false)}
        />
      )}
    </div>
  );
}
