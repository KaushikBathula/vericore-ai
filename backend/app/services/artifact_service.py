from pathlib import Path

from backend.app.core.config import get_settings


class ArtifactService:
    """
    Handles creation and management of all generated project artifacts.
    """

    def __init__(self):
        settings = get_settings()
        self.base_directory = settings.generated_projects_dir

    def create_project(
        self,
        project_name: str,
    ) -> dict[str, Path]:
        """
        Create the directory structure for a generated project.
        """

        project_dir = self.base_directory / project_name

        rtl_dir = project_dir / "rtl"
        testbench_dir = project_dir / "testbench"
        simulation_dir = project_dir / "simulation"
        synthesis_dir = project_dir / "synthesis"
        documentation_dir = project_dir / "documentation"

        for directory in [
            project_dir,
            rtl_dir,
            testbench_dir,
            simulation_dir,
            synthesis_dir,
            documentation_dir,
        ]:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

        return {
            "root": project_dir,
            "rtl": rtl_dir,
            "testbench": testbench_dir,
            "simulation": simulation_dir,
            "synthesis": synthesis_dir,
            "documentation": documentation_dir,
        }

    def save_rtl(
        self,
        rtl_directory: Path,
        module_name: str,
        rtl_source: str,
    ) -> Path:
        """
        Save the generated RTL Verilog file.
        """

        rtl_file = rtl_directory / f"{module_name}.v"

        rtl_file.write_text(
            rtl_source,
            encoding="utf-8",
        )

        return rtl_file
    def save_testbench(
        self,
        testbench_directory: Path,
        module_name: str,
        testbench_source: str,
    ) -> Path:
        """
        Save the generated Verilog testbench.
        """

        testbench_file = (
            testbench_directory
            / f"tb_{module_name}.v"
        )

        testbench_file.write_text(
            testbench_source,
            encoding="utf-8",
        )

        return testbench_file