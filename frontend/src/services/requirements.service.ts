import { GenerateRTLRequest } from "@/types/generation";
import { ApiClient } from "@/lib/api-client";
import { PipelineResponse } from "@/types/pipeline";

export class RequirementsService {
  static async generateRTL(
    request: GenerateRTLRequest
  ): Promise<PipelineResponse> {
    return ApiClient.post<PipelineResponse>("/pipeline/run", request);
  }
}
