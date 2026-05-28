import { AppNavbar } from "@/components/layout/AppNavbar";

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex flex-col bg-neutral-50 dark:bg-neutral-950">
      <AppNavbar />
      <main className="flex-1">{children}</main>
    </div>
  );
}
