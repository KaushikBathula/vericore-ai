import json

from backend.app.schemas.verification_plan import VerificationPlan


class VerificationParser:

    @staticmethod
    def parse(response: str) -> VerificationPlan:
        data = json.loads(response)

        return VerificationPlan.model_validate(data)