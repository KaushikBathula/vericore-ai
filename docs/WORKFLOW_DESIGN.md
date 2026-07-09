# LangGraph Workflow Design

## Graph

```text
START
  -> Requirement Agent
  -> RTL Agent
  -> Verification Agent
  -> Simulation Agent
  -> Decision Node
       success -> Synthesis Agent -> Documentation Agent -> END
       failure -> Debug Agent -> RTL Agent -> Simulation Agent
```

## State

The workflow state should include:

- original prompt
- project ID and run ID
- structured design specification
- RTL files
- testbench files
- simulation command result
- compiler diagnostics
- simulation diagnostics
- debug iteration count
- synthesis result
- generated documentation
- artifact registry
- workflow logs
- final status

## Decision Node

The decision node routes based on:

- compiler exit code
- simulation exit code
- presence of expected output markers
- maximum debug iteration count
- unrecoverable tool or API failure

## Debug Loop

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
