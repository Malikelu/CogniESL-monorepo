import { cn } from "@/lib/utils/cn";
import { type ReactNode } from "react";

type BadgeVariant = "standard" | "primary" | "secondary" | "success" | "accent" | "outline" | "new";

interface BadgeProps {
  variant?: BadgeVariant;
  children: ReactNode;
  className?: string;
}

const variantStyles: Record<BadgeVariant, string> = {
  standard: "bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300",
  primary: "bg-primary-500 text-white",
  secondary: "bg-secondary-100 text-secondary-700 dark:bg-secondary-900/30 dark:text-secondary-300",
  success: "bg-success-100 text-success-700 dark:bg-success-900/30 dark:text-success-300",
  accent: "bg-accent-100 text-accent-700 dark:bg-accent-900/30 dark:text-accent-300",
  outline: "border border-neutral-300 text-neutral-600 dark:border-neutral-600 dark:text-neutral-400",
  new: "bg-primary-500 text-white text-[11px] font-bold px-2 py-0.5 tracking-wider uppercase",
};

export function Badge({ variant = "standard", children, className }: BadgeProps) {
  return (
    <span className={cn("inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold", variantStyles[variant], className)}>
      {children}
    </span>
  );
}
