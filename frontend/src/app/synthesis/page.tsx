"use client";

import { Download, Settings } from "lucide-react";

import CodeViewer from "@/components/pipeline/CodeViewer";
import MissingPipelineState from "@/components/pipeline/MissingPipelineState";
import StatusBadge from "@/components/pipeline/StatusBadge";
import WaveformViewer from "@/components/waveform/WaveformViewer";
import { usePipelineArtifacts } from "@/hooks/usePipelineArtifacts";
import {
  extractBooleanFromReport,
  extractTextFromReport,
} from "@/lib/pipeline-report";
import { getArtifactUrl } from "@/services/pipelineService";

export default function SynthesisPage() {
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

  const synthesisSuccess = extractBooleanFromReport(
    artifacts?.documentation_markdown,
    ["- Success"],
  );

  const warningCount = extractTextFromReport(
    artifacts?.documentation_markdown,
    "Warnings",
  );

  const cellCount = extractTextFromReport(
    artifacts?.documentation_markdown,
    "Cells",
  );

  const reportUrl = getArtifactUrl(
    artifacts?.download_urls.synthesis_report ?? null,
  );

  const netlistUrl = getArtifactUrl(
    artifacts?.download_urls.synthesis_netlist ?? null,
  );
  const schematicUrl = getArtifactUrl(
    artifacts?.download_urls.synthesis_schematic_svg ?? null,
  );


  const postSynthesisWaveformUrl = getArtifactUrl(
    artifacts?.download_urls.post_synthesis_waveform ?? null,
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="flex items-center gap-2 text-3xl font-bold">
          <Settings className="h-7 w-7" />
          Synthesis
        </h1>

        <p className="mt-2 text-muted-foreground">
          Module: {moduleName}
        </p>
      </div>

      {error && (
        <p className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          {error}
        </p>
      )}

      <section className="grid gap-4 md:grid-cols-4">
        <div className="rounded-xl border bg-card p-4 shadow-sm">
          <p className="text-sm text-muted-foreground">
            Yosys Status
          </p>

          <div className="mt-2">
            <StatusBadge success={synthesisSuccess} />
          </div>
        </div>

        <div className="rounded-xl border bg-card p-4 shadow-sm">
          <p className="text-sm text-muted-foreground">
            Warnings
          </p>

          <p className="mt-2 text-2xl font-semibold">
            {warningCount ?? "Unavailable"}
          </p>
        </div>

        <div className="rounded-xl border bg-card p-4 shadow-sm">
          <p className="text-sm text-muted-foreground">
            Cells
          </p>

          <p className="mt-2 text-2xl font-semibold">
            {cellCount ?? "Unavailable"}
          </p>
        </div>

        <div className="rounded-xl border bg-card p-4 shadow-sm">
          <p className="text-sm text-muted-foreground">
            Artifacts
          </p>

          <div className="mt-2 flex flex-wrap gap-3">
            {reportUrl && (
              <a
                href={reportUrl}
                className="inline-flex items-center gap-1 text-sm font-medium underline-offset-4 hover:underline"
              >
                <Download className="h-4 w-4" />
                Report
              </a>
            )}

            {netlistUrl && (
              <a
                href={netlistUrl}
                className="inline-flex items-center gap-1 text-sm font-medium underline-offset-4 hover:underline"
              >
                <Download className="h-4 w-4" />
                Netlist
              </a>
            )}
            {schematicUrl && (
              <a
                href={schematicUrl}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 text-sm font-medium underline-offset-4 hover:underline"
              >
                <Download className="h-4 w-4" />
                Schematic
              </a>
            )}

            {postSynthesisWaveformUrl && (
              <a
                href={postSynthesisWaveformUrl}
                className="inline-flex items-center gap-1 text-sm font-medium underline-offset-4 hover:underline"
              >
                <Download className="h-4 w-4" />
                VCD
              </a>
            )}

            {!reportUrl &&
              !netlistUrl &&
              !schematicUrl &&
              !postSynthesisWaveformUrl && (
                <span className="text-sm font-medium">
                  Unavailable
                </span>
              )}
          </div>
        </div>
      </section>

      <section className="rounded-xl border bg-card p-6 shadow-sm">
        <div className="mb-4">
          <h2 className="text-lg font-semibold">
            Yosys Report
          </h2>

          <p className="mt-1 break-all text-sm text-muted-foreground">
            {artifacts?.artifact_paths.synthesis_report ??
              "Unavailable"}
          </p>
        </div>

        {loading ? (
          <p className="text-sm text-muted-foreground">
            Loading synthesis report...
          </p>
        ) : (
          <CodeViewer
            code={artifacts?.synthesis_report ?? null}
            emptyMessage="Synthesis report is not available."
          />
        )}
      </section>

      <section className="rounded-xl border bg-card p-6 shadow-sm">
        <div className="mb-4">
          <h2 className="text-lg font-semibold">
            Synthesis Schematic
          </h2>

          <p className="mt-1 text-sm text-muted-foreground">
            RTL circuit synthesized by Yosys.
          </p>
        </div>

        {loading ? (
          <p className="text-sm text-muted-foreground">
            Loading synthesis schematic...
          </p>
        ) : schematicUrl ? (
          <div className="overflow-auto rounded-lg border bg-white p-4">
            <img
              src={schematicUrl}
              alt={`${moduleName} synthesis schematic`}
              className="mx-auto h-auto max-w-full"
            />
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">
            Synthesis schematic is not available.
          </p>
        )}
      </section>

      <section className="rounded-xl border bg-card p-6 shadow-sm">
        <h2 className="mb-4 text-lg font-semibold">
          Post-Synthesis Simulation Output
        </h2>

        <CodeViewer
          code={artifacts?.post_synthesis_simulation_output ?? null}
          emptyMessage="Post-synthesis simulation output is not available."
        />
      </section>

      <section className="rounded-xl border bg-card p-6 shadow-sm">
        <div className="mb-4">
          <h2 className="text-lg font-semibold">
            Post-Synthesis Waveform
          </h2>

          <p className="mt-1 text-sm text-muted-foreground">
            Waveform generated from the synthesized netlist.
          </p>
        </div>

        <WaveformViewer
          vcdContent={
            artifacts?.post_synthesis_waveform_source ?? null
          }
        />
      </section>
    </div>
  );
}