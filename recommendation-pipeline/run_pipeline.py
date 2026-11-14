from pathlib import Path
import json
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _rerun_with_base_python_if_venv_packages_are_blocked() -> None:
    if sys.prefix == sys.base_prefix:
        return

    import_check = "import numpy; import pandas"
    active_check = subprocess.run(
        [sys.executable, "-c", import_check],
        capture_output=True,
        text=True,
        check=False,
    )
    if active_check.returncode == 0:
        return

    base_python = getattr(sys, "_base_executable", None)
    if not base_python or not Path(base_python).is_file():
        return

    base_check = subprocess.run(
        [base_python, "-c", import_check],
        capture_output=True,
        text=True,
        check=False,
    )
    if base_check.returncode != 0:
        return

    print(
        "The active virtual environment cannot load NumPy/pandas. "
        "Retrying with its base Python interpreter.",
        file=sys.stderr,
    )
    result = subprocess.run(
        [base_python, str(Path(__file__).resolve()), *sys.argv[1:]],
        cwd=PROJECT_ROOT,
        check=False,
    )
    raise SystemExit(result.returncode)


_rerun_with_base_python_if_venv_packages_are_blocked()

from src.orchestration.pipeline import run_pipeline

if __name__ == '__main__':
    summary = run_pipeline()
    print("Recommendation pipeline completed successfully.")
    print(f"Validation status: {summary['validation_report']['status']}")
    print("Model metrics:")
    for model in summary['metrics']:
        print(
            f"  {model['model']}: "
            f"Precision@5={model['precision@k']:.4f}, "
            f"Recall@5={model['recall@k']:.4f}, "
            f"NDCG@5={model['ndcg@k']:.4f}, "
            f"Coverage={model['coverage']:.4f}, "
            f"Diversity={model['diversity']:.4f}"
        )
    print(f"Reports: {PROJECT_ROOT / 'reports'}")
