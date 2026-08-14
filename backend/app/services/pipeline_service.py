"""
Pipeline Service.

Coordinates the complete VeriCore AI design flow.
"""

from __future__ import annotations

from pathlib import Path

from backend.app.agents.debug_agent import DebugAgent
from backend.app.agents.requirement_agent import RequirementAgent
from backend.app.agents.rtl_agent import RTLAgent
from backend.app.agents.verification_agent import VerificationAgent
from backend.app.schemas.documentation_report import DocumentationReport
from backend.app.services.code_generation_service import (
    CodeGenerationService,
)
from backend.app.services.documentation_service import (
    DocumentationService,
)
from backend.app.services.simulation_service import (
    SimulationService,
)
from backend.app.services.synthesis_service import (
    SynthesisService,
)
from backend.app.services.artifact_service import (
    ArtifactService,
)
from backend.app.services.rtl_repair_service import (
    RTLRepairService,
)


class PipelineService:
    """
    Coordinates the complete VeriCore AI workflow.
    """

    def __init__(self) -> None:
        self.requirement_agent = RequirementAgent()
        self.rtl_agent = RTLAgent()
        self.verification_agent = VerificationAgent()
        self.artifact_service = ArtifactService()
        self.code_generation_service = CodeGenerationService()
        self.simulation_service = SimulationService()
        self.synthesis_service = SynthesisService()
        self.documentation_service = DocumentationService()
        self.rtl_repair_service = RTLRepairService()
        self.debug_agent = DebugAgent()
        self.max_debug_iterations = 3

    def execute(
        self,
        requirement_text: str,
        output_directory: Path,
    ) -> DocumentationReport:
        """
        Execute the complete VeriCore AI pipeline.
        Parameters
        ----------
        requirement_text:
            Natural-language hardware specification.

        output_directory:
            Directory where generated artifacts are stored.

        Returns
        -------
        DocumentationReport
            Complete pipeline result.
        """
        print("\n########################################")
        print("### NEW PIPELINE SERVICE IS RUNNING ###")
        print("########################################\n")
        # ----------------------------------------
        # Requirement Analysis
        # ----------------------------------------
        print("STEP 1: Before RequirementAgent")
        requirement_spec = self.requirement_agent.execute(
        
            requirement_text
        )
        print("STEP 2: After RequirementAgent")

        # ----------------------------------------
        # RTL Generation
        # ----------------------------------------
        print("STEP 3: Before RTLAgent")

        rtl_design = self.rtl_agent.execute(
            requirement_spec
        )
        print("STEP 4: After RTLAgent")
        print("\nRTL FINISHED\n")

        # ----------------------------------------
        # Verification Planning
        # ----------------------------------------
        print("\nABOUT TO CALL VERIFICATION AGENT\n")
        print("STEP 5: Before VerificationAgent")
        verification_plan = self.verification_agent.execute(
            requirement_spec,
            rtl_design,
        )
        print("STEP 6: After VerificationAgent")
        print("\nVERIFICATION AGENT RETURNED\n")
        # ----------------------------------------
        # HDL Generation
        # ----------------------------------------
        print("STEP 7: Before CodeGeneration")
        rtl_source, testbench_source = (
            self.code_generation_service.generate(
                rtl_design,
                verification_plan,
            )
        
        )
        print("STEP 8: After CodeGeneration")
        # ----------------------------------------
        # Create Project Artifacts
        # ----------------------------------------
   
        project_paths = self.artifact_service.create_project(
            requirement_spec.module_name
        )
        rtl_file = self.artifact_service.save_rtl(
            rtl_directory=project_paths["rtl"],
            module_name=requirement_spec.module_name,
            rtl_source=rtl_source,
        )
        testbench_file = self.artifact_service.save_testbench(
            testbench_directory=project_paths["testbench"],
            module_name=requirement_spec.module_name,
            testbench_source=testbench_source,
        )

        # ----------------------------------------
        # Simulation
        # ----------------------------------------

        simulation_result = None
        synthesis_result = None
        post_synthesis_simulation_result = None

        debug_report = None

        for attempt in range(self.max_debug_iterations):

            simulation_result = (
                self.simulation_service.simulate(
                    rtl_file=rtl_file,
                    testbench_file=testbench_file,
                    working_directory=project_paths["simulation"],
                )
            )

            if not simulation_result.simulation_success:
                debug_report = self.debug_agent.execute(
                    simulation_result
                )
                rtl_design = self.rtl_repair_service.repair(
                    requirement_spec=requirement_spec,
                    debug_report=debug_report,
                )
                rtl_source, testbench_source = (
                    self.code_generation_service.generate(
                        rtl_design,
                        verification_plan,
                    )
                )
                rtl_file = self.artifact_service.save_rtl(
                    rtl_directory=project_paths["rtl"],
                    module_name=requirement_spec.module_name,
                    rtl_source=rtl_source,
                )
                testbench_file = self.artifact_service.save_testbench(
                    testbench_directory=project_paths["testbench"],
                    module_name=requirement_spec.module_name,
                    testbench_source=testbench_source,
                )
                continue

            synthesis_result = self.synthesis_service.synthesize(
                rtl_source=rtl_source,
                top_module=requirement_spec.module_name,
                output_directory=project_paths["synthesis"],
            )

            # ----------------------------------------
            # Synthesis Failure → Debug / Repair
            # ----------------------------------------

            if not synthesis_result.synthesis_success:
                debug_report = self.debug_agent.execute(
                    simulation_result
                )

                rtl_design = self.rtl_repair_service.repair(
                    requirement_spec=requirement_spec,
                    debug_report=debug_report,
                )

                rtl_source, testbench_source = (
                    self.code_generation_service.generate(
                        rtl_design,
                        verification_plan,
                    )
                )

                rtl_file = self.artifact_service.save_rtl(
                    rtl_directory=project_paths["rtl"],
                    module_name=requirement_spec.module_name,
                    rtl_source=rtl_source,
                )

                testbench_file = self.artifact_service.save_testbench(
                    testbench_directory=project_paths["testbench"],
                    module_name=requirement_spec.module_name,
                    testbench_source=testbench_source,
                )

                continue

            # ----------------------------------------
            # Post-Synthesis Simulation
            # ----------------------------------------

            if synthesis_result.netlist_path is None:
                raise RuntimeError(
                    "Synthesis reported success but no synthesized netlist was produced."
                )

            netlist_file = Path(
                synthesis_result.netlist_path
            )

            if not netlist_file.exists():
                raise FileNotFoundError(
                    f"Synthesized netlist not found: {netlist_file}"
                )

            post_synthesis_simulation_result = (
                self.simulation_service.simulate(
                    rtl_file=netlist_file,
                    testbench_file=testbench_file,
                    working_directory=project_paths["synthesis"],
                )
            )

            break

            

        # ----------------------------------------
        # Documentation Object
        # ----------------------------------------

        report = self._build_report(
            requirement_text=requirement_text,
            requirement_spec=requirement_spec,
            rtl_design=rtl_design,
            verification_plan=verification_plan,
            rtl_source=rtl_source,
            testbench_source=testbench_source,
            simulation_result=simulation_result,
            synthesis_result=synthesis_result,
            post_synthesis_simulation_result=(
                post_synthesis_simulation_result
            ),
            debug_report=debug_report,
        )
        # ----------------------------------------
        # Save Documentation
        # ----------------------------------------

        self.documentation_service.generate(
            report,
            project_paths["documentation"],
        )

        return report

        def _build_report(
            self,
            requirement_text: str,
            requirement_spec,
            rtl_design,
            verification_plan,
            rtl_source: str,
            testbench_source: str,
            simulation_result,
            synthesis_result,
            post_synthesis_simulation_result,
            debug_report=None,
        ) -> DocumentationReport:
            """
            Build the final documentation report.
            """

        return DocumentationReport(
            requirement_text=requirement_text,
            requirement_spec=requirement_spec,
            rtl_design=rtl_design,
            verification_plan=verification_plan,
            rtl_source=rtl_source,
            testbench_source=testbench_source,
            simulation_result=simulation_result,
            synthesis_result=synthesis_result,
            post_synthesis_simulation_result=(
                post_synthesis_simulation_result
            ),
            debug_report=debug_report,
            generated_files={},
            success=(
                simulation_result is not None
                and simulation_result.simulation_success
                and synthesis_result is not None
                and synthesis_result.synthesis_success
                and post_synthesis_simulation_result is not None
                and post_synthesis_simulation_result.simulation_success
            ),
        )

    def _needs_debug(
        self,
        simulation_result,
        synthesis_result,
    ) -> bool:
        """
        Determine whether the pipeline requires a debug iteration.
        """

        if not simulation_result.simulation_success:
            return True

        if not synthesis_result.synthesis_success:
            return True

        return False
