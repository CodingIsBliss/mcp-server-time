"""MCP Time Server – exposes timezone-aware time tools over streamable-http.

Uses only the Python standard library (zoneinfo) so there are no extra
dependencies beyond the MCP SDK.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo, available_timezones

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Time")


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def get_current_time(timezone_name: str = "UTC") -> dict:
    """Get the current date & time in a given IANA timezone.

    Args:
        timezone_name: IANA timezone name, e.g. "America/New_York", "Asia/Tokyo".
                       Defaults to "UTC".
    """
    try:
        tz = ZoneInfo(timezone_name)
    except (KeyError, Exception):
        return {"error": f"Unknown timezone: {timezone_name}. Use list_timezones to see valid names."}

    now = datetime.now(tz)
    return {
        "timezone": timezone_name,
        "datetime": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day_of_week": now.strftime("%A"),
        "utc_offset": now.strftime("%z"),
    }


@mcp.tool()
def convert_time(
    time_str: str,
    from_timezone: str,
    to_timezone: str,
) -> dict:
    """Convert a time from one timezone to another.

    Args:
        time_str: Time string in ISO-8601 format, e.g. "2026-03-24T15:30:00".
        from_timezone: Source IANA timezone, e.g. "America/Los_Angeles".
        to_timezone: Target IANA timezone, e.g. "Europe/London".
    """
    try:
        from_tz = ZoneInfo(from_timezone)
        to_tz = ZoneInfo(to_timezone)
    except (KeyError, Exception) as exc:
        return {"error": f"Invalid timezone: {exc}"}

    try:
        dt = datetime.fromisoformat(time_str)
    except ValueError:
        return {"error": f"Cannot parse '{time_str}'. Use ISO-8601 format like 2026-03-24T15:30:00"}

    # Attach source tz if naive
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=from_tz)

    converted = dt.astimezone(to_tz)
    return {
        "original": {
            "timezone": from_timezone,
            "datetime": dt.isoformat(),
        },
        "converted": {
            "timezone": to_timezone,
            "datetime": converted.isoformat(),
            "date": converted.strftime("%Y-%m-%d"),
            "time": converted.strftime("%H:%M:%S"),
            "day_of_week": converted.strftime("%A"),
        },
    }


@mcp.tool()
def time_difference(timezone_a: str, timezone_b: str) -> dict:
    """Calculate the current time difference between two timezones.

    Args:
        timezone_a: First IANA timezone.
        timezone_b: Second IANA timezone.
    """
    try:
        tz_a = ZoneInfo(timezone_a)
        tz_b = ZoneInfo(timezone_b)
    except (KeyError, Exception) as exc:
        return {"error": f"Invalid timezone: {exc}"}

    now = datetime.now(timezone.utc)
    offset_a = now.astimezone(tz_a).utcoffset() or timedelta()
    offset_b = now.astimezone(tz_b).utcoffset() or timedelta()

    diff = offset_b - offset_a
    total_minutes = int(diff.total_seconds() / 60)
    hours, minutes = divmod(abs(total_minutes), 60)
    sign = "+" if total_minutes >= 0 else "-"

    return {
        "timezone_a": timezone_a,
        "timezone_b": timezone_b,
        "difference": f"{sign}{hours:02d}:{minutes:02d}",
        "difference_hours": total_minutes / 60,
        "current_time_a": now.astimezone(tz_a).isoformat(),
        "current_time_b": now.astimezone(tz_b).isoformat(),
    }


@mcp.tool()
def list_timezones(region: str = "") -> dict:
    """List available IANA timezones, optionally filtered by region prefix.

    Args:
        region: Filter prefix e.g. "America", "Europe", "Asia". Empty = all.
    """
    all_tz = sorted(available_timezones())
    if region:
        all_tz = [tz for tz in all_tz if tz.lower().startswith(region.lower())]
    return {"count": len(all_tz), "timezones": all_tz[:100]}  # cap at 100


def main():
    """Entry-point used by the console-script."""
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
