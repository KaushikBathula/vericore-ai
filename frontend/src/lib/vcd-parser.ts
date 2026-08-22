import {
  ParsedVcd,
  VcdValue,
  WaveformSignal,
  WaveformTransition,
} from "@/types/waveform";

interface SignalDefinition {
  id: string;
  name: string;
  width: number;
  scopeDepth: number;
}

function normalizeValue(value: string): VcdValue {
  return value.trim().toLowerCase();
}

function parseValueChange(
  line: string,
): { id: string; value: VcdValue } | null {
  const vectorMatch = line.match(/^b([01xz]+)\s+(\S+)$/i);

  if (vectorMatch) {
    return {
      value: normalizeValue(vectorMatch[1]),
      id: vectorMatch[2],
    };
  }

  const scalarMatch = line.match(/^([01xz])(\S+)$/i);

  if (scalarMatch) {
    return {
      value: normalizeValue(scalarMatch[1]),
      id: scalarMatch[2],
    };
  }

  return null;
}

function cleanSignalName(name: string): string {
  return name
    .replace(/\s+\[\d+:\d+\]\s*$/, "")
    .trim();
}

export function parseVcd(content: string): ParsedVcd {
  const lines = content.split(/\r?\n/);

  const definitions = new Map<string, SignalDefinition>();
  const transitions = new Map<string, WaveformTransition[]>();

  let timescale = "";
  let currentTime = 0;
  let endTime = 0;
  let inDefinitions = true;

  let insideTimescale = false;
  const timescaleParts: string[] = [];

  const scopeStack: string[] = [];

  let topLevelScopeDepth = -1;

  for (const rawLine of lines) {
    const line = rawLine.trim();

    if (!line) {
      continue;
    }

    if (line === "$timescale") {
      insideTimescale = true;
      continue;
    }

    if (insideTimescale) {
      if (line === "$end") {
        insideTimescale = false;
        timescale = timescaleParts.join(" ");
        continue;
      }

      timescaleParts.push(line);
      continue;
    }

    const scopeMatch = line.match(/^\$scope\s+\S+\s+(\S+)\s+\$end$/);

    if (scopeMatch && inDefinitions) {
      scopeStack.push(scopeMatch[1]);

      if (topLevelScopeDepth === -1) {
        topLevelScopeDepth = scopeStack.length;
      }

      continue;
    }

    if (line === "$upscope $end" && inDefinitions) {
      scopeStack.pop();
      continue;
    }

    if (line === "$enddefinitions $end") {
      inDefinitions = false;
      continue;
    }

    if (inDefinitions) {
      const match = line.match(
        /^\$var\s+\S+\s+(\d+)\s+(\S+)\s+(.+?)\s+\$end$/,
      );

      if (match) {
        const width = Number(match[1]);
        const id = match[2];
        const rawName = match[3];

        /*
         * Only keep signals declared directly inside the
         * top-level testbench scope.
         *
         * This removes DUT/internal signals such as:
         *   dut.A
         *   dut.B
         *   dut._03_
         *   dut.SUM
         */
        if (scopeStack.length !== topLevelScopeDepth) {
          continue;
        }

        const name = cleanSignalName(rawName);

        if (!definitions.has(id)) {
          definitions.set(id, {
            id,
            name,
            width,
            scopeDepth: scopeStack.length,
          });

          transitions.set(id, []);
        }
      }

      continue;
    }

    if (line.startsWith("#")) {
      const time = Number(line.slice(1));

      if (Number.isFinite(time)) {
        currentTime = time;
        endTime = Math.max(endTime, time);
      }

      continue;
    }

    const change = parseValueChange(line);

    if (!change) {
      continue;
    }

    const signalTransitions = transitions.get(change.id);

    if (!signalTransitions) {
      continue;
    }

    signalTransitions.push({
      time: currentTime,
      value: change.value,
    });
  }

  const signals: WaveformSignal[] = [];

  for (const definition of definitions.values()) {
    signals.push({
      id: definition.id,
      name: definition.name,
      width: definition.width,
      transitions: transitions.get(definition.id) ?? [],
    });
  }

  return {
    timescale,
    signals,
    endTime,
  };
}