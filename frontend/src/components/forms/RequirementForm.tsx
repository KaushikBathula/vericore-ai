"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { RequirementsService } from "@/services/requirements.service";

export default function RequirementForm() {
  const [projectName, setProjectName] = useState("");
  const [requirement, setRequirement] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState("");

  const handleGenerateRTL = async () => {
    console.log("Generate button clicked");
    try {
      setIsGenerating(true);
      setError("");

      await RequirementsService.generateRTL({
        requirement,
      });
    } catch (error) {
      console.error(error);
      setError("Failed to start RTL generation pipeline.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="rounded-xl border bg-card p-6 shadow-sm">
      <h2 className="text-xl font-semibold">
        New Hardware Requirement
      </h2>

      <p className="mt-2 text-sm text-muted-foreground">
        Enter your hardware specification below.
      </p>

      {/* Project Name */}
      <div className="mt-6 space-y-2">
        <label
          htmlFor="projectName"
          className="text-sm font-medium"
        >
          Project Name
        </label>

        <input
          id="projectName"
          type="text"
          placeholder="Example: 4-bit ALU"
          value={projectName}
          onChange={(e) => setProjectName(e.target.value)}
          className="w-full rounded-lg border px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Requirement Description */}
      <div className="mt-6 space-y-2">
        <label
          htmlFor="requirement"
          className="text-sm font-medium"
        >
          Requirement Description
        </label>

        <textarea
          id="requirement"
          rows={10}
          placeholder={`Example:

Design a synthesizable 4-bit ALU.

Inputs:
- A[3:0]
- B[3:0]
- opcode[2:0]

Operations:
- ADD
- SUB
- AND
- OR
- XOR

Outputs:
- result[3:0]
- carry
- zero
- overflow`}
          value={requirement}
          onChange={(e) => setRequirement(e.target.value)}
          className="w-full rounded-lg border px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Error Message */}
      {error && (
        <p className="mt-4 text-sm text-red-600">
          {error}
        </p>
      )}

      {/* Generate RTL Button */}
      <div className="mt-6">
        <Button
          type="button"
          className="w-full"
          disabled={isGenerating}
          onClick={handleGenerateRTL}
        >
          {isGenerating ? "Generating..." : "Generate RTL"}
        </Button>
      </div>
    </div>
  );
}