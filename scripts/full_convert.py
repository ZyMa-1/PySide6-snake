import pathlib
import subprocess as sp

PROJECT_ROOT = pathlib.Path(__file__).absolute().parent.parent


def convert_ui(input_path: pathlib.Path, output_path: pathlib.Path):
    params = ["--no-autoconnection"]
    full_command = f"pyside6-uic {' '.join(params)} {str(input_path)} --output {str(output_path)}"
    exit_code = sp.call(full_command, stdout=sp.PIPE)
    if exit_code == 0:
        print("\033[1;32;40m" + "pyside6-uic success \033[0;37;40m")
    else:
        print("\033[1;31;40m" + "pyside6-uic error \033[0;37;40m")


if __name__ == "__main__":
    ################## UI ######################################

    input_path_1 = PROJECT_ROOT / "designer" / "MainWindow.ui"
    output_path_1 = PROJECT_ROOT / "src" / "ui" / "Ui_MainWindow.py"

    convert_ui(input_path_1, output_path_1)
