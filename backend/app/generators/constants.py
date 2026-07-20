"""
Constants used by the Verilog generation pipeline.

Keeping these values centralized avoids hardcoded literals
throughout the generators and makes future extensions easier.
"""

# ---------------------------------------------------------------------
# Clock Detection
# ---------------------------------------------------------------------

CLOCK_SIGNAL_NAMES: set[str] = {
    "clk",
    "clock",
}

# Default half-period used for generated clocks.
# Generates:
#
# always #5 clk = ~clk;
#
DEFAULT_CLOCK_HALF_PERIOD = 5