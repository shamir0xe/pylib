from enum import Enum


class ExceptionTypes(Enum):
    AVL_TREE_INVALID = "avl_tree_invalid"
    BK_TREE_INVALID = "bk_tree_invalid"
    CONNECTION_INVALID = "connection_invalid"
    DATABASE_INVALID = "database_invalid"
    DB_SESSION_NOT_AVAILABLE = "db_session_not_available"
    DB_SESSION_NOT_FOUND = "db_session_not_found"
    ID_INVALID = "id_invalid"
    TIME_FORMAT_NOT_SUPPORTED = "time_format_not_supported"
    TRIE_TREE_INVALID = "trie_tree_invalid"
