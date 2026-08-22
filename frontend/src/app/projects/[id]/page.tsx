"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowLeft, CheckCircle, XCircle } from "lucide-react";

import { getProject, Project } from "@/services/projectService";
import { getPipelineArtifacts } from "@/services/pipelineService";
import { PipelineArtifactsResponse } from "@/types/pipeline";

interface ProjectPageProps {
  params: Promise<{
    id: string;
  }>;
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
          {project.description || "No project description available."}
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
              Current Run / Generated Artifacts
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
          <h2 className="text-xl font-semibold">
            Generated Artifacts
          </h2>

          <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {[
              ["RTL", artifacts.rtl_source],
              ["Testbench", artifacts.testbench_source],
              ["Simulation Output", artifacts.simulation_output],
              [
                "Simulation Waveform",
                artifacts.simulation_waveform_source,
              ],
              ["Synthesis Report", artifacts.synthesis_report],
              [
                "Post-Synthesis Simulation",
                artifacts.post_synthesis_simulation_output,
              ],
              [
                "Post-Synthesis Waveform",
                artifacts.post_synthesis_waveform_source,
              ],
              [
                "Documentation",
                artifacts.documentation_markdown,
              ],
            ].map(([name, content]) => (
              <div
                key={name}
                className="rounded-lg border p-4"
              >
                <p className="font-medium">
                  {name}
                </p>

                <p className="mt-2 text-sm text-muted-foreground">
                  {content ? "Available" : "Not available"}
                </p>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}