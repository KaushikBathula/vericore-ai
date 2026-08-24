"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowLeft, CheckCircle, XCircle, Download } from "lucide-react";

import { getProject, Project } from "@/services/projectService";
import { getPipelineArtifacts } from "@/services/pipelineService";
import { PipelineArtifactsResponse } from "@/types/pipeline";

interface ProjectPageProps {
  params: Promise<{
    id: string;
  }>;
}

function artifactUrl(url: string | null): string | null {
  if (!url) {
    return null;
  }

  if (url.startsWith("http://") || url.startsWith("https://")) {
    return url;
  }

  const baseUrl =
    process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

  return `${baseUrl}${url}`;
}

export default function ProjectPage({
  params,
}: ProjectPageProps) {
  const [project, setProject] = useState<Project | null>(null);
  const [artifacts, setArtifacts] =
    useState<PipelineArtifactsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadProject() {
      try {
        const { id } = await params;
        const projectId = Number(id);

        if (!Number.isInteger(projectId) || projectId <= 0) {
          throw new Error("Invalid project ID.");
        }

        const projectData = await getProject(projectId);
        setProject(projectData);

        try {
          const artifactData = await getPipelineArtifacts(
            projectData.project_name,
          );

          setArtifacts(artifactData);
        } catch {
          setArtifacts(null);
        }
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load project.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadProject();
  }, [params]);

  if (loading) {
    return (
      <div className="space-y-4">
        <p className="text-sm text-muted-foreground">
          Loading project...
        </p>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="space-y-4">
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 text-sm font-medium"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Dashboard
        </Link>

        <div className="rounded-xl border p-6">
          <p className="text-sm text-red-600">
            {error ?? "Project not found."}
          </p>
        </div>
      </div>
    );
  }

  const artifactAvailable = Boolean(artifacts);

  const artifactCards = artifacts
    ? [
        {
          name: "RTL",
          description: "Generated synthesizable Verilog",
          content: artifacts.rtl_source,
          url: artifacts.download_urls.rtl,
        },
        {
          name: "Testbench",
          description: "Generated verification testbench",
          content: artifacts.testbench_source,
          url: artifacts.download_urls.testbench,
        },
        {
          name: "Simulation Output",
          description: "RTL simulation results",
          content: artifacts.simulation_output,
          url: artifacts.download_urls.simulation_output,
        },
        {
          name: "Simulation Waveform",
          description: "RTL VCD waveform",
          content: artifacts.simulation_waveform_source,
          url: artifacts.download_urls.simulation_waveform,
        },
        {
          name: "Synthesis Netlist",
          description: "Post-synthesis Verilog netlist",
          content: artifacts.artifact_paths.synthesis_netlist,
          url: artifacts.download_urls.synthesis_netlist,
        },
        {
          name: "Synthesis Report",
          description: "Yosys synthesis report",
          content: artifacts.synthesis_report,
          url: artifacts.download_urls.synthesis_report,
        },
        {
          name: "Schematic",
          description: "Generated circuit schematic",
          content: artifacts.artifact_paths.synthesis_schematic_svg,
          url: artifacts.download_urls.synthesis_schematic_svg,
        },
        {
          name: "Post-Synthesis Simulation",
          description: "Netlist simulation results",
          content: artifacts.post_synthesis_simulation_output,
          url: artifacts.download_urls.post_synthesis_simulation_output,
        },
        {
          name: "Post-Synthesis Waveform",
          description: "Post-synthesis VCD waveform",
          content: artifacts.post_synthesis_waveform_source,
          url: artifacts.download_urls.post_synthesis_waveform,
        },
        {
          name: "Documentation",
          description: "Generated project documentation",
          content: artifacts.documentation_markdown,
          url: artifacts.download_urls.documentation,
        },
      ]
    : [];

  return (
    <div className="space-y-8">
      <Link
        href="/dashboard"
        className="inline-flex items-center gap-2 text-sm font-medium"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Dashboard
      </Link>

      <div>
        <h1 className="text-3xl font-bold">
          {project.project_name}
        </h1>

        <p className="mt-2 text-muted-foreground">
          {project.description ||
            "No project description available."}
        </p>
      </div>

      <section className="rounded-xl border bg-card p-6 shadow-sm">
        <h2 className="text-xl font-semibold">
          Project Information
        </h2>

        <div className="mt-6 grid gap-6 md:grid-cols-2">
          <div>
            <p className="text-sm text-muted-foreground">
              Project / Module Name
            </p>

            <p className="mt-1 font-medium">
              {project.project_name}
            </p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">
              Status
            </p>

            <p className="mt-1 font-medium">
              {project.status}
            </p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">
              Project ID
            </p>

            <p className="mt-1 font-medium">
              {project.id}
            </p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">
              Generated Artifacts
            </p>

            <div className="mt-1 flex items-center gap-2">
              {artifactAvailable ? (
                <>
                  <CheckCircle className="h-4 w-4" />
                  <span className="font-medium">
                    Available
                  </span>
                </>
              ) : (
                <>
                  <XCircle className="h-4 w-4" />
                  <span className="font-medium">
                    No generated artifacts found
                  </span>
                </>
              )}
            </div>
          </div>
        </div>
      </section>

      {artifacts && (
        <section className="rounded-xl border bg-card p-6 shadow-sm">
          <div>
            <h2 className="text-xl font-semibold">
              Generated Artifacts
            </h2>

            <p className="mt-1 text-sm text-muted-foreground">
              Artifacts generated by the VeriCore AI pipeline.
            </p>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {artifactCards.map((artifact) => {
              const downloadUrl = artifactUrl(artifact.url);

              return (
                <div
                  key={artifact.name}
                  className="rounded-lg border p-4"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-medium">
                        {artifact.name}
                      </p>

                      <p className="mt-1 text-xs text-muted-foreground">
                        {artifact.description}
                      </p>
                    </div>

                    {artifact.content && downloadUrl ? (
                      <a
                        href={downloadUrl}
                        download
                        className="inline-flex items-center gap-1 rounded-md border px-2 py-1 text-xs font-medium transition hover:bg-muted"
                      >
                        <Download className="h-3.5 w-3.5" />
                        Download
                      </a>
                    ) : null}
                  </div>

                  <div className="mt-4">
                    {artifact.content ? (
                      <span className="text-sm font-medium">
                        ✓ Available
                      </span>
                    ) : (
                      <span className="text-sm text-muted-foreground">
                        Not available
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      )}
    </div>
  );
}