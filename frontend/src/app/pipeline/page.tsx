"use client";

import Link from "next/link";
import {
  BookOpen,
  CheckCircle,
  FileCode,
  Gauge,
  PlayCircle,
  Settings,
  TestTube,
} from "lucide-react";

import MissingPipelineState from "@/components/pipeline/MissingPipelineState";
import StatusBadge from "@/components/pipeline/StatusBadge";
import { usePipelineArtifacts } from "@/hooks/usePipelineArtifacts";
import {
  extractBooleanFromReport,
  extractTextFromReport,
} from "@/lib/pipeline-report";

const actions = [
  { href: "/rtl", label: "View RTL", icon: FileCode },
  { href: "/testbench", label: "View Testbench", icon: TestTube },
  { href: "/simulation", label: "View Simulation", icon: PlayCircle },
  { href: "/synthesis", label: "View Synthesis", icon: Settings },
  { href: "/documentation", label: "View Documentation", icon: BookOpen },
];

export default function PipelinePage() {
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

  const documentation = artifacts?.documentation_markdown;
  const compileSuccess = extractBooleanFromReport(
    documentation,
    ["Compile Success"],
  );
  const simulationSuccess = extractBooleanFromReport(
    documentation,
    ["Simulation Success"],
  );
  const synthesisSuccess = extractBooleanFromReport(
    documentation,
    ["- Success", "Success"],
  );
  const requirementDescription = extractTextFromReport(
    documentation,
    "Description",
  );

  const steps = [
    { label: "Requirement Analysis", status: !!requirementDescription },
    { label: "RTL Generation", status: !!artifacts?.rtl_source },
    { label: "Verification", status: !!artifacts?.testbench_source },
    { label: "RTL Compilation", status: compileSuccess },
    { label: "RTL Simulation", status: simulationSuccess },
    { label: "Synthesis", status: synthesisSuccess },
    {
      label: "Post-Synthesis Simulation",
      status: artifacts?.post_synthesis_simulation_output
        ? latestPipelineResult.success
        : null,
    },
    {
      label: "Documentation",
      status: !!artifacts?.documentation_markdown,
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          <h1 className="flex items-center gap-2 text-3xl font-bold">
            <Gauge className="h-7 w-7" />
            Pipeline
          </h1>
          <p className="mt-2 text-muted-foreground">
            Project: {moduleName}
          </p>
        </div>

        <StatusBadge
          success={latestPipelineResult.success}
          label={
            latestPipelineResult.success ? "Completed" : "Not Completed"
          }
        />
      </div>

      {error && (
        <p className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          {error}
        </p>
      )}

      {loading ? (
        <p className="text-sm text-muted-foreground">
          Loading generated artifacts...
        </p>
      ) : (
        <>
          <section className="rounded-xl border bg-card p-6 shadow-sm">
            <div className="grid gap-3 md:grid-cols-2">
              {steps.map((step) => (
                <div
                  key={step.label}
                  className="flex items-center justify-between rounded-lg border p-3"
                >
                  <div className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm font-medium">
                      {step.label}
                    </span>
                  </div>
                  <StatusBadge success={step.status} />
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-xl border bg-card p-6 shadow-sm">
            <h2 className="text-lg font-semibold">Run Summary</h2>
            <dl className="mt-4 grid gap-4 md:grid-cols-2">
              <div>
                <dt className="text-sm text-muted-foreground">Message</dt>
                <dd className="mt-1 text-sm font-medium">
                  {latestPipelineResult.message}
                </dd>
              </div>
              <div>
                <dt className="text-sm text-muted-foreground">Report</dt>
                <dd className="mt-1 break-all text-sm font-medium">
                  {latestPipelineResult.report_path}
                </dd>
              </div>
              <div className="md:col-span-2">
                <dt className="text-sm text-muted-foreground">
                  Requirement Summary
                </dt>
                <dd className="mt-1 text-sm font-medium">
                  {requirementDescription ?? "Not available in report."}
                </dd>
              </div>
            </dl>
          </section>

          <section className="grid gap-3 md:grid-cols-3">
            {actions.map((action) => {
              const Icon = action.icon;

              return (
                <Link
                  key={action.href}
                  href={action.href}
                  className="inline-flex h-10 items-center justify-center gap-2 rounded-lg border bg-background px-3 text-sm font-medium hover:bg-muted"
                >
                  <Icon className="h-4 w-4" />
                  {action.label}
                </Link>
              );
            })}
          </section>
        </>
      )}
    </div>
  );
}
