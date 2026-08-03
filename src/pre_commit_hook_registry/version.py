"""Package version resolution."""

from importlib.metadata import PackageNotFoundError, version


def get_version() -> str:
    """Return the installed package version.

    Returns:
        Installed distribution version or a local development fallback.
    """
    try:
        return version("pre-commit-hook-registry")
    except PackageNotFoundError:
        return "0.0.0+local"
