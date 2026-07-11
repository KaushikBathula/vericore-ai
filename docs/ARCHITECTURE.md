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


## Project Manager Agent

The Project Manager Agent is the central orchestrator of VeriCore AI. It does not generate RTL or execute engineering tasks directly. Instead, it coordinates all specialized AI agents, manages the workflow state, tracks execution progress, decides which agent should execute next, handles retry logic after failures, and determines when the workflow has successfully completed.

Responsibilities include:

- Initialize a new design workflow
- Maintain the global workflow state
- Delegate tasks to specialized agents
- Monitor execution status
- Handle retry and recovery logic
- Coordinate LangGraph execution
- Collect generated artifacts
- Trigger synthesis and documentation after successful verification
- Terminate the workflow upon successful completion

## Autonomous Workflow

The autonomous workflow follows a centralized orchestration model where the Project Manager Agent coordinates all engineering agents.

                     User
                       │
                       ▼
            Project Manager Agent
                       │
                       ▼
            Requirement Agent
                       │
                       ▼
                 RTL Agent
                       │
                       ▼
           Verification Agent
                       │
                       ▼
             Simulation Agent
                       │
              Compilation OK?
               /             \
             Yes             No
              │               │
              ▼               ▼
      Synthesis Agent    Debug Agent
              │               │
              └───────┬───────┘
                      ▼
          Documentation Agent
                      │
                      ▼
             Download Package


## Workflow State

The Project Manager maintains a shared workflow state throughout execution.

The workflow state includes:

- Project Identifier
- Module Name
- Current Workflow Stage
- Active Agent
- Retry Counter
- Generated RTL Files
- Testbench Files
- Simulation Status
- Compilation Errors
- Synthesis Status
- Generated Reports
- Artifact Locations
- Execution Logs
- Overall Workflow Status

Every agent receives the current workflow state, performs its specialized task, updates the state, and returns control to the Project Manager Agent.


## Memory Layer

VeriCore AI includes a lightweight memory layer that stores workflow context and generated engineering artifacts.

The memory layer consists of:

- Project Memory
- Artifact Memory
- Conversation Memory

This enables agents to reference previous RTL versions, debugging iterations, simulation outputs, synthesis reports, and generated documentation without losing workflow context.

The memory layer is designed to support future expansion toward long-running autonomous engineering sessions.

## Future Expansion

The architecture is intentionally modular.

Future releases may include:

- Timing Analysis Agent
- Power Analysis Agent
- Formal Verification Agent
- DFT Agent
- RTL Optimization Agent
- Linting Agent
- Multi-LLM Support
- Cloud Simulation
- Distributed Agent Execution