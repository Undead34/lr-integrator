import subprocess

def main():
    # Comando de PyInstaller
    subprocess.run([
        "pyinstaller",
        "--name", "lr-integrator",
        "--distpath", "build/dist",
        "--workpath", "build/tmp",
        "--specpath", "build/spec",
        "__main__.py"
    ])
