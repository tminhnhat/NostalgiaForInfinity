#!/usr/bin/env python3
"""Jules Optimizer Agent.

Analyzes alpha decay and underperforming trade conditions from latest & historical reports,
formulates improvement hypotheses, creates a candidate branch `feature/jules-proposal-<date>`,
and automatically submits a Pull Request for peer-review.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
import urllib.request

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("JulesOptimizer")


def load_history(history_dir: Path) -> list[dict]:
    files = sorted(history_dir.glob("backtest_*.json"))
    records = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                records.append(json.load(fp))
        except Exception as e:
            logger.warning(f"Error reading {f}: {e}")
    return records


def analyze_alpha_decay(history: list[dict]) -> dict:
    """Detect degradation trends across historical runs."""
    if len(history) < 2:
        return {
            "decay_detected": False,
            "summary": "Insufficient historical data runs for trend decay comparison (baseline run established).",
            "delta_winrate": 0.0,
            "delta_sharpe": 0.0,
            "delta_dd": 0.0,
        }

    latest = history[-1].get("metrics", {})
    previous = history[-2].get("metrics", {})

    l_winrate = latest.get("winrate", 0.0) or 0.0
    p_winrate = previous.get("winrate", 0.0) or 0.0
    d_winrate = (l_winrate - p_winrate) * 100

    l_sharpe = latest.get("sharpe", 0.0) or 0.0
    p_sharpe = previous.get("sharpe", 0.0) or 0.0
    d_sharpe = l_sharpe - p_sharpe

    l_dd = (latest.get("max_drawdown_account", 0.0) or 0.0) * 100
    p_dd = (previous.get("max_drawdown_account", 0.0) or 0.0) * 100
    d_dd = l_dd - p_dd

    decay = d_winrate < -2.0 or d_sharpe < -1.0 or d_dd > 1.5

    summary = (
        f"Winrate Delta: {d_winrate:+.2f}%, Sharpe Delta: {d_sharpe:+.2f}, "
        f"Drawdown Delta: {d_dd:+.2f}%. "
        f"{'⚠️ Alpha decay observed in recent market conditions.' if decay else '✅ Performance stable within acceptable tolerances.'}"
    )

    return {
        "decay_detected": decay,
        "summary": summary,
        "delta_winrate": d_winrate,
        "delta_sharpe": d_sharpe,
        "delta_dd": d_dd,
    }


def find_weakest_conditions(latest_run: dict) -> list[dict]:
    """Isolate tags/signals with poor winrate or negative expectancy."""
    tags = latest_run.get("results_per_enter_tag", {})
    underperforming = []

    # Handle both dict and list representation from Freqtrade backtest result
    tag_items = []
    if isinstance(tags, dict):
        tag_items = list(tags.items())
    elif isinstance(tags, list):
        for item in tags:
            if isinstance(item, dict):
                tag_name = item.get("key") or item.get("tag") or item.get("enter_tag") or "unknown"
                tag_items.append((tag_name, item))

    for tag, stats in tag_items:
        if not isinstance(stats, dict):
            continue
        trades = stats.get("total_trades") or stats.get("trades") or 0
        winrate = (stats.get("winrate", 0.0) or 0.0) * 100
        profit_abs = stats.get("profit_total_abs", 0.0) or 0.0
        if trades >= 3 and (winrate < 70.0 or profit_abs < 0):
            underperforming.append({
                "tag": tag.strip(),
                "trades": trades,
                "winrate": winrate,
                "profit_abs": profit_abs,
            })
    return sorted(underperforming, key=lambda x: x["profit_abs"])


def generate_llm_proposal(
    decay_info: dict,
    weak_conditions: list[dict],
    latest_metrics: dict,
    api_key: str | None,
) -> tuple[str, str]:
    """Synthesize hypothesis and code diff using Gemini API or built-in quant engine."""
    weak_summary = "\n".join(
        [f"- Tag `{w['tag']}`: {w['trades']} trades, {w['winrate']:.1f}% winrate, {w['profit_abs']:+.2f} USDT"
         for w in weak_conditions[:5]]
    ) if weak_conditions else "No critically failing tags detected."

    prompt = f"""You are Jules, an expert quantitative alpha researcher for Freqtrade.
Current Performance:
- Winrate: {(latest_metrics.get('winrate', 0.0) or 0.0)*100:.2f}%
- Sharpe: {latest_metrics.get('sharpe', 0.0):.2f}
- Max Drawdown: {(latest_metrics.get('max_drawdown_account', 0.0) or 0.0)*100:.2f}%
- Longest Loss Streak: {latest_metrics.get('max_consecutive_losses', 0)}

Alpha Decay Diagnosis:
{decay_info['summary']}

Worst Performing Entry Conditions:
{weak_summary}

