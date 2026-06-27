import subprocess
import sys

def update_repo():
    print("Checking for updates...")
    try:
        # Check if it's a git repository
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True, text=True)

        # Perform git pull
        result = subprocess.run(["git", "pull", "origin", "main"], check=True, capture_output=True, text=True)

        if "Already up to date." in result.stdout:
            print("StartLoader is already up to date.")
        else:
            print("StartLoader has been updated successfully.")
            print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error during update: {e}")
        if e.stderr:
            # e.stderr is already str because text=True was used in the second call,
            # but the first call didn't use text=True. Let's fix the consistency.
            print(f"Details: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'git' command not found. Please install Git to use the update script.")
        sys.exit(1)

if __name__ == "__main__":
    update_repo()
