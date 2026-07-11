from app.schemas.requirement_spec import RequirementSpec


spec = RequirementSpec(
    module_name="16-bit ALU",
    description="Arithmetic Logic Unit",
    inputs=[
        "A",
        "B",
        "opcode"
    ],
    outputs=[
        "result"
    ],
    operations=[
        "ADD",
        "SUB"
    ],
    parameters={
        "width":16
    },
    verification_points=[
        "overflow check"
    ]
)


print(spec.model_dump())