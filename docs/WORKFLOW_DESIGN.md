# LangGraph Workflow Design

## Graph

```text
START
  │
  ▼
Coordinator Agent
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
  ▼
Decision Node
  │
  ├── Success
  │      │
  │      ▼
  │  Synthesis Agent
  │      │
  │      ▼
  │ Documentation Agent
  │      │
  │      ▼
  │      END
  │
  └── Failure
         │
         ▼
     Debug Agent
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
         └──────────────► Decision Node
```

## State

The workflow state is shared across all LangGraph nodes and maintained by the Coordinator Agent. Every agent receives the current workflow state, updates only its relevant fields, and returns the updated state to the Coordinator Agent.

The workflow state includes:

- current workflow stage
- active agent
- retry counter
- execution timestamps
- generated artifact paths
- workflow execution history

## Decision Node

The Decision Node is responsible for determining the next workflow step.

Possible outcomes:

- Continue to synthesis
- Send the design to the Debug Agent
- Retry simulation
- Abort due to unrecoverable failure
- Complete the workflow successfully

The Coordinator Agent records every decision in the workflow log.

## Debug Loop

After RTL regeneration, the workflow automatically returns to the Verification Agent and Simulation Agent before another decision is made. This iterative loop continues until the design passes verification or the maximum retry limit is reached.
The Debug Agent receives:

- structured spec
- current RTL
- testbench
- compiler errors
- simulation output
- previous debug attempts

It should produce a structured patch instruction, not free-form guesses. The RTL Agent then regenerates or repairs RTL using that structured debug context.

## Stop Conditions

- Success: compilation passes, simulation passes, synthesis completes, documentation generated.
- Controlled failure: debug iteration limit reached.
- Fatal failure: missing dependency, invalid input, EDA tool crash, API outage, or unsafe command request.
  
## Coordinator Agent

The Coordinator Agent is the central orchestration component of VeriCore AI.

Responsibilities include:

- Initialize workflow execution
- Maintain workflow state
- Select the next agent
- Coordinate LangGraph execution
- Handle retry logic
- Monitor execution progress
- Record workflow history
- Manage generated artifacts
- Detect workflow completion
- Gracefully terminate failed executions

## Workflow Characteristics

The LangGraph workflow demonstrates core Agentic AI capabilities:

- Multi-agent collaboration
- Centralized orchestration
- Shared workflow memory
- Autonomous decision making
- Iterative debugging
- Tool invocation
- State persistence
- Recoverable execution
- Modular extensibility