from ulid import ULID


class GenerateId:
    """Generate ULID"""

    @staticmethod
    def generate() -> str:
        return str(ULID())
