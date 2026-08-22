import Link from "next/link";
import { ClipboardList } from "lucide-react";

export default function MissingPipelineState() {
  return (
    <div className="rounded-xl border bg-card p-8 shadow-sm">
      <h1 className="text-2xl font-semibold">
        No pipeline result is currently loaded.
      </h1>

      <p className="mt-2 text-sm text-muted-foreground">
        Run the pipeline from the requirements page to view generated artifacts.
      </p>

      <Link
        href="/requirements"
        className="mt-6 inline-flex h-9 items-center gap-2 rounded-lg bg-primary px-3 text-sm font-medium text-primary-foreground hover:bg-primary/80"
      >
        <ClipboardList className="h-4 w-4" />
        Go to Requirements
      </Link>
    </div>
  );
}
