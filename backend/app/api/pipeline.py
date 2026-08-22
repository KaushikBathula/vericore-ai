"""
Pipeline API.

Exposes the complete VeriCore AI pipeline.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from backend.app.core.config import get_settings
from backend.app.schemas.pipeline_artifacts import (
    PipelineArtifactDownloadUrls,
    PipelineArtifactPaths,
    PipelineArtifactsResponse,
)
from backend.app.schemas.pipeline_request import PipelineRequest
from backend.app.schemas.pipeline_response import PipelineResponse
from backend.app.services.pipeline_service import PipelineService

router = APIRouter()


def _project_directory(module_name: str) -> Path:
    """
    Resolve a generated project directory without allowing path traversal.
    """

    if (
        not module_name
        or "/" in module_name
        or "\\" in module_name
        or module_name in {".", ".."}
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid module name.",
        )

    base_directory = get_settings().generated_projects_dir.resolve()
    project_directory = (base_directory / module_name).resolve()

    if (
        project_directory != base_directory
        and base_directory not in project_directory.parents
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid module path.",
        )

    if not project_directory.exists() or not project_directory.is_dir():
        raise HTTPException(
            status_code=404,
            detail="Generated project not found.",
        )

    return project_directory


def _relative_path(path: Path | None) -> str | None:
    if path is None or not path.exists():
        return None

    return path.as_posix()


def _read_text(path: Path | None) -> str | None:
    if path is None or not path.exists() or not path.is_file():
        return None

    return path.read_text(
        encoding="utf-8",
        errors="replace",
    )


def _artifact_file_map(project_directory: Path) -> dict[str, Path]:
    module_name = project_directory.name

    return {
        "rtl": project_directory / "rtl" / f"{module_name}.v",
        "testbench": (
            project_directory
            / "testbench"
            / f"tb_{module_name}.v"
        ),
        "simulation_output": (
            project_directory
            / "simulation"
            / "simulation.out"
        ),
        "simulation_waveform": (
            project_directory
            / "simulation"
            / f"tb_{module_name}.vcd"
        ),
        "synthesis_design": (
            project_directory
            / "synthesis"
            / "design.v"
        ),
        "synthesis_script": (
            project_directory
            / "synthesis"
            / "design.ys"
        ),
        "synthesis_netlist": (
            project_directory
            / "synthesis"
            / "netlist.v"
        ),
        "synthesis_report": (
            project_directory
            / "synthesis"
            / "yosys.log"
        ),
        "synthesis_schematic_svg": (
            project_directory
            / "synthesis"
            / f"{module_name}.svg"
        ),
        "synthesis_schematic_dot": (
            project_directory
            / "synthesis"
            / f"{module_name}.dot"
        ),
        "post_synthesis_simulation_output": (
            project_directory
            / "synthesis"
            / "simulation.out"
        ),
        "post_synthesis_waveform": (
            project_directory
            / "synthesis"
            / f"tb_{module_name}.vcd"
        ),
        "documentation": (
            project_directory
            / "documentation"
            / "report.md"
        ),
    }


def _download_url(
    module_name: str,
    artifact_name: str,
    path: Path,
) -> str | None:
    if not path.exists() or not path.is_file():
        return None

    return (
        f"/api/pipeline/artifacts/"
        f"{module_name}/files/{artifact_name}"
    )


@router.post(
    "/run",
    response_model=PipelineResponse,
)
def run_pipeline(
    request: PipelineRequest,
) -> PipelineResponse:
    """
    Execute the complete VeriCore AI pipeline.
    """

    print("\n############################################")
    print("########## PIPELINE API HIT ################")
    print("############################################\n")

    try:
        service = PipelineService()

        print("PipelineService Object :", service)
        print("PipelineService Class  :", PipelineService)
        print("PipelineService Module :", PipelineService.__module__)
        print("Requirement Received   :", request.requirement)
        print()

        report = service.execute(
            requirement_text=request.requirement,
            output_directory=Path("generated_projects"),
        )

        print("\n########## PIPELINE COMPLETED ##########\n")

        report_path = (
            Path("generated_projects")
            / report.requirement_spec.module_name
            / "documentation"
            / "report.md"
        ).as_posix()

        return PipelineResponse(
            success=report.success,
            report_path=report_path,
            message="Pipeline executed successfully.",
        )

    except Exception as exc:

        print("\n########## PIPELINE FAILED ##########")
        print(exc)
        print("#####################################\n")

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get(
    "/artifacts/{module_name}",
    response_model=PipelineArtifactsResponse,
)
def get_pipeline_artifacts(
    module_name: str,
) -> PipelineArtifactsResponse:
    """
    Return generated artifact contents and file locations
    for a project.
    """

    project_directory = _project_directory(module_name)
    files = _artifact_file_map(project_directory)

    return PipelineArtifactsResponse(
        module_name=module_name,
        project_path=project_directory.as_posix(),
        artifact_paths=PipelineArtifactPaths(
            rtl=_relative_path(files["rtl"]),
            testbench=_relative_path(files["testbench"]),
            simulation_output=_relative_path(
                files["simulation_output"]
            ),
            simulation_waveform=_relative_path(
                files["simulation_waveform"]
            ),
            synthesis_design=_relative_path(
                files["synthesis_design"]
            ),
            synthesis_script=_relative_path(
                files["synthesis_script"]
            ),
            synthesis_netlist=_relative_path(
                files["synthesis_netlist"]
            ),
            synthesis_report=_relative_path(
                files["synthesis_report"]
            ),
            synthesis_schematic_svg=_relative_path(
                files["synthesis_schematic_svg"]
            ),
            synthesis_schematic_dot=_relative_path(
                files["synthesis_schematic_dot"]
            ),
            post_synthesis_simulation_output=_relative_path(
                files["post_synthesis_simulation_output"]
            ),
            post_synthesis_waveform=_relative_path(
                files["post_synthesis_waveform"]
            ),
            documentation=_relative_path(
                files["documentation"]
            ),
        ),
        download_urls=PipelineArtifactDownloadUrls(
            rtl=_download_url(
                module_name,
                "rtl",
                files["rtl"],
            ),
            testbench=_download_url(
                module_name,
                "testbench",
                files["testbench"],
            ),
            simulation_output=_download_url(
                module_name,
                "simulation_output",
                files["simulation_output"],
            ),
            simulation_waveform=_download_url(
                module_name,
                "simulation_waveform",
                files["simulation_waveform"],
            ),
            synthesis_netlist=_download_url(
                module_name,
                "synthesis_netlist",
                files["synthesis_netlist"],
            ),
            synthesis_report=_download_url(
                module_name,
                "synthesis_report",
                files["synthesis_report"],
            ),
            synthesis_schematic_svg=_download_url(
                module_name,
                "synthesis_schematic_svg",
                files["synthesis_schematic_svg"],
            ),
            synthesis_schematic_dot=_download_url(
                module_name,
                "synthesis_schematic_dot",
                files["synthesis_schematic_dot"],
            ),
            post_synthesis_simulation_output=_download_url(
                module_name,
                "post_synthesis_simulation_output",
                files["post_synthesis_simulation_output"],
            ),
            post_synthesis_waveform=_download_url(
                module_name,
                "post_synthesis_waveform",
                files["post_synthesis_waveform"],
            ),
            documentation=_download_url(
                module_name,
                "documentation",
                files["documentation"],
            ),
        ),
        rtl_source=_read_text(files["rtl"]),
        testbench_source=_read_text(files["testbench"]),
        simulation_output=_read_text(
            files["simulation_output"]
        ),
        simulation_waveform_source=_read_text(
            files["simulation_waveform"]
        ),
        synthesis_report=_read_text(
            files["synthesis_report"]
        ),
        post_synthesis_simulation_output=_read_text(
            files["post_synthesis_simulation_output"]
        ),
        post_synthesis_waveform_source=_read_text(
            files["post_synthesis_waveform"]
        ),
        documentation_markdown=_read_text(
            files["documentation"]
        ),

    )


@router.get(
    "/artifacts/{module_name}/files/{artifact_name}",
)
def download_pipeline_artifact(
    module_name: str,
    artifact_name: str,
) -> FileResponse:
    """
    Download one generated pipeline artifact by whitelist name.
    """

    project_directory = _project_directory(module_name)
    files = _artifact_file_map(project_directory)

    if artifact_name not in files:
        raise HTTPException(
            status_code=404,
            detail="Artifact not found.",
        )

    artifact_file = files[artifact_name]

    if not artifact_file.exists() or not artifact_file.is_file():
        raise HTTPException(
            status_code=404,
            detail="Artifact file not found.",
        )

    return FileResponse(
        artifact_file,
        filename=artifact_file.name,
    )
