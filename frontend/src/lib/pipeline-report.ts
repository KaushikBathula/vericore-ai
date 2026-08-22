export function extractBooleanFromReport(
  markdown: string | null | undefined,
  labels: string[],
): boolean | null {
  if (!markdown) {
    return null;
  }

  for (const label of labels) {
    const pattern = new RegExp(
      `${escapeRegExp(label)}\\s*[:*]+\\s*(true|false)`,
      "i",
    );
    const match = markdown.match(pattern);

    if (match?.[1]) {
      return match[1].toLowerCase() === "true";
    }
  }

  return null;
}

export function extractTextFromReport(
  markdown: string | null | undefined,
  label: string,
): string | null {
  if (!markdown) {
    return null;
  }

  const pattern = new RegExp(
    `${escapeRegExp(label)}\\s*[:*]+\\s*([^\\n]+)`,
    "i",
  );
  const match = markdown.match(pattern);

  return match?.[1]?.trim() ?? null;
}

export function countGeneratedTests(testbench: string | null): number | null {
  if (!testbench) {
    return null;
  }

  const matches = testbench.match(/\/\/\s*(?:Addition\s+)?Test\b/gi);

  return matches?.length ?? null;
}

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
