# Directory Structure

```text
vericore-ai/
  backend/                 FastAPI application and backend tests
  frontend/                Next.js dashboard
  agents/                  Reusable AI agent implementations
  prompts/                 Agent prompt templates
  tools/                   OpenAI, EDA, filesystem, reporting, and security adapters
  workflow/                LangGraph graph, nodes, edges, and state
  database/                SQLite session setup, models base, migrations, seed notes
  generated_projects/      User-generated RTL project artifacts
  tests/                   Cross-system tests
  docs/                    Architecture and project planning
  config/                  YAML configuration for app, logging, and toolchains
  scripts/                 Developer and CI helper scripts
  docker/                  Dockerfiles for app and EDA toolchain images
```

## Project Artifact Layout

Each generated hardware project should use this shape:

```text
generated_projects/<project_id>/
  spec/
    structured_spec.json
  rtl/
    <module>.sv
  tb/
    <module>_tb.sv
  sim/
    compile.log
    simulation.log
    waveform.vcd
  synth/
    yosys.log
    netlist.v
    synthesis_report.md
  docs/
    report.md
    report.pdf
  logs/
    workflow.jsonl
```
