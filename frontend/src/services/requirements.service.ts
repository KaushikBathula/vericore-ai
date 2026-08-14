import { GenerateRTLRequest } from "@/types/generation";
import { ApiClient } from "@/lib/api-client";
export class RequirementsService {
  static async generateRTL(request: GenerateRTLRequest) {
    // Backend integration will be added in the next task.
    return ApiClient.post("/pipeline/run", request);
  }
}