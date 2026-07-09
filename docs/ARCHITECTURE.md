# VeriCore AI Architecture

## Vision

VeriCore AI is an agentic RTL engineering platform that converts natural-language hardware requirements into complete design packages: structured requirements, synthesizable RTL, testbenches, simulation results, debug iterations, synthesis reports, waveform artifacts, and documentation.

The first implementation target is a production-quality educational and portfolio system. The architecture should be credible enough for internship interviews, college evaluation, and future open-source expansion.

## Architectural Principles

- Keep transport, business logic, AI agents, workflow orchestration, persistence, and EDA tool execution separated.
- Store every prompt outside Python code under `prompts/`.
- Treat EDA tools as replaceable adapters.
- Treat each generated hardware design as an immutable project run with versioned artifacts.
- Prefer typed Pydantic contracts between layers.
- Never execute shell commands from raw user input.
- Make every workflow step observable through logs and persisted run state.

## Top-Level Components

### Frontend

Next.js, React, TailwindCSS, TypeScript, and ShadCN UI provide a dark professional dashboard. The frontend calls backend REST APIs and renders project history, workflow progress, generated files, reports, logs, and settings.

### Backend API

FastAPI exposes REST endpoints for generation, simulation, debugging, synthesis, project listing, logs, reports, and downloads. Route handlers remain thin and delegate to services.

### Application Services

Services implement use cases such as "generate RTL package", "run simulation", "run synthesis", and "download project archive". They coordinate repositories, workflow graph execution, artifact storage, and tool adapters.

### Agent Layer

Each AI agent has a single responsibility and an isolated prompt set:

- Requirement Agent extracts structured hardware intent.
- RTL Agent generates synthesizable Verilog/SystemVerilog.
- Verification Agent creates testbenches and expected behavior.
- Simulation Agent prepares simulation commands and interprets results.
- Debug Agent diagnoses failures and proposes fixes.
- Synthesis Agent summarizes synthesis intent and constraints.
- Documentation Agent writes user-facing technical documentation.
- Coordinator Agent supervises global consistency and workflow metadata.

### LangGraph Workflow

LangGraph owns orchestration. Nodes wrap agents and tool execution. Conditional edges decide whether to continue to synthesis or loop through debug and RTL regeneration.

### Tool Adapters

The `tools/eda/` package wraps Icarus Verilog, Verilator, Yosys, GTKWave, and optional OpenSTA. Adapters expose typed methods and return structured command results, logs, artifact paths, and errors.

### Persistence

SQLite stores projects, runs, artifacts, logs, reports, workflow status, and configuration metadata. Repositories isolate database access from services.

### Generated Projects

Each user request creates a project directory under `generated_projects/`. A project contains RTL, testbenches, simulation outputs, waveforms, synthesis output, logs, and reports.

## Clean Architecture Flow

1. Frontend submits a natural-language hardware prompt.
2. FastAPI validates request schema.
3. Generation service creates a project record.
4. LangGraph executes the autonomous workflow.
5. Agents generate structured outputs.
6. Tool adapters run simulations and synthesis.
7. Repositories persist state and logs.
8. Reports and artifacts are written to the project folder.
9. Frontend displays progress and downloadable outputs.

## Supported Initial Modules

The first release should support templates and agent guidance for:

AND Gate, OR Gate, XOR Gate, NOT Gate, Multiplexer, Decoder, Encoder, Priority Encoder, Comparator, Adder, Subtractor, ALU, Register, Counter, Shift Register, FSM, UART, and FIFO.

Support should be implemented through extensible module capability definitions rather than hardcoded logic in one file.
