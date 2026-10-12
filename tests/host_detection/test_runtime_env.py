import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_cwd_dotenv_is_loaded_when_run_from_a_script_file(tmp_path):
    # A console script sets __main__.__file__, which makes a bare find_dotenv()
    # search upward from the installed package instead of the working directory.
    project = tmp_path / "project"
    project.mkdir()
    (project / ".env").write_text("OPENSPACE_TEST_CWD_DOTENV=loaded\n")
    script = tmp_path / "entry.py"
    script.write_text(
        "import os\n"
        "from openspace.host_detection.resolver import load_runtime_env\n"
        "load_runtime_env()\n"
        "print(os.environ.get('OPENSPACE_TEST_CWD_DOTENV', 'missing'))\n"
    )
    env = {k: v for k, v in os.environ.items() if k not in {"OPENSPACE_SKIP_DOTENV", "OPENSPACE_TEST_CWD_DOTENV"}}
    env["PYTHONPATH"] = str(REPO_ROOT)

    result = subprocess.run(
        [sys.executable, str(script)], cwd=project, env=env, capture_output=True, text=True, check=True
    )

    assert result.stdout.strip() == "loaded"