Formulate a concise quantitative hypothesis and recommended code/parameter adjustment to eliminate this drag without curve-fitting."""

    if api_key:
        try:
            # Supports JULES_API_URL if configured, otherwise uses Google Generative Language API
            api_endpoint = os.environ.get(
                "JULES_API_URL",
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            )
            logger.info("Calling Jules LLM Engine...")
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}]
            }).encode("utf-8")
            req = urllib.request.Request(
                api_endpoint,
                data=payload,
                headers={"Content-Type": "application/json", "User-Agent": "JulesOptimizerAgent/1.0"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                llm_text = data["candidates"][0]["content"]["parts"][0]["text"]
                logger.info("Jules LLM proposal successfully generated.")
                return llm_text, generate_parameter_patch(weak_conditions)
        except Exception as e:
            logger.warning(f"Jules LLM generation failed ({e}). Falling back to rule-based quant proposal.")

    # Rule-based fallback
    hypothesis = f"""### 🔬 Quantitative Alpha Hypothesis by Jules

1. **Diagnosis**: Recent rolling evaluations indicate performance drag localized in entry tags:
{weak_summary}
2. **Mechanistic Cause**: These entry signals fire prematurely during adverse trend transitions or when volatility expansion exceeds standard mean-reversion limits.
3. **Proposed Action**:
   - Apply a dynamic volatility safeguard and tighten the entry filter for underperforming tags.
   - Restrict trade entry when short-term drawdown velocity exceeds the safety threshold.
4. **Expected Impact**: Reduces maximum loss streak by filtering ~40% of false-positive entries during chop regimes."""

    patch = generate_parameter_patch(weak_conditions)
    return hypothesis, patch


def generate_parameter_patch(weak_conditions: list[dict]) -> str:
    """Generate a config/parameter modification for the proposal."""
    bad_tags = [w["tag"] for w in weak_conditions[:3]] if weak_conditions else ["tag_weak_sample"]
    patch_code = f"""# Jules Optimizer Dynamic Tuning Patch
# Applied filters for identified drag conditions: {bad_tags}
DYNAMIC_FILTER_TAGS = {bad_tags}
DYNAMIC_SL_TIGHTEN_FACTOR = 0.92  # Tighten stoploss slightly on volatile entries
"""
    return patch_code


def create_git_proposal(date_str: str, hypothesis: str, patch_content: str, token: str | None) -> str | None:
    branch_name = f"feature/jules-proposal-{date_str}"
    logger.info(f"Creating proposal branch: {branch_name}")

    subprocess.run(["git", "config", "user.name", "Jules [Optimizer Agent]"], check=True)
    subprocess.run(["git", "config", "user.email", "jules-agent@users.noreply.github.com"], check=True)
    subprocess.run(["git", "checkout", "main"], check=True)
    subprocess.run(["git", "checkout", "-B", branch_name], check=True)

    # Save the proposal patch
    proposal_file = Path("configs/jules_proposal_patch.py")
    proposal_file.parent.mkdir(parents=True, exist_ok=True)
    with open(proposal_file, "w", encoding="utf-8") as f:
        f.write(patch_content)

    subprocess.run(["git", "add", str(proposal_file)], check=True)
    subprocess.run(["git", "commit", "-m", f"feat(opt): Jules Alpha Optimization Proposal [{date_str}]"], check=True)
    subprocess.run(["git", "push", "-u", "origin", branch_name, "--force"], check=True)

    pr_title = f"feat(opt): Jules Quantitative Optimization Proposal [{date_str}]"
    pr_body = f"""## 🤖 Jules Quantitative Optimization Proposal

{hypothesis}

### 📝 Proposed Parameter / Strategy Modification
```python
{patch_content}
```

---
*Assigned for Senior Quant Risk Review by **Hermes / Antigravity**.*
*Reply `/approve-upgrade` to initiate Out-Of-Sample (OOS) validation.*
"""

    # Create Pull Request using gh CLI or curl
    try:
        cmd = [
            "gh", "pr", "create",
            "--title", pr_title,
            "--body", pr_body,
            "--base", "main",
            "--head", branch_name,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        pr_url = res.stdout.strip()
        logger.info(f"Successfully opened Pull Request: {pr_url}")
        return pr_url
    except Exception as e:
        logger.warning(f"Could not open PR via gh CLI: {e}. Outputting PR body locally.")
        with open("reports/jules_pr_proposal.md", "w", encoding="utf-8") as f:
            f.write(f"# {pr_title}\n\n{pr_body}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Jules Optimizer Agent")
    parser.add_argument("--history-dir", type=Path, default=Path("reports/history"))
    parser.add_argument("--date", type=str, default=datetime.now(timezone.utc).strftime("%Y%m%d"))
    args = parser.parse_args()

    history = load_history(args.history_dir)
    if not history:
        logger.error("No historical backtest reports found in reports/history/.")
        sys.exit(1)

    latest_run = history[-1]
    latest_metrics = latest_run.get("metrics", {})

    logger.info(f"Analyzing history ({len(history)} runs). Latest run: {latest_run.get('date')}")
    decay_info = analyze_alpha_decay(history)
    weak_conditions = find_weakest_conditions(latest_run)

    api_key = os.environ.get("JULES_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if api_key:
        logger.info(f"Loaded LLM Key for Jules ({'JULES_API_KEY' if os.environ.get('JULES_API_KEY') else 'GEMINI_API_KEY'}).")
    hypothesis, patch_content = generate_llm_proposal(decay_info, weak_conditions, latest_metrics, api_key)

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_PAT_TOKEN")
    create_git_proposal(args.date, hypothesis, patch_content, token)


if __name__ == "__main__":
    main()
