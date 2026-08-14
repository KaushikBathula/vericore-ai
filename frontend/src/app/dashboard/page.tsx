"use client";

import { useEffect, useState } from "react";
import { Cpu, FolderOpen, PlayCircle, CheckCircle } from "lucide-react";

import StatCard from "@/components/ui/StatCard";
import {
  getDashboardStats,
  DashboardStats,
} from "@/services/dashboardService";

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const dashboardStats = await getDashboardStats();
        setStats(dashboardStats);
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

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Projects"
          value={loading ? "..." : (stats?.totalProjects.toString() ?? "0")}
          icon={<FolderOpen className="h-5 w-5 text-muted-foreground" />}
        />

        <StatCard
          title="Generated RTL"
          value={loading ? "..." : (stats?.generatedRTL.toString() ?? "0")}
          icon={<Cpu className="h-5 w-5 text-muted-foreground" />}
        />

        <StatCard
          title="Pipeline Runs"
          value={loading ? "..." : (stats?.pipelineRuns.toString() ?? "0")}
          icon={<PlayCircle className="h-5 w-5 text-muted-foreground" />}
        />

        <StatCard
          title="Successful Builds"
          value={loading ? "..." : (stats?.successfulBuilds.toString() ?? "0")}
          icon={<CheckCircle className="h-5 w-5 text-muted-foreground" />}
        />
      </div>
    </div>
  );
}