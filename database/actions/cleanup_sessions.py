from ...database.session_pools import SessionPools


class CleanupSessions:
    @staticmethod
    def cleanup() -> None:
        SessionPools().close_all()

