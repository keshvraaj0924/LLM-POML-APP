#!/usr/bin/env python3
"""
Launcher script for POML vs RAW comparison tools
"""
import sys
import subprocess
import os

def main():
    print("🤖 POML vs RAW Comparison Tools")
    print("=" * 40)
    print("1. Command Line Interface (CLI)")
    print("2. Streamlit Web UI")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nChoose interface (1-3): ").strip()
            
            if choice == "1":
                print("\n🔄 Launching CLI...")
                subprocess.run([sys.executable, "main.py"])
                break
            elif choice == "2":
                print("\n🔄 Launching Streamlit UI...")
                print("📝 Note: This will open in your browser at http://localhost:8501")
                subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
                break
            elif choice == "3":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()
