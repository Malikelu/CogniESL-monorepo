import { cn } from "@/lib/utils";
import { ButtonHTMLAttributes, forwardRef } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
  asChild?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", children, ...props }, ref) => {
    return (
      <button ref={ref} className={cn(
        "inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
        {
          "bg-primary-500 text-white hover:bg-primary-600 shadow-glow hover:shadow-glow-lg": variant === "primary",
          "bg-secondary-500 text-white hover:bg-secondary-600": variant === "secondary",
          "border-2 border-primary-500 text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20": variant === "outline",
          "text-neutral-600 dark:text-neutral-300 hover:text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20": variant === "ghost",
        },
        {
          "px-4 py-2 text-sm": size === "sm",
          "px-6 py-3 text-base": size === "md",
          "px-8 py-4 text-lg": size === "lg",
        },
        className
      )} {...props}>
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";
