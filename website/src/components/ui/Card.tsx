import { cn } from "@/lib/utils";
import { HTMLAttributes, forwardRef } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
  variant?: "default" | "bordered" | "elevated";
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, hover = false, variant = "default", children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "rounded-2xl p-6",
          {
            "bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800": variant === "default",
            "bg-white dark:bg-neutral-900 border-2 border-neutral-200 dark:border-neutral-700": variant === "bordered",
            "bg-white dark:bg-neutral-900 shadow-lg": variant === "elevated",
          },
          hover && "shadow-md hover:shadow-lg transition-all duration-300 hover:-translate-y-1",
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = "Card";
