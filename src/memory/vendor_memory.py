import json
import os
from datetime import datetime
from typing import Dict, List, Optional

BASE_DIR = "memory"
os.makedirs(BASE_DIR, exist_ok=True)


# =====================================================
# INTERNAL HELPERS
# =====================================================

def _company_dir(company_id: str) -> str:
    """
    Creates and returns directory path for a company.
    """
    safe_company = company_id.replace(" ", "_").lower()
    path = os.path.join(BASE_DIR, safe_company)
    os.makedirs(path, exist_ok=True)
    return path


def _convert_numpy(obj):
    """
    Recursively converts numpy types to native Python types.
    Prevents JSON serialization errors.
    """
    if isinstance(obj, dict):
        return {k: _convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_numpy(v) for v in obj]
    elif hasattr(obj, "item"):  # numpy types (int64, float64, bool_)
        return obj.item()
    else:
        return obj


# =====================================================
# SNAPSHOT FUNCTIONS
# =====================================================

def save_snapshot(summary: Dict, company_id: str) -> None:
    """
    Saves snapshot with timestamp (does NOT overwrite).
    Automatically converts numpy values to JSON-safe types.
    """
    company_path = _company_dir(company_id)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(company_path, f"{timestamp}.json")

    # Convert numpy types before saving
    summary = _convert_numpy(summary)

    with open(file_path, "w") as f:
        json.dump(summary, f, indent=4)


def list_snapshots(company_id: str) -> List[str]:
    """
    Returns sorted list of snapshot filenames for a company.
    """
    company_path = _company_dir(company_id)
    files = [f for f in os.listdir(company_path) if f.endswith(".json")]
    return sorted(files)


def load_snapshot(company_id: str, filename: str) -> Optional[Dict]:
    """
    Loads specific snapshot file.
    """
    company_path = _company_dir(company_id)
    file_path = os.path.join(company_path, filename)

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r") as f:
        return json.load(f)


def load_previous_snapshot(company_id: str) -> Optional[Dict]:
    """
    Loads most recent snapshot (if exists).
    """
    snapshots = list_snapshots(company_id)

    if not snapshots:
        return None

    latest_file = snapshots[-1]
    return load_snapshot(company_id, latest_file)


# =====================================================
# COMPARISON LOGIC
# =====================================================

def compare_snapshots(current: Dict, previous: Dict) -> Dict:
    """
    Compares two financial summaries.
    """

    if not previous:
        return {}

    delta_exposure = (
        current.get("financial_exposure", 0)
        - previous.get("financial_exposure", 0)
    )

    delta_recoverable = (
        current.get("recoverable_savings", 0)
        - previous.get("recoverable_savings", 0)
    )

    delta_total_spend = (
        current.get("total_spend", 0)
        - previous.get("total_spend", 0)
    )

    if previous.get("financial_exposure", 0) != 0:
        delta_exposure_pct = (
            delta_exposure / previous["financial_exposure"]
        ) * 100
    else:
        delta_exposure_pct = 0

    return {
        "exposure_change": round(delta_exposure, 2),
        "recoverable_change": round(delta_recoverable, 2),
        "total_spend_change": round(delta_total_spend, 2),
        "exposure_pct_change": round(delta_exposure_pct, 2),
    }