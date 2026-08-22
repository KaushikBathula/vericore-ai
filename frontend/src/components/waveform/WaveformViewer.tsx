"use client";

import { useMemo } from "react";

import { parseVcd } from "@/lib/vcd-parser";
import { ParsedVcd, WaveformSignal } from "@/types/waveform";

interface WaveformViewerProps {
  vcdContent: string | null;
}

const LEFT_WIDTH = 150;
const TIME_WIDTH = 12;
const ROW_HEIGHT = 64;
const WAVE_TOP = 14;
const WAVE_BOTTOM = 50;

function displayValue(signal: WaveformSignal, value: string): string {
  if (signal.width === 1) {
    return value;
  }

  return value.replace(/^0b/i, "").padStart(signal.width, "0");
}

function transitionValue(
  signal: WaveformSignal,
  time: number,
): string {
  let currentValue = signal.width === 1 ? "x" : "x";

  for (const transition of signal.transitions) {
    if (transition.time > time) {
      break;
    }

    currentValue = transition.value;
  }

  return currentValue;
}

function valueToLevel(value: string): "high" | "low" | "unknown" {
  if (value === "1") {
    return "high";
  }

  if (value === "0") {
    return "low";
  }

  return "unknown";
}

function DigitalWaveform({
  signal,
  waveform,
}: {
  signal: WaveformSignal;
  waveform: ParsedVcd;
}) {
  const endTime = Math.max(waveform.endTime, 1);

  const points = useMemo(() => {
    const result = [
      {
        time: 0,
        value: transitionValue(signal, 0),
      },
    ];

    for (const transition of signal.transitions) {
      if (transition.time > 0) {
        result.push({
          time: transition.time,
          value: transition.value,
        });
      }
    }

    return result;
  }, [signal]);

  const isBus = signal.width > 1;

  return (
    <svg
      width={Math.max(endTime * TIME_WIDTH, 500)}
      height={ROW_HEIGHT}
      className="block"
      preserveAspectRatio="none"
    >
      {/* Horizontal center guide */}
      <line
        x1="0"
        y1={ROW_HEIGHT / 2}
        x2={endTime * TIME_WIDTH}
        y2={ROW_HEIGHT / 2}
        stroke="currentColor"
        strokeOpacity="0.08"
      />

      {points.map((point, index) => {
        const nextPoint = points[index + 1];

        const startX = point.time * TIME_WIDTH;
        const endX = (nextPoint?.time ?? endTime) * TIME_WIDTH;

        const level = valueToLevel(point.value);

        if (isBus) {
          return (
            <g key={`${point.time}-${index}`}>
              {/* Bus transition edges */}
              <polygon
                points={`
                  ${startX},${WAVE_TOP + 8}
                  ${startX + 6},${WAVE_TOP}
                  ${endX - 6},${WAVE_TOP}
                  ${endX},${WAVE_TOP + 8}
                  ${endX - 6},${WAVE_BOTTOM}
                  ${startX + 6},${WAVE_BOTTOM}
                  ${startX},${WAVE_BOTTOM - 8}
                `}
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
              />

              {/* Bus value */}
              {endX - startX > 35 && (
                <text
                  x={(startX + endX) / 2}
                  y={ROW_HEIGHT / 2 + 4}
                  textAnchor="middle"
                  className="fill-current font-mono text-[11px]"
                >
                  {displayValue(signal, point.value)}
                </text>
              )}
            </g>
          );
        }

        const y =
          level === "high"
            ? WAVE_TOP
            : level === "low"
              ? WAVE_BOTTOM
              : ROW_HEIGHT / 2;

        const previousY =
          index === 0
            ? y
            : (() => {
                const previousLevel = valueToLevel(points[index - 1].value);

                return previousLevel === "high"
                  ? WAVE_TOP
                  : previousLevel === "low"
                    ? WAVE_BOTTOM
                    : ROW_HEIGHT / 2;
              })();

        return (
          <g key={`${point.time}-${index}`}>
            {/* Vertical transition */}
            {index > 0 && (
              <line
                x1={startX}
                y1={previousY}
                x2={startX}
                y2={y}
                stroke="currentColor"
                strokeWidth="2"
              />
            )}

            {/* Signal level */}
            <line
              x1={startX}
              y1={y}
              x2={endX}
              y2={y}
              stroke="currentColor"
              strokeWidth="2"
            />
          </g>
        );
      })}
    </svg>
  );
}

function WaveformRow({
  signal,
  waveform,
}: {
  signal: WaveformSignal;
  waveform: ParsedVcd;
}) {

  return (
    <div
      className="grid border-t"
      style={{
        gridTemplateColumns: `${LEFT_WIDTH}px 1fr`,
        minHeight: `${ROW_HEIGHT}px`,
      }}
    >
      <div className="flex items-center border-r bg-muted/20 px-3 font-mono text-sm font-medium">
        {signal.name}
        {signal.width > 1 && (
          <span className="ml-1 text-xs text-muted-foreground">
            [{signal.width - 1}:0]
          </span>
        )}
      </div>

      <div className="overflow-x-hidden">
        <DigitalWaveform
          signal={signal}
          waveform={waveform}
        />
      </div>
    </div>
  );
}

export default function WaveformViewer({
  vcdContent,
}: WaveformViewerProps) {
  const waveform = useMemo<ParsedVcd | null>(() => {
    if (!vcdContent) {
      return null;
    }

    try {
      return parseVcd(vcdContent);
    } catch {
      return null;
    }
  }, [vcdContent]);

  if (!vcdContent) {
    return (
      <div className="rounded-lg border bg-muted/30 p-4 text-sm text-muted-foreground">
        Waveform data is not available.
      </div>
    );
  }

  if (!waveform) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
        Unable to parse the VCD waveform.
      </div>
    );
  }

  if (waveform.signals.length === 0) {
    return (
      <div className="rounded-lg border bg-muted/30 p-4 text-sm text-muted-foreground">
        No waveform signals were found.
      </div>
    );
  }

  const endTime = Math.max(waveform.endTime, 1);
  const timelineWidth = Math.max(endTime * TIME_WIDTH, 500);

  return (
    <div className="overflow-x-auto rounded-lg border bg-background">
      <div
        style={{
          minWidth: `${LEFT_WIDTH + timelineWidth}px`,
        }}
      >
        {/* Timeline */}
        <div
          className="grid border-b bg-muted/30"
          style={{
            gridTemplateColumns: `${LEFT_WIDTH}px 1fr`,
          }}
        >
          <div className="border-r px-3 py-2 text-sm font-semibold">
            Signal
          </div>

          <div
            className="relative h-10"
            style={{
              minWidth: `${timelineWidth}px`,
            }}
          >
            {Array.from(
              {
                length: Math.min(
                  Math.ceil(endTime / 10) + 1,
                  200,
                ),
              },
              (_, index) => index * 10,
            ).map((time) => {
              if (time > endTime) {
                return null;
              }

              return (
                <div
                  key={time}
                  className="absolute inset-y-0 border-l border-dashed border-zinc-300"
                  style={{
                    left: `${(time / endTime) * 100}%`,
                  }}
                >
                  <span className="absolute left-1 top-1 font-mono text-xs text-muted-foreground">
                    {time}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Signals */}
        {waveform.signals.map((signal) => (
          <WaveformRow
            key={signal.id}
            signal={signal}
            waveform={waveform}
          />
        ))}
      </div>
    </div>
  );
}