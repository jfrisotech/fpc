#!/usr/bin/env python3
"""
FPC Project Validator
Generates Flutter projects for all combinations and validates them.
Usage: python tests/test_project_validator.py [--quick] [--keep]
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
import datetime
from collections import defaultdict
from typing import List, Dict, Tuple

# Make sure we can import from the repo root
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)

from tests.validation_criteria import validate_project, ValidationError
from fpc.project_manager import _flutter_env

# ─────────────────────────────────────────────────────────────
# Test Matrix
# ─────────────────────────────────────────────────────────────

# Group 1 — Architecture × State (baseline: no DB, no BaaS, standard)
GROUP1 = [
    {"arch": a, "state": s, "http": "none", "db": "none", "baas": "none", "structure": "standard"}
    for a in ["mvc", "mvvm", "clean"]
    for s in ["provider", "bloc", "getx", "riverpod", "mobx", "none"]
]

# Group 2 — DB variations (arch=clean, state=bloc, http=dio)
GROUP2 = [
    {"arch": "clean", "state": "bloc", "http": "dio", "db": db, "baas": "none", "structure": "standard"}
    for db in ["sqlite", "hive", "isar", "objectbox"]
]

# Group 3 — Structure modular (arch=mvc + mvvm + clean, key states)
GROUP3 = [
    {"arch": a, "state": s, "http": "none", "db": "none", "baas": "none", "structure": "modular"}
    for a in ["mvc", "mvvm", "clean"]
    for s in ["bloc", "getx", "none"]
]

# Group 4 — BaaS variations
GROUP4 = [
    {"arch": "clean", "state": "bloc", "http": "dio", "db": "none", "baas": baas, "structure": "standard"}
    for baas in ["firebase", "supabase", "appwrite"]
]

# Group 5 — Critical combinations (high risk)
GROUP5 = [
    {"arch": "clean", "state": "mobx",     "http": "dio",  "db": "hive",      "baas": "firebase",  "structure": "modular"},
    {"arch": "clean", "state": "riverpod", "http": "dio",  "db": "isar",      "baas": "firebase",  "structure": "modular"},
    {"arch": "clean", "state": "mobx",     "http": "dio",  "db": "objectbox", "baas": "supabase",  "structure": "modular"},
    {"arch": "mvvm",  "state": "mobx",     "http": "http", "db": "isar",      "baas": "appwrite",  "structure": "standard"},
    {"arch": "mvc",   "state": "getx",     "http": "dio",  "db": "objectbox", "baas": "firebase",  "structure": "modular"},
]


def combo_name(c: Dict) -> str:
    """Generate a short deterministic project name from combo dict."""
    parts = [
        c["arch"],
        c["state"],
        c["http"] if c["http"] != "none" else "",
        c["db"] if c["db"] != "none" else "",
        c["baas"] if c["baas"] != "none" else "",
        c["structure"] if c["structure"] != "standard" else "",
    ]
    slug = "_".join(p for p in parts if p)
    # Flutter project names must be snake_case and start with a letter
    slug = slug.replace("-", "_")
    if not slug[0].isalpha():
        slug = "p_" + slug
    # Max length 30 to avoid FS issues
    return f"t_{slug}"[:30]


# ─────────────────────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────────────────────

class ProjectValidator:
    def __init__(self, base_dir: str, fpc_cmd: str, run_analyze: bool = True, keep: bool = False):
        self.base_dir = base_dir
        self.fpc_cmd = fpc_cmd
        self.run_analyze = run_analyze
        self.keep = keep
        self.results: List[Dict] = []
        # Build env with Flutter in PATH for all subprocesses
        self.flutter_env = _flutter_env()

    def _run(self, cmd: List[str], cwd: str = None, timeout: int = 600, env: dict = None) -> Tuple:
        try:
            result = subprocess.run(
                cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                env=env,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "TIMEOUT"
        except Exception as e:
            return -1, "", str(e)

    def validate_combo(self, combo: Dict, group: str) -> Dict:
        name = combo_name(combo)
        project_path = os.path.join(self.base_dir, name)
        print(f"\n{'='*60}")
        print(f"[{group}] Testing: {name}")
        print(f"  arch={combo['arch']} state={combo['state']} http={combo['http']}")
        print(f"  db={combo['db']} baas={combo['baas']} structure={combo['structure']}")
        print('='*60)

        # Clean up if exists
        if os.path.exists(project_path):
            shutil.rmtree(project_path)

        result_entry = {
            "name": name,
            "group": group,
            "combo": combo,
            "create_ok": False,
            "analyze_ok": None,
            "analyze_output": "",
            "validation_errors": [],
            "error_counts": {"CRITICAL": 0, "ERROR": 0, "WARNING": 0},
        }

        # Step 1: Generate project
        cmd = [
            self.fpc_cmd, "create",
            "-n", name,
            "-p", self.base_dir,
            "--arch", combo["arch"],
            "--state", combo["state"],
            "--http", combo["http"],
            "--db", combo["db"],
            "--baas", combo["baas"],
            "--structure", combo["structure"],
        ]
        print(f"  → Running: {' '.join(cmd)}")
        rc, stdout, stderr = self._run(cmd, timeout=600, env=self.flutter_env)

        if rc != 0:
            msg = f"fpc create FAILED (exit {rc}): {stderr[-500:]}"
            print(f"  ✗ {msg}")
            result_entry["validation_errors"].append({
                "severity": "CRITICAL", "category": "GENERATION",
                "message": msg, "file": ""
            })
            result_entry["error_counts"]["CRITICAL"] += 1
            self.results.append(result_entry)
            return result_entry

        if not os.path.isdir(project_path):
            msg = f"Project directory not created: {project_path}"
            print(f"  ✗ {msg}")
            result_entry["validation_errors"].append({
                "severity": "CRITICAL", "category": "GENERATION",
                "message": msg, "file": ""
            })
            result_entry["error_counts"]["CRITICAL"] += 1
            self.results.append(result_entry)
            return result_entry

        result_entry["create_ok"] = True
        print(f"  ✓ Project created")

        # Step 2: flutter analyze
        if self.run_analyze:
            print(f"  → Running flutter analyze...")
            rc2, out2, err2 = self._run(["flutter", "analyze"], cwd=project_path, timeout=300, env=self.flutter_env)
            analyze_output = out2 + err2
            result_entry["analyze_ok"] = (rc2 == 0)
            result_entry["analyze_output"] = analyze_output[-3000:]  # last 3000 chars

            if rc2 == 0:
                print(f"  ✓ flutter analyze passed")
            else:
                print(f"  ✗ flutter analyze FAILED")
                # Extract errors from analyze output
                for line in analyze_output.splitlines():
                    if " error • " in line or " warning • " in line:
                        sev = "ERROR" if " error • " in line else "WARNING"
                        result_entry["validation_errors"].append({
                            "severity": sev,
                            "category": "DART_ANALYZE",
                            "message": line.strip(),
                            "file": ""
                        })
                        result_entry["error_counts"][sev] += 1

        # Step 3: Structural validation
        validation_errors: List[ValidationError] = validate_project(
            project_path, name,
            combo["arch"], combo["state"], combo["structure"],
            combo["http"], combo["db"], combo["baas"]
        )

        for ve in validation_errors:
            result_entry["validation_errors"].append(ve.to_dict())
            result_entry["error_counts"][ve.severity] = result_entry["error_counts"].get(ve.severity, 0) + 1

        critical_count = result_entry["error_counts"].get("CRITICAL", 0)
        error_count = result_entry["error_counts"].get("ERROR", 0)
        warning_count = result_entry["error_counts"].get("WARNING", 0)
        print(f"  → Validation: CRITICAL={critical_count} ERROR={error_count} WARNING={warning_count}")

        # Cleanup
        if not self.keep:
            shutil.rmtree(project_path, ignore_errors=True)
            print(f"  → Project cleaned up")

        self.results.append(result_entry)
        return result_entry

    def run_all(self, groups: List[Tuple[str, List[Dict]]]):
        for group_name, combos in groups:
            for combo in combos:
                self.validate_combo(combo, group_name)

    def generate_report(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON detail
        json_path = os.path.join(output_dir, f"errors_detail_{timestamp}.json")
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        # Markdown summary
        md_path = os.path.join(output_dir, f"summary_{timestamp}.md")
        passed = [r for r in self.results if r["error_counts"].get("CRITICAL", 0) == 0 and r["error_counts"].get("ERROR", 0) == 0]
        failed = [r for r in self.results if r not in passed]

        lines = [
            "# FPC Validation Report",
            f"Generated: {datetime.datetime.now().isoformat()}",
            "",
            f"## Summary: {len(passed)}/{len(self.results)} passed",
            "",
            "## Results",
            "",
            "| Combo | Group | CRITICAL | ERROR | WARNING | Analyze | Status |",
            "|-------|-------|----------|-------|---------|---------|--------|",
        ]
        for r in self.results:
            status = "✅" if r in passed else "❌"
            analyze = "✅" if r.get("analyze_ok") else ("❌" if r.get("analyze_ok") is False else "—")
            lines.append(
                f"| {r['name']} | {r['group']} | "
                f"{r['error_counts'].get('CRITICAL',0)} | "
                f"{r['error_counts'].get('ERROR',0)} | "
                f"{r['error_counts'].get('WARNING',0)} | "
                f"{analyze} | {status} |"
            )

        lines += ["", "## Failed Combinations — Error Details", ""]
        for r in failed:
            lines.append(f"### ❌ `{r['name']}`")
            lines.append(f"Combo: `{r['combo']}`\n")
            for e in r["validation_errors"]:
                lines.append(f"- **[{e['severity']}][{e['category']}]** {e['message']}")
                if e.get("file"):
                    lines.append(f"  - File: `{e['file']}`")
            lines.append("")

        with open(md_path, 'w') as f:
            f.write('\n'.join(lines))

        print(f"\n{'='*60}")
        print(f"REPORT SAVED:")
        print(f"  JSON: {json_path}")
        print(f"  MD:   {md_path}")
        print(f"SUMMARY: {len(passed)}/{len(self.results)} combos passed")
        print('='*60)
        return json_path, md_path


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="FPC Project Validator")
    parser.add_argument("--quick", action="store_true", help="Only run Group 1 (arch×state, no DB/BaaS)")
    parser.add_argument("--keep",  action="store_true", help="Keep generated projects (don't delete)")
    parser.add_argument("--no-analyze", action="store_true", help="Skip flutter analyze")
    parser.add_argument("--out", default="/tmp/fpc_validation_report", help="Output directory for reports")
    parser.add_argument("--base", default="/tmp/fpc_validation", help="Base directory for generated projects")
    args = parser.parse_args()

    os.makedirs(args.base, exist_ok=True)

    # Find fpc command
    fpc_cmd = shutil.which("fpc")
    if not fpc_cmd:
        # Try running from repo
        fpc_cmd = os.path.join(repo_root, "fpc_cli")
        if not os.path.isfile(fpc_cmd):
            print("ERROR: Cannot find 'fpc' command. Install fpc or check PATH.")
            sys.exit(1)

    print(f"Using fpc: {fpc_cmd}")
    print(f"Output base: {args.base}")
    print(f"Reports: {args.out}")

    validator = ProjectValidator(
        base_dir=args.base,
        fpc_cmd=fpc_cmd,
        run_analyze=not args.no_analyze,
        keep=args.keep,
    )

    groups = [("G1-arch-x-state", GROUP1)]
    if not args.quick:
        groups += [
            ("G2-db-variations", GROUP2),
            ("G3-modular-structure", GROUP3),
            ("G4-baas-variations", GROUP4),
            ("G5-critical", GROUP5),
        ]

    validator.run_all(groups)
    validator.generate_report(args.out)


if __name__ == "__main__":
    main()
