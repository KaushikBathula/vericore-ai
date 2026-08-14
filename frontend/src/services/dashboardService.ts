import { getProjects } from "./projectService";

export interface DashboardStats {
  totalProjects: number;
  generatedRTL: number;
  pipelineRuns: number;
  successfulBuilds: number;
}

export async function getDashboardStats(): Promise<DashboardStats> {
  const projects = await getProjects();

  return {
    totalProjects: projects.length,
    generatedRTL: 0,
    pipelineRuns: 0,
    successfulBuilds: 0,
  };
}