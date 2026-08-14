"""
Testbench Generator

Coordinates the complete Verilog testbench generation process
by delegating individual responsibilities to specialized
generator classes.
"""

from __future__ import annotations
from backend.app.generators.result_checker_generator import ResultCheckerGenerator
from backend.app.generators.assertion_generator import AssertionGenerator
from backend.app.generators.clock_generator import ClockGenerator
from backend.app.generators.dut_instantiator import DUTInstantiator
from backend.app.generators.module_footer_generator import ModuleFooterGenerator
from backend.app.generators.module_header_generator import ModuleHeaderGenerator
from backend.app.generators.reset_generator import ResetGenerator
from backend.app.generators.signal_generator import SignalGenerator
from backend.app.generators.stimulus_generator import StimulusGenerator
from backend.app.generators.waveform_generator import WaveformGenerator
from backend.app.schemas.rtl_design import RTLDesign


class TestbenchGenerator:
    __test__ = False
    """
    Generates a complete Verilog testbench by orchestrating
    specialized generator components.
    """

    def __init__(self) -> None:
        self.header_generator = ModuleHeaderGenerator()
        self.signal_generator = SignalGenerator()
        self.dut_instantiator = DUTInstantiator()
        self.clock_generator = ClockGenerator()
        self.reset_generator = ResetGenerator()
        self.waveform_generator = WaveformGenerator()
        self.stimulus_generator = StimulusGenerator()
        self.assertion_generator = AssertionGenerator()
        self.footer_generator = ModuleFooterGenerator()
        self.result_checker_generator = ResultCheckerGenerator()
    def generate(
        self,
        rtl_design: RTLDesign,
        verification_plan=None,
    ) -> str:
        """
        Generate a complete Verilog testbench.

        Parameters
        ----------
        rtl_design:
            Structured RTL design.

        Returns
        -------
        str
            Complete Verilog testbench source.
        """

        requirement = rtl_design.requirement
        tb_name = f"tb_{requirement.module_name}"

        lines: list[str] = []

        # -------------------------------------------------
        # Module Header
        # -------------------------------------------------

        lines.extend(
            self.header_generator.generate(tb_name)
        )

        # -------------------------------------------------
        # Signal Declarations
        # -------------------------------------------------

        lines.extend(
            self.signal_generator.generate(requirement)
        )

        # -------------------------------------------------
        # DUT Instantiation
        # -------------------------------------------------

        lines.extend(
            self.dut_instantiator.generate(requirement)
        )

        # -------------------------------------------------
        # Clock Generation
        # -------------------------------------------------

        lines.extend(
            self.clock_generator.generate(requirement)
        )

        # -------------------------------------------------
        # Reset Generation
        # -------------------------------------------------

        lines.extend(
            self.reset_generator.generate(requirement)
        )

        # -------------------------------------------------
        # Waveform Generation
        # -------------------------------------------------

        lines.extend(
            self.waveform_generator.generate(tb_name)
        )

        # -------------------------------------------------
        # Stimulus Generation
        # -------------------------------------------------

        lines.extend(
            self.stimulus_generator.generate(
                requirement,
                verification_plan,
            )
        )

        # -------------------------------------------------
        # Assertions
        # -------------------------------------------------

        lines.extend(
            self.assertion_generator.generate(requirement)
        )

        # -------------------------------------------------
        # Module Footer
        # -------------------------------------------------

        lines.extend(
            self.footer_generator.generate()
        )

        return "\n".join(lines)