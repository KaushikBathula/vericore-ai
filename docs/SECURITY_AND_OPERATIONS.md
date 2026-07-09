# Security and Operations

## Secrets

- Store API keys only in `.env`.
- Keep `.env` out of source control.
- Never return secrets through APIs, logs, reports, or frontend state.

## Input Validation

- Validate prompts for empty, oversized, or unsupported requests.
- Sanitize project names and generated filenames.
- Restrict public APIs to project IDs and artifact IDs.

## Command Safety

- Never build shell commands by concatenating raw user input.
- Use subprocess argument lists.
- Run tools inside a bounded project working directory.
- Apply timeouts to compile, simulation, synthesis, and report generation.
- Capture stdout, stderr, exit code, duration, and tool version.

## Error Handling

Handle:

- invalid prompts
- invalid RTL
- syntax errors
- simulation failures
- timeouts
- missing dependencies
- EDA tool crashes
- OpenAI API failures
- network failures
- file permission failures

## Observability

Log these streams:

- API requests and failures
- agent execution start/end
- prompt and completion metadata without secrets
- simulation commands and results
- debug iterations
- synthesis results
- report generation
- performance timing

## Deployment

The production deployment should separate:

- frontend service
- backend API service
- EDA toolchain image or worker
- SQLite volume for local deployments
- generated project artifact volume
