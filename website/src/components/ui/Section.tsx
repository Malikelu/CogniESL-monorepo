import { cn } from "@/lib/utils";

interface SectionProps {
  children: React.ReactNode;
  className?: string;
  id?: string;
  background?: "white" | "neutral" | "primary" | "dark";
}

export function Section({ children, className, id, background = "white" }: SectionProps) {
  return (
    <section
      id={id}
      className={cn(
        "py-16 sm:py-20 lg:py-24",
        {
          "bg-white dark:bg-neutral-900": background === "white",
          "bg-neutral-50 dark:bg-neutral-950": background === "neutral",
          "bg-primary-50 dark:bg-primary-950": background === "primary",
          "bg-neutral-900 text-white": background === "dark",
        },
        className
      )}
    >
      {children}
    </section>
  );
}
