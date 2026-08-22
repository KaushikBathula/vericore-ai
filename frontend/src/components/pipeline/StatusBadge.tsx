import { CheckCircle, CircleAlert, CircleHelp } from "lucide-react";

interface StatusBadgeProps {
  success: boolean | null;
  label?: string;
}

export default function StatusBadge({
  success,
  label,
}: StatusBadgeProps) {
  if (success === null) {
    return (
      <span className="inline-flex items-center gap-1 rounded-md border px-2 py-1 text-xs font-medium text-muted-foreground">
        <CircleHelp className="h-3.5 w-3.5" />
        {label ?? "Unavailable"}
      </span>
    );
  }

  return (
    <span
      className={
        success
          ? "inline-flex items-center gap-1 rounded-md border border-emerald-200 bg-emerald-50 px-2 py-1 text-xs font-medium text-emerald-700"
          : "inline-flex items-center gap-1 rounded-md border border-red-200 bg-red-50 px-2 py-1 text-xs font-medium text-red-700"
      }
    >
      {success ? (
        <CheckCircle className="h-3.5 w-3.5" />
      ) : (
        <CircleAlert className="h-3.5 w-3.5" />
      )}
      {label ?? (success ? "Success" : "Failed")}
    </span>
  );
}
