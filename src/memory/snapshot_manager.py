import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional

MEMORY_DIR = "memory"
os.makedirs(MEMORY_DIR, exist_ok=True)


# =====================================================
# NUMPY SAFE CONVERSION
# =====================================================
def _convert_numpy(obj):
    """
    Recursively convert numpy types to native Python types
    so JSON serialization never fails.
    """
    if isinstance(obj, dict):
        return {k: _convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_numpy(v) for v in obj]
    elif hasattr(obj, "item"):  # numpy types
        return obj.item()
    else:
        return obj


# =====================================================
# Utility: Generate Unique File ID
# =====================================================
def generate_file_id(file_name: str, df_hash: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_name = file_name.replace(" ", "_").replace(".csv", "")
    return f"{safe_name}_{timestamp}_{df_hash[:6]}"


def generate_dataframe_hash(df) -> str:
    content = df.to_csv(index=False).encode()
    return hashlib.md5(content).hexdigest()


def _get_snapshot_path(file_id: str) -> str:
    return os.path.join(MEMORY_DIR, f"{file_id}.json")


# =====================================================
# SAVE SNAPSHOT
# =====================================================
def save_snapshot(
    file_name: str,
    df,
    summary: Dict,
    issues: List[Dict]
) -> str:

    df_hash = generate_dataframe_hash(df)
    file_id = generate_file_id(file_name, df_hash)

    snapshot = {
        "file_id": file_id,
        "timestamp": datetime.utcnow().isoformat(),
        "summary": summary,
        "issues": issues
    }

    # 🔥 FIX: Convert numpy types before saving
    snapshot = _convert_numpy(snapshot)

    path = _get_snapshot_path(file_id)

    with open(path, "w") as f:
        json.dump(snapshot, f, indent=4)

    return file_id


# =====================================================
# LOAD SNAPSHOT
# =====================================================
def load_snapshot(file_id: str) -> Optional[Dict]:
    path = _get_snapshot_path(file_id)

    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        return json.load(f)


def list_snapshots() -> List[str]:
    files = [
        f.replace(".json", "")
        for f in os.listdir(MEMORY_DIR)
        if f.endswith(".json")
    ]
    files.sort()
    return files


# =====================================================
# COMPARISON ENGINE
# =====================================================
def compare_snapshots(previous: Dict, current: Dict) -> Dict:

    prev_summary = previous["summary"]
    curr_summary = current["summary"]

    delta = {
        "total_spend_change": curr_summary["total_spend"] - prev_summary["total_spend"],
        "financial_exposure_change": curr_summary["financial_exposure"] - prev_summary["financial_exposure"],
        "recoverable_savings_change": curr_summary["recoverable_savings"] - prev_summary["recoverable_savings"],
        "exposure_pct_change": curr_summary["exposure_pct"] - prev_summary["exposure_pct"],
    }

    # =====================================================
    # Root Cause Comparison
    # =====================================================
    prev_issues = {i["root_cause"]: i for i in previous["issues"]}
    curr_issues = {i["root_cause"]: i for i in current["issues"]}

    resolved = []
    new = []
    persisting = []
    root_cause_deltas = {}

    for root in prev_issues:
        if root not in curr_issues:
            resolved.append(root)

    for root in curr_issues:
        if root not in prev_issues:
            new.append(root)
        else:
            persisting.append(root)

            prev_exposure = prev_issues[root]["exposure"]
            curr_exposure = curr_issues[root]["exposure"]

            if prev_exposure != 0:
                pct_change = ((curr_exposure - prev_exposure) / prev_exposure) * 100
            else:
                pct_change = 0

            root_cause_deltas[root] = {
                "exposure_change": curr_exposure - prev_exposure,
                "pct_change": round(pct_change, 2)
            }

    return {
        "summary_delta": delta,
        "issues_resolved": resolved,
        "issues_new": new,
        "issues_persisting": persisting,
        "root_cause_delta": root_cause_deltas
    }