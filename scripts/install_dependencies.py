import subprocess
import sys
import os

def main():
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")

    if not os.path.exists(requirements_path):
        print("requirements.txt not found.")
        return

    print("🔧 Installing packages listed in requirements.txt...\n")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("\nAll packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install some packages.\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
