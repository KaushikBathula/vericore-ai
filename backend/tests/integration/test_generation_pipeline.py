from backend.app.services.generation_service import GenerationService


def test_generation_pipeline():

    service = GenerationService()

    requirement = """
    Design a 16-bit ALU.
    It should support addition and subtraction.
    """

    requirement_spec, rtl_design, verification_plan = service.generate(
        requirement
    )

    # Requirement Agent
    assert requirement_spec.module_name

    # RTL Agent
    assert (
        rtl_design.requirement.module_name
        == requirement_spec.module_name
    )
    assert len(rtl_design.internal_signals) > 0
    assert len(rtl_design.derived_operations) > 0

    # Verification Agent
    assert verification_plan