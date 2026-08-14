import type { ReactNode } from "react";

interface StatCardProps {
  title: string;
  value: string;
  icon?: ReactNode;
}

export default function StatCard({
  title,
  value,
  icon,
}: StatCardProps) {
  return (
    <div className="rounded-xl border bg-card p-6 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-sm font-medium text-muted-foreground">
          {title}
        </h3>

        {icon}
      </div>

      <p className="text-3xl font-bold">
        {value}
      </p>
    </div>
  );
}