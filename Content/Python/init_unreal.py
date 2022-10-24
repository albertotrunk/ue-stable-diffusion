import unreal
import subprocess
import pkg_resources
from pathlib import Path

PYTHON_INTERPRETER_PATH = unreal.get_interpreter_executable_path()
assert Path(PYTHON_INTERPRETER_PATH).exists(), f"Python not found at '{PYTHON_INTERPRETER_PATH}'"

def pip_install(packages):
    # dont show window
    info = subprocess.STARTUPINFO()
    info.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    proc = subprocess.Popen(
        [
            PYTHON_INTERPRETER_PATH,
            '-m', 'pip', 'install',
            '--no-warn-script-location',
            *packages
        ],
        startupinfo = info,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        encoding = "utf-8"
    )

    while proc.poll() is None:
        unreal.log(proc.stdout.readline().strip())
        unreal.log_warning(proc.stderr.readline().strip())

    return proc.poll()

# Put here your required python packages
# remember C:\Program Files\Epic Games\UE_5.0\Engine\Plugins\Experimental\PythonFoundationPackages\Content\Python\Lib\Win64\site-packages
required = {'Pillow == 9.2.0','einops == 0.4.1', 'omegaconf == 2.2.3'}

installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if len(missing) > 0:
    pip_install(missing)
else:
    unreal.log("All python requirements already satisfied")
