# File Responsibilities

## Root

- `README.md`: project overview and documentation index.
- `.env.example`: safe example environment variables.
- `.gitignore`: ignored local artifacts, environments, logs, and generated outputs.
- `pyproject.toml`: Python tooling, formatting, linting, and pytest config.
- `requirements.txt`: backend runtime dependencies.
- `docker-compose.yml`: local multi-container development stack.

## Backend

- `backend/app/main.py`: FastAPI app factory and startup wiring.
- `backend/app/api/router.py`: central API router registration.
- `backend/app/api/routes/*.py`: thin REST route modules.
- `backend/app/core/config.py`: environment-backed settings.
- `backend/app/core/logging.py`: logging setup.
- `backend/app/core/exceptions.py`: domain and API exception mapping.
- `backend/app/core/security.py`: API security helpers.
- `backend/app/models/*.py`: database models.
- `backend/app/schemas/*.py`: Pydantic request and response contracts.
- `backend/app/services/*.py`: application use cases.
- `backend/app/repositories/*.py`: database persistence abstractions.
- `backend/app/dependencies/*.py`: dependency injection providers.
- `backend/app/utils/*.py`: small framework-independent helpers.

## Agents

- `agents/base/agent.py`: shared abstract agent interface.
- `agents/base/prompt_loader.py`: prompt loading from files.
- `agents/base/llm_client.py`: LLM abstraction over OpenAI SDK or LangChain.
- `agents/<name>/agent.py`: implementation for one agent responsibility only.

## Prompts

- `prompts/<agent>/system.md`: role, constraints, and output rules.
- `prompts/<agent>/user.md`: task template and runtime variables.

Prompts must not be embedded in Python files.

## Tools

- `tools/eda/base.py`: common command result and adapter interface.
- `tools/eda/icarus.py`: Icarus Verilog compile/simulate adapter.
- `tools/eda/verilator.py`: Verilator lint adapter.
- `tools/eda/yosys.py`: Yosys synthesis adapter.
- `tools/eda/gtkwave.py`: waveform artifact adapter.
- `tools/eda/opensta.py`: optional timing analysis adapter.
- `tools/openai/client.py`: OpenAI client creation and retries.
- `tools/filesystem/project_writer.py`: generated project file writer.
- `tools/filesystem/artifact_store.py`: artifact lookup and archive creation.
- `tools/reporting/markdown.py`: Markdown report generation.
- `tools/reporting/pdf.py`: PDF-ready export path.
- `tools/security/sanitization.py`: filename and input sanitization.
- `tools/security/subprocess.py`: safe subprocess execution policy.

## Workflow

- `workflow/graph.py`: LangGraph graph builder.
- `workflow/nodes/*.py`: node functions wrapping agents and tools.
- `workflow/edges/decision.py`: conditional routing logic.
- `workflow/state/design_state.py`: typed graph state.

## Frontend

- `frontend/app/*/page.tsx`: route pages.
- `frontend/components/layout/*.tsx`: dashboard shell.
- `frontend/components/workflow/*.tsx`: workflow visualization.
- `frontend/components/files/*.tsx`: generated file browser.
- `frontend/lib/api.ts`: typed API client.
- `frontend/hooks/*.ts`: reusable data hooks.
- `frontend/types/api.ts`: shared frontend API types.
- `frontend/styles/globals.css`: global Tailwind styles.

## Tests

- `backend/tests/unit/`: backend unit tests.
- `backend/tests/integration/`: workflow and tool integration tests.
- `backend/tests/api/`: FastAPI route tests.
- `tests/e2e/`: future browser-level tests.
