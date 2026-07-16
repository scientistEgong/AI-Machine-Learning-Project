# debug_paths.py
import os
import sys
from pathlib import Path

print("=" * 60)
print("🔍 STREAMLIT PATH DIAGNOSTIC SYSTEM")
print("=" * 60)

# 1. Current Working Directory (Where terminal is running from)
cwd = Path.cwd()
print(f"Current Working Directory (CWD): {cwd}")

# 2. File Location
file_loc = Path(__file__).resolve()
print(f"This script's absolute path:    {file_loc}")
print(f"Parent directory (Project Root): {file_loc.parent}")

# 3. Python System Path
print("\n🐍 Python sys.path (Search locations for imports):")
for path in sys.path[:5]:  # Print first 5 search paths
    print(f"  - {path}")

# 4. Try importing config
print("\n⚙️ Testing configuration imports...")
try:
    import config
    print("✅ Successfully imported config.py!")
    print(f"   BASE_DIR resolved to: {config.BASE_DIR}")
    print(f"   REPORTS_DIR exists:   {config.REPORTS_DIR.exists()} ({config.REPORTS_DIR})")
    print(f"   CLASS_NAMES_FILE:     {config.CLASS_NAMES_FILE.exists()} ({config.CLASS_NAMES_FILE})")
    print(f"   DISEASE_INFO_FILE:    {config.DISEASE_INFO_FILE.exists()} ({config.DISEASE_INFO_FILE})")
except Exception as e:
    print(f"❌ Failed to load config or resolve paths: {e}")

print("=" * 60)