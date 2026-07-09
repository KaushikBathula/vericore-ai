# Development Order

## Phase 1: Foundation

1. Configure Python project, FastAPI app factory, settings, logging, and exception handling.
2. Define Pydantic schemas for generation, workflow state, artifacts, logs, and reports.
3. Implement SQLite models, session management, and repositories.
4. Add safe path handling and filename sanitization.

## Phase 2: Toolchain Adapters

1. Implement safe subprocess runner.
2. Implement Icarus Verilog compile/simulation adapter.
3. Implement Verilator lint adapter.
4. Implement Yosys synthesis adapter.
5. Add GTKWave/VCD artifact support.
6. Add dependency detection and clear missing-tool errors.

## Phase 3: Agent Layer

1. Implement prompt loader.
2. Implement base agent interface and LLM client.
3. Implement Requirement Agent with structured JSON output.
4. Implement RTL Agent.
5. Implement Verification Agent.
6. Implement Debug Agent.
7. Implement Synthesis and Documentation Agents.

## Phase 4: LangGraph

1. Define typed workflow state.
2. Implement node wrappers.
3. Implement decision routing.
4. Add debug loop limits.
5. Persist workflow events after every node.

## Phase 5: Backend APIs

1. Implement `/generate`.
2. Implement project, log, report, and download APIs.
3. Add simulation/debug/synthesis re-run APIs.
4. Add API tests.

## Phase 6: Frontend

1. Build dark dashboard shell.
2. Build Generate RTL page.
3. Build workflow timeline.
4. Build generated file browser.
5. Build reports and history pages.
6. Build settings page.

## Phase 7: Quality and Deployment

1. Add unit and integration tests.
2. Add Dockerfiles and Docker Compose.
3. Add CI-ready scripts.
4. Add deployment notes for Render and Railway.
5. Polish documentation and sample projects.
