import os
import subprocess
import sys

def main():
    # Set PYTHONPATH to current directory
    os.environ["PYTHONPATH"] = os.getcwd()

    # Run streamlit
    cmd = ["streamlit", "run", "src/dashboard.py"]
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    except Exception as e:
        print(f"Error starting dashboard: {e}")

if __name__ == "__main__":
    main()
