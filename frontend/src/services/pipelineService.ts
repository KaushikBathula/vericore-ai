import { ApiClient, API_BASE_URL } from "@/lib/api-client";
import {
  PipelineArtifactsResponse,
  PipelineResponse,
} from "@/types/pipeline";

export function getModuleNameFromReportPath(
  response: PipelineResponse | null,
): string | null {
  if (!response?.report_path) {
    return null;
  }

  const parts = response.report_path.replaceAll("\\", "/").split("/");
  const generatedProjectsIndex = parts.lastIndexOf("generated_projects");

  if (
    generatedProjectsIndex >= 0
    && parts.length > generatedProjectsIndex + 1
  ) {
    return parts[generatedProjectsIndex + 1] || null;
  }

  if (parts.length >= 3 && parts.at(-2) === "documentation") {
    return parts.at(-3) || null;
  }

  return null;
}

export function getArtifactUrl(path: string | null): string | null {
  if (!path) {
    return null;
  }

  if (path.startsWith("/api/")) {
    const baseWithoutApi = API_BASE_URL.replace(/\/api\/?$/, "");
    return `${baseWithoutApi}${path}`;
  }

  return `${API_BASE_URL}${path}`;
}

export async function getPipelineArtifacts(
  moduleName: string,
): Promise<PipelineArtifactsResponse> {
  return ApiClient.get<PipelineArtifactsResponse>(
    `/pipeline/artifacts/${encodeURIComponent(moduleName)}`,
  );
}
