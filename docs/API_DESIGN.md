# API Design

All responses should use typed Pydantic schemas and consistent error envelopes.

## Endpoints

### `POST /generate`

Creates a project and runs the autonomous LangGraph workflow.

Request fields:

- `prompt`: natural-language hardware specification.
- `target_language`: `verilog` or `systemverilog`.
- `max_debug_iterations`: bounded retry count.
- `enable_waveform`: whether to emit VCD output.

Response fields:

- `project_id`
- `run_id`
- `status`
- `workflow_trace`
- `artifacts`

### `POST /simulate`

Runs or re-runs simulation for an existing project.

### `POST /debug`

Runs a debug iteration using existing compiler/simulation logs.

### `POST /synthesis`

Runs Yosys synthesis and stores synthesis reports.

### `GET /projects`

Lists generated projects with status, timestamps, module type, and latest run result.

### `GET /logs`

Returns API, agent, workflow, simulation, debug, and synthesis logs. Supports filtering by `project_id`, `run_id`, `level`, and `component`.

### `GET /reports`

Returns report metadata or a rendered report body for a project.

### `GET /download`

Downloads a project archive or a single artifact.

## Error Envelope

```json
{
  "error": {
    "code": "SIMULATION_FAILED",
    "message": "Simulation failed after 3 debug iterations.",
    "details": {}
  }
}
```

## REST Rules

- Validate all input at the API boundary.
- Return stable machine-readable error codes.
- Use IDs instead of filesystem paths in public APIs.
- Never expose internal absolute paths or secrets.
- Make long-running workflow status queryable by project/run ID.
