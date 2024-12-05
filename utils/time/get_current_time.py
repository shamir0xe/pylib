from datetime import datetime, UTC


class GetCurrentTime:
    @staticmethod
    def get() -> datetime:
        return datetime.now(UTC)
