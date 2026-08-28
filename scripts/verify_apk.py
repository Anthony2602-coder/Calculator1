import sys
from pathlib import Path

MIN = 100_000

def main():
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"NOT FOUND: {p}"); sys.exit(1)
    data = p.read_bytes()
    if len(data) < MIN:
        print(f"TOO SMALL ({len(data)} bytes) — not a valid APK"); sys.exit(1)
    if data[:2] != b"PK":
        print("NOT A ZIP/APK file"); sys.exit(1)
    print(f"Valid APK: {len(data)/1024/1024:.2f} MB")

if __name__ == "__main__":
    main()
