import subprocess
import sys

if __name__ == "__main__":
    print("=" * 60)
    print("Cardiac Load Monitoring Dashboard")
    print("=" * 60)
    print("\nStarting dashboard...")
    print("Dashboard will be available at: http://127.0.0.1:8050/")
    print("\nPress Ctrl+C to stop\n")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\nDashboard stopped.")
