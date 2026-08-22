"use client";

import { FileCode } from "lucide-react";

import CodeViewer from "@/components/pipeline/CodeViewer";
import MissingPipelineState from "@/components/pipeline/MissingPipelineState";
import { usePipelineArtifacts } from "@/hooks/usePipelineArtifacts";

export default function RTLPage() {
  const { latestPipelineResult, moduleName, artifacts, loading, error, isHydrated } =
    usePipelineArtifacts();

  if (!isHydrated) {
    return <p className="text-sm text-muted-foreground">Loading...</p>;
  }

  if (!latestPipelineResult || !moduleName) {
    return <MissingPipelineState />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="flex items-center gap-2 text-3xl font-bold">
          <FileCode className="h-7 w-7" />
          RTL Viewer
        </h1>
        <p className="mt-2 text-muted-foreground">
          Module: {artifacts?.module_name ?? moduleName}
        </p>
      </div>

      {error && (
        <p className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          {error}
        </p>
      )}

      <section className="rounded-xl border bg-card p-6 shadow-sm">
        <div className="mb-4">
          <h2 className="text-lg font-semibold">Generated RTL Source</h2>
          <p className="mt-1 break-all text-sm text-muted-foreground">
            {artifacts?.artifact_paths.rtl ?? "RTL artifact path unavailable."}
          </p>
        </div>

        {loading ? (
          <p className="text-sm text-muted-foreground">Loading RTL...</p>
        ) : (
          <CodeViewer
            code={artifacts?.rtl_source ?? null}
            emptyMessage="Generated RTL source is not available."
          />
        )}
      </section>
    </div>
  );
}
