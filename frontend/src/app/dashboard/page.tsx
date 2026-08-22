"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  Cpu,
  FolderOpen,
  PlayCircle,
  CheckCircle,
  ArrowRight,
} from "lucide-react";

import StatCard from "@/components/ui/StatCard";
import {
  getDashboardStats,
  DashboardStats,
} from "@/services/dashboardService";
import {
  getProjects,
  Project,
} from "@/services/projectService";

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [dashboardStats, projectList] = await Promise.all([
          getDashboardStats(),
          getProjects(),
        ]);

        setStats(dashboardStats);
        setProjects(projectList);
      } catch {
        setError("Failed to load dashboard.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  return (
    <div className="space-y-8">
      {error && (
        <p className="text-sm text-red-600">
          {error}
        </p>
      )}

      {/* Dashboard statistics */}
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Projects"
          value={
            loading
              ? "..."
              : (stats?.totalProjects.toString() ?? "0")
          }
          icon={
            <FolderOpen className="h-5 w-5 text-muted-foreground" />
          }
        />

        <StatCard
          title="Generated RTL"
          value={
            loading
              ? "..."
              : (stats?.generatedRTL.toString() ?? "0")
          }
          icon={
            <Cpu className="h-5 w-5 text-muted-foreground" />
          }
        />

        <StatCard
          title="Pipeline Runs"
          value={
            loading
              ? "..."
              : (stats?.pipelineRuns.toString() ?? "0")
          }
          icon={
            <PlayCircle className="h-5 w-5 text-muted-foreground" />
          }
        />

        <StatCard
          title="Successful Builds"
          value={
            loading
              ? "..."
              : (stats?.successfulBuilds.toString() ?? "0")
          }
          icon={
            <CheckCircle className="h-5 w-5 text-muted-foreground" />
          }
        />
      </div>

      {/* Projects */}
      <section className="space-y-4">
        <div>
          <h2 className="text-xl font-semibold">
            Projects
          </h2>

          <p className="text-sm text-muted-foreground">
            Select a project to view its generated artifacts and
            pipeline information.
          </p>
        </div>

        {loading ? (
          <div className="rounded-xl border bg-card p-6">
            <p className="text-sm text-muted-foreground">
              Loading projects...
            </p>
          </div>
        ) : projects.length === 0 ? (
          <div className="rounded-xl border bg-card p-6">
            <p className="text-sm text-muted-foreground">
              No projects found.
            </p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
            {projects.map((project) => (
              <Link
                key={project.id}
                href={`/projects/${project.id}`}
                className="group block"
              >
                <div className="h-full rounded-xl border bg-card p-6 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-center gap-3">
                      <div className="rounded-lg border p-2">
                        <FolderOpen className="h-5 w-5" />
                      </div>

                      <div>
                        <h3 className="font-semibold">
                          {project.project_name}
                        </h3>

                        <p className="text-xs text-muted-foreground">
                          Project #{project.id}
                        </p>
                      </div>
                    </div>

                    <ArrowRight className="h-5 w-5 text-muted-foreground transition-transform group-hover:translate-x-1" />
                  </div>

                  <p className="mt-4 line-clamp-2 text-sm text-muted-foreground">
                    {project.description ||
                      "No project description available."}
                  </p>

                  <div className="mt-5 flex items-center justify-between border-t pt-4">
                    <span className="text-xs text-muted-foreground">
                      Status
                    </span>

                    <span className="text-sm font-medium">
                      {project.status}
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}