import { apiRequest } from "@/lib/api";

export interface Project {
  id: number;
  project_name: string;
  description: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export async function getProjects(): Promise<Project[]> {
  return apiRequest<Project[]>("/projects");
}
export async function getProject(
  projectId: number,
): Promise<Project> {
  return apiRequest<Project>(`/projects/${projectId}`);
}