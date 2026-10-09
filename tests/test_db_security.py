"""
Tests for the SQLite read-only authorizer layer (src/config/db.py).

The project's authorizer blocks CREATE_TABLE and all mutations, so we
seed the test table BEFORE installing the authorizer, then install it
to guard subsequent statements.
"""

import sqlite3
import pytest

from src.config.db import DB


@pytest.fixture
def secure_conn():
    conn = sqlite3.connect(":memory:")
    db = DB()

    # Seed BEFORE installing authorizer (CREATE/INSERT are blocked)
    conn.execute("CREATE TABLE t(id INTEGER PRIMARY KEY, val TEXT)")
    conn.execute("INSERT INTO t(id, val) VALUES (1, 'hello')")
    conn.commit()

    # Install the read-only authorizer for the test body
    conn.set_authorizer(db._authorizer)
    yield conn
    conn.close()


def _run(conn, sql):
    try:
        cur = conn.execute(sql)
        if cur.description is not None:
            cur.fetchall()
        return True, None
    except sqlite3.OperationalError as e:
        return False, str(e)
    except sqlite3.DatabaseError as e:
        return False, str(e)


# --- Reads are allowed ---

def test_select_allowed(secure_conn):
    ok, err = _run(secure_conn, "SELECT val FROM t WHERE id = 1")
    assert ok, f"read-only SELECT should be allowed, got error: {err}"


def test_select_count_allowed(secure_conn):
    ok, err = _run(secure_conn, "SELECT COUNT(*) FROM t")
    assert ok, err
    assert secure_conn.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 1


# --- Mutations are denied ---
# The sqlite3 authorizer returns SQLITE_DENY → sqlite3 raises
# "not authorized"

@pytest.mark.parametrize(
    "sql",
    [
        "INSERT INTO t(id, val) VALUES (2, 'evil')",
        "UPDATE t SET val = 'hacked' WHERE id = 1",
        "DELETE FROM t WHERE id = 1",
        "DROP TABLE t",
        "CREATE TABLE evil(id INTEGER)",
        "ALTER TABLE t ADD COLUMN bad TEXT",
    ],
)
def test_mutation_denied(secure_conn, sql):
    ok, err = _run(secure_conn, sql)
    assert not ok, f"mutation should be denied, but it succeeded: {sql}"
    assert "not authorized" in (err or "").lower(), f"unexpected error: {err}"


def test_attach_denied(secure_conn):
    ok, err = _run(secure_conn, "ATTACH DATABASE 'evil.db' AS evil")
    assert not ok
    assert "not authorized" in (err or "").lower()
