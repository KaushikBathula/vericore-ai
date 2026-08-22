export type VcdValue = "0" | "1" | "x" | "z" | string;

export interface WaveformTransition {
  time: number;
  value: VcdValue;
}

export interface WaveformSignal {
  id: string;
  name: string;
  width: number;
  transitions: WaveformTransition[];
}

export interface ParsedVcd {
  timescale: string;
  signals: WaveformSignal[];
  endTime: number;
}
