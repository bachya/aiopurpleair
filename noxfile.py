"""Define nox actions."""
import nox


@nox.session
def coverage(session: nox.sessions.Session) -> None:
    """Report test coverage.

    Args:
        session: A nox session.
    """
    args = session.posargs or [
        "-s",
        "--cov=aiopurpleair",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "tests/",
    ]
    session.run("poetry", "lock", external=True)
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session
def tests(session: nox.sessions.Session) -> None:
    """Run all tests.

    Args:
        session: A nox session.
    """
    args = session.posargs or ["-s", "tests/"]
    session.run("poetry", "lock", external=True)
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
