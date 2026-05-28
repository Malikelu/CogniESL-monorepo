import { cn } from "@/lib/utils/cn";
import { type ReactNode } from "react";

interface ContainerProps {
  children: ReactNode;
  className?: string;
  narrow?: boolean;
  size?: "sm" | "md" | "lg" | "xl";
}

const sizeMap = {
  sm: "max-w-2xl",
  md: "max-w-4xl",
  lg: "max-w-6xl",
  xl: "max-w-7xl",
};

export function Container({ children, className, narrow = false, size }: ContainerProps) {
  const maxWidth = size ? sizeMap[size] : narrow ? "max-w-3xl" : "max-w-7xl";
  return (
    <div className={cn("w-full mx-auto px-4 sm:px-6 lg:px-8", maxWidth, className)}>
      {children}
    </div>
  );
}
