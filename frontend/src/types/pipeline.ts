export interface PipelineResponse {
  success: boolean;
  report_path: string;
  message: string;
}

export interface PipelineArtifactPaths {
  rtl: string | null;
  testbench: string | null;
  simulation_output: string | null;
  simulation_waveform: string | null;
  synthesis_design: string | null;
  synthesis_script: string | null;
  synthesis_netlist: string | null;
  synthesis_report: string | null;
  synthesis_schematic_svg: string | null;
  synthesis_schematic_dot: string | null;
  post_synthesis_simulation_output: string | null;
  post_synthesis_waveform: string | null;
  documentation: string | null;
}

export interface PipelineArtifactDownloadUrls {
  rtl: string | null;
  testbench: string | null;
  simulation_output: string | null;
  simulation_waveform: string | null;
  synthesis_netlist: string | null;
  synthesis_report: string | null;
  synthesis_schematic_svg: string | null;
  synthesis_schematic_dot: string | null;
  post_synthesis_simulation_output: string | null;
  post_synthesis_waveform: string | null;
  documentation: string | null;
}

export interface PipelineArtifactsResponse {
  module_name: string;
  project_path: string;
  artifact_paths: PipelineArtifactPaths;
  download_urls: PipelineArtifactDownloadUrls;
  rtl_source: string | null;
  testbench_source: string | null;
  simulation_output: string | null;
  simulation_waveform_source: string | null;
  synthesis_report: string | null;
  post_synthesis_simulation_output: string | null;
  post_synthesis_waveform_source: string | null;
  documentation_markdown: string | null;
}
