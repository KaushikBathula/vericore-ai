"use client";

import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import { PipelineResponse } from "@/types/pipeline";

interface PipelineContextValue {
  latestPipelineResult: PipelineResponse | null;
  setLatestPipelineResult: (result: PipelineResponse) => void;
  clearPipelineResult: () => void;
  isHydrated: boolean;
}

const STORAGE_KEY = "vericore.latestPipelineResult";

function getStoredPipelineResult(): PipelineResponse | null {
  if (typeof window === "undefined") {
    return null;
  }

  const stored = window.localStorage.getItem(STORAGE_KEY);

  if (!stored) {
    return null;
  }

  try {
    return JSON.parse(stored) as PipelineResponse;
  } catch {
    window.localStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

const PipelineContext = createContext<PipelineContextValue | null>(null);

export function PipelineProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [latestPipelineResult, setPipelineResultState] =
    useState<PipelineResponse | null>(null);

  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const storedResult = getStoredPipelineResult();

      if (storedResult) {
        setPipelineResultState(storedResult);
      }

      setIsHydrated(true);
    }, 0);

    return () => window.clearTimeout(timer);
  }, []);

  const setLatestPipelineResult = (result: PipelineResponse) => {
    setPipelineResultState(result);
    window.localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(result),
    );
  };

  const clearPipelineResult = () => {
    setPipelineResultState(null);
    window.localStorage.removeItem(STORAGE_KEY);
  };

  const value = useMemo(
    () => ({
      latestPipelineResult,
      setLatestPipelineResult,
      clearPipelineResult,
      isHydrated,
    }),
    [latestPipelineResult, isHydrated],
  );

  return (
    <PipelineContext.Provider value={value}>
      {children}
    </PipelineContext.Provider>
  );
}

export function usePipeline() {
  const context = useContext(PipelineContext);

  if (!context) {
    throw new Error(
      "usePipeline must be used within PipelineProvider",
    );
  }

  return context;
}