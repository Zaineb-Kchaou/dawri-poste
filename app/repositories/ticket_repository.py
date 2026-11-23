"""Couche accès aux données (SQLite).

Point clé du UC1 (UC à risque) : l'attribution du numéro de ticket doit rester correcte
quand plusieurs clients arrivent au même moment. Trois protections se cumulent :

1. Le numéro est calculé DANS la base, à l'intérieur d'une transaction BEGIN IMMEDIATE qui
   verrouille l'écriture : deux demandes ne peuvent pas lire le même "dernier numéro".
2. Une contrainte UNIQUE (bureau, service, jour, numéro) rend un doublon impossible,
   même si l'application contenait un bug.
3. Un index unique partiel interdit deux tickets WAITING pour le même client et le même service.

Avec PostgreSQL, on remplacerait (1) par un compteur verrouillé (SELECT ... FOR UPDATE)
ou par UPDATE ... RETURNING.
"""
import sqlite3

from app.errors import ActiveTicketExists
from app.models import Ticket

SCHEMA = """
CREATE TABLE IF NOT EXISTS ticket (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    bureau_id     TEXT    NOT NULL,
    service_code  TEXT    NOT NULL,
    day           TEXT    NOT NULL,
    number        INTEGER NOT NULL,
    client_phone  TEXT    NOT NULL,
    status        TEXT    NOT NULL DEFAULT 'WAITING',
    created_at    TEXT    NOT NULL,
    UNIQUE (bureau_id, service_code, day, number)
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_one_waiting_ticket_per_client
    ON ticket (bureau_id, service_code, day, client_phone)
    WHERE status = 'WAITING';
"""


class TicketRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        # isolation_level=None : on gère nous-mêmes BEGIN / COMMIT.
        # timeout : une demande attend son tour (verrou) au lieu d'échouer immédiatement.
        conn = sqlite3.connect(self.db_path, timeout=30, isolation_level=None)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self) -> None:
        conn = self._connect()
        try:
            conn.executescript(SCHEMA)
        finally:
            conn.close()

    def create_with_next_number(self, bureau_id: str, service_code: str, day: str,
                                client_phone: str, created_at: str) -> Ticket:
        """Crée un ticket avec le prochain numéro libre, de façon atomique."""
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")  # un seul écrivain à la fois
            number = conn.execute(
                "SELECT COALESCE(MAX(number), 0) + 1 FROM ticket "
                "WHERE bureau_id = ? AND service_code = ? AND day = ?",
                (bureau_id, service_code, day),
            ).fetchone()[0]
            cur = conn.execute(
                "INSERT INTO ticket (bureau_id, service_code, day, number, client_phone, status, created_at) "
                "VALUES (?, ?, ?, ?, ?, 'WAITING', ?)",
                (bureau_id, service_code, day, number, client_phone, created_at),
            )
            ticket_id = cur.lastrowid
            conn.execute("COMMIT")
        except sqlite3.IntegrityError as exc:
            self._rollback(conn)
            if "client_phone" in str(exc):
                raise ActiveTicketExists() from exc
            raise
        except Exception:
            self._rollback(conn)
            raise
        finally:
            conn.close()
        return Ticket(ticket_id, bureau_id, service_code, day, number, client_phone, "WAITING", created_at)

    def count_waiting_up_to(self, bureau_id: str, service_code: str, day: str, number: int) -> int:
        """Position dans la file : nombre de tickets WAITING dont le numéro est <= number."""
        conn = self._connect()
        try:
            return conn.execute(
                "SELECT COUNT(*) FROM ticket WHERE bureau_id = ? AND service_code = ? AND day = ? "
                "AND status = 'WAITING' AND number <= ?",
                (bureau_id, service_code, day, number),
            ).fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def _rollback(conn: sqlite3.Connection) -> None:
        try:
            conn.execute("ROLLBACK")
        except sqlite3.Error:
            pass
