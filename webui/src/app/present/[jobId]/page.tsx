// Compatibility shim — the real presenter is at /present?jobId=xxx.
// generateStaticParams must return at least one entry for output: 'export'.
// The dummy "_" page is never linked to; real /present/[jobId] URLs (if any
// old links exist) are redirected client-side by PresentRedirect below.
import PresentRedirect from "./PresentRedirect";

export function generateStaticParams() {
  return [{ jobId: "_" }];
}

export default function PresentPage() {
  return <PresentRedirect />;
}
