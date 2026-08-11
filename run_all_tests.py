import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def copy_test_evidence(
    project_folder: Path,
    evidence_folder: Path,
):
    """Copy the HTML report and Playwright artifacts."""

    report_path = (
        project_folder / "report.html"
    )

    test_results_path = (
        project_folder / "test-results"
    )

    # Copy the HTML report.
    if report_path.exists():
        shutil.copy2(
            report_path,
            evidence_folder / "report.html",
        )

    # Copy screenshots, traces and videos.
    if test_results_path.exists():
        shutil.copytree(
            test_results_path,
            evidence_folder / "test-results",
        )


def main():
    """Run all tests and preserve execution evidence."""

    project_folder = Path(
        __file__
    ).resolve().parent

    # Create a unique folder for this execution.
    execution_time = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    evidence_folder = (
        project_folder
        / "evidence"
        / f"run_{execution_time}"
    )

    evidence_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    command = [
        sys.executable,
        "-m",
        "pytest",
        "tests",
        "--headed",
        "--slowmo",
        "250",
        "-v",
        "--color=no",
    ]

    header = (
        "=" * 60
        + "\nAUTOMATION EXERCISE TEST EXECUTION\n"
        + "=" * 60
        + "\nBrowser : Chromium"
        + "\nMode    : Headed"
        + "\nTests   : 3 test scenarios"
        + f"\nRun     : {execution_time}"
        + "\n"
        + "=" * 60
        + "\n"
    )

    print(header, end="")

    # Run pytest while displaying and saving its output.
    process = subprocess.Popen(
        command,
        cwd=project_folder,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    terminal_lines = [header]

    if process.stdout is not None:
        for line in process.stdout:
            print(line, end="")
            terminal_lines.append(line)

    return_code = process.wait()

    if return_code == 0:
        result_message = "RESULT: ALL TESTS PASSED"
    else:
        result_message = (
            "RESULT: ONE OR MORE TESTS FAILED"
        )

    footer = (
        "\n"
        + "=" * 60
        + f"\n{result_message}"
        + f"\nEVIDENCE: {evidence_folder}"
        + "\n"
        + "=" * 60
        + "\n"
    )

    print(footer, end="")

    terminal_lines.append(footer)

    # Save the complete terminal output.
    terminal_log = (
        evidence_folder
        / "terminal_output.txt"
    )

    terminal_log.write_text(
        "".join(terminal_lines),
        encoding="utf-8",
    )

    # Copy the report and Playwright evidence.
    copy_test_evidence(
        project_folder,
        evidence_folder,
    )

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())