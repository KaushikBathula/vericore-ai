"use client";

import { useEffect, useMemo, useState } from "react";

import { usePipeline } from "@/context/PipelineContext";
import {
  getModuleNameFromReportPath,
  getPipelineArtifacts,
} from "@/services/pipelineService";
import { PipelineArtifactsResponse } from "@/types/pipeline";

export function usePipelineArtifacts() {
  const { latestPipelineResult, isHydrated } = usePipeline();

  const moduleName = useMemo(
    () => getModuleNameFromReportPath(latestPipelineResult),
    [latestPipelineResult],
  );

  const [artifacts, setArtifacts] =
    useState<PipelineArtifactsResponse | null>(null);

  const [requestState, setRequestState] = useState<{
    moduleName: string | null;
    status: "idle" | "loading" | "success" | "error";
    error: string | null;
  }>({
    moduleName: null,
    status: "idle",
    error: null,
  });

  useEffect(() => {
    if (!isHydrated || !moduleName) {
      return;
    }

    let isCurrent = true;

    getPipelineArtifacts(moduleName)
      .then((result) => {
        if (isCurrent) {
          setArtifacts(result);
          setRequestState({
            moduleName,
            status: "success",
            error: null,
          });
        }
      })
      .catch((caughtError: unknown) => {
        if (isCurrent) {
          setRequestState({
            moduleName,
            status: "error",
            error:
              caughtError instanceof Error
                ? caughtError.message
                : "Failed to load generated pipeline artifacts.",
          });
        }
      });

    return () => {
      isCurrent = false;
    };
  }, [isHydrated, moduleName]);

  const loading =
    isHydrated &&
    Boolean(moduleName) &&
    requestState.moduleName !== moduleName;

  return {
    latestPipelineResult,
    moduleName,
    artifacts,
    loading,
    error: requestState.error,
    isHydrated,
  };
}