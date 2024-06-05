import shutil
import subprocess
from pathlib import Path


def install_command(json_path):
    outputs = subprocess.check_output("conda info --json", shell=True, text=True)
    with open(json_path, 'w') as f:
        f.write(outputs)
    script_src_path = Path(__file__).parent / "condaac.sh"
    script_tgt_path = Path.home() / ".local" / "bin" / "condaac.sh"
    shutil.copy2(script_src_path, script_tgt_path)
    return f"alias condaac=\"source {script_tgt_path}\""
