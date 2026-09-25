"""Flat-file persistence for profiles (JSON). No printing, no domain logic."""
import json
import logging
import os

logger = logging.getLogger(__name__)


def load_profiles(path: str) -> list[dict]:
    """Load all profiles. A missing file gives []; a corrupt file is set aside."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError("profiles file must contain a JSON list")
        return data
    except (json.JSONDecodeError, ValueError, OSError) as error:
        logger.error("Could not read %s (%s); starting empty", path, error)
        _quarantine_corrupt_file(path)
        return []


def _quarantine_corrupt_file(path: str) -> None:
    """Rename an unreadable file so it is not overwritten silently."""
    try:
        os.replace(path, path + ".corrupt")
    except OSError as error:
        logger.error("Could not quarantine %s: %s", path, error)


def save_profiles(path: str, profiles: list[dict]) -> bool:
    """Write profiles atomically; deterministic key order. Returns success."""
    folder = os.path.dirname(path)
    try:
        if folder:
            os.makedirs(folder, exist_ok=True)
        temp_path = path + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as handle:
            json.dump(profiles, handle, indent=2, sort_keys=True, ensure_ascii=False)
        os.replace(temp_path, path)
        return True
    except OSError as error:
        logger.error("Could not save %s: %s", path, error)
        return False


def find_profile(profiles: list[dict], student_id: str) -> dict | None:
    """Return the profile with this student ID, or None."""
    for profile in profiles:
        if profile.get("student_id") == student_id:
            return profile
    return None


def filter_profiles(profiles: list[dict], key: str, value: str) -> list[dict]:
    """Return profiles whose field `key` equals `value` (case-insensitive)."""
    return [p for p in profiles if str(p.get(key, "")).lower() == value.lower()]


def upsert_profile(profiles: list[dict], profile: dict) -> list[dict]:
    """Return a new list with the profile added, replacing any same student ID."""
    others = [p for p in profiles if p.get("student_id") != profile["student_id"]]
    return others + [profile]