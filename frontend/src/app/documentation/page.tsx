"use client";

import { BookOpen, Download } from "lucide-react";

import CodeViewer from "@/components/pipeline/CodeViewer";
import MissingPipelineState from "@/components/pipeline/MissingPipelineState";
import { usePipelineArtifacts } from "@/hooks/usePipelineArtifacts";
import { getArtifactUrl } from "@/services/pipelineService";

export default function DocumentationPage() {
  const {
    latestPipelineResult,
    moduleName,
    artifacts,
    loading,
    error,
    isHydrated,
  } = usePipelineArtifacts();

  if (!isHydrated) {
    return <p className="text-sm text-muted-foreground">Loading...</p>;
  }

  if (!latestPipelineResult || !moduleName) {
    return <MissingPipelineState />;
  }

  const documentationUrl = getArtifactUrl(
    artifacts?.download_urls.documentation ?? null,
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          <h1 className="flex items-center gap-2 text-3xl font-bold">
            <BookOpen className="h-7 w-7" />
            Documentation
          </h1>
          <p className="mt-2 text-muted-foreground">
            Module: {moduleName}
          </p>
        </div>

        {documentationUrl && (
          <a
            href={documentationUrl}
            className="inline-flex h-9 items-center gap-2 rounded-lg border bg-background px-3 text-sm font-medium hover:bg-muted"
          >
            <Download className="h-4 w-4" />
            Download Report
          </a>
        )}
      </div>

      {error && (
        <p className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          {error}
        </p>
      )}

      <section className="rounded-xl border bg-card p-6 shadow-sm">
        <div className="mb-4">
          <h2 className="text-lg font-semibold">
            Generated Markdown Report
          </h2>
          <p className="mt-1 break-all text-sm text-muted-foreground">
            {artifacts?.artifact_paths.documentation ?? "Unavailable"}
          </p>
        </div>

        {loading ? (
          <p className="text-sm text-muted-foreground">
            Loading documentation...
          </p>
        ) : (
          <CodeViewer
            code={artifacts?.documentation_markdown ?? null}
            emptyMessage="Generated documentation is not available."
          />
        )}
      </section>
    </div>
  );
}
