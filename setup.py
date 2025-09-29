#!/usr/bin/env python3
"""
Setup script for Factorio Twitch Chat Integration
This script helps users set up the bot by copying the example config and installing dependencies.
"""

import os
import sys
import subprocess
import shutil

def main():
    print("=== Factorio Twitch Chat Integration Setup ===\n")
    
    # Check if Config.py exists
    if not os.path.exists("Config.py"):
        if os.path.exists("Config.example.py"):
            print("Creating Config.py from Config.example.py...")
            shutil.copy2("Config.example.py", "Config.py")
            print("✅ Config.py created successfully!")
            print("⚠️  Please edit Config.py and fill in your Twitch and Factorio settings.")
        else:
            print("❌ Config.example.py not found!")
            return 1
    else:
        print("✅ Config.py already exists.")
    
    # Install dependencies
    print("\nInstalling Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return 1
    except FileNotFoundError:
        print("❌ requirements.txt not found!")
        return 1
    
    print("\n=== Setup Complete! ===")
    print("Next steps:")
    print("1. Edit Config.py and fill in your settings")
    print("2. Set up Factorio RCON (see README.md)")
    print("3. Run: python FactorioTwitchChatIntergration.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())