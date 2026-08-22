"use client";

import { TestTube } from "lucide-react";

import CodeViewer from "@/components/pipeline/CodeViewer";
import MissingPipelineState from "@/components/pipeline/MissingPipelineState";
import StatusBadge from "@/components/pipeline/StatusBadge";
import { usePipelineArtifacts } from "@/hooks/usePipelineArtifacts";
import {
  countGeneratedTests,
  extractBooleanFromReport,
} from "@/lib/pipeline-report";

export default function TestbenchPage() {
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

  const simulationSuccess = extractBooleanFromReport(
    artifacts?.documentation_markdown,
    ["Simulation Success"],
  );
  const testCount = countGeneratedTests(artifacts?.testbench_source ?? null);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="flex items-center gap-2 text-3xl font-bold">
          <TestTube className="h-7 w-7" />
          Testbench
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

      <section className="grid gap-4 md:grid-cols-3">
        <div className="rounded-xl border bg-card p-4 shadow-sm">
          <p className="text-sm text-muted-foreground">Verification</p>
          <div className="mt-2">
            <StatusBadge success={simulationSuccess} />
          </div>
        </div>
        <div className="rounded-xl border bg-card p-4 shadow-sm">
          <p className="text-sm text-muted-foreground">Generated Tests</p>
          <p className="mt-2 text-2xl font-semibold">
            {testCount ?? "Unavailable"}
          </p>
        </div>
        <div className="rounded-xl border bg-card p-4 shadow-sm">
          <p className="text-sm text-muted-foreground">Artifact</p>
          <p className="mt-2 break-all text-sm font-medium">
            {artifacts?.artifact_paths.testbench ?? "Unavailable"}
          </p>
        </div>
      </section>

      <section className="rounded-xl border bg-card p-6 shadow-sm">
        <h2 className="mb-4 text-lg font-semibold">
          Generated Testbench Source
        </h2>
        {loading ? (
          <p className="text-sm text-muted-foreground">
            Loading testbench...
          </p>
        ) : (
          <CodeViewer
            code={artifacts?.testbench_source ?? null}
            emptyMessage="Generated testbench source is not available."
          />
        )}
      </section>
    </div>
  );
}
