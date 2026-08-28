import re
from pathlib import Path

p = Path(__file__).parents[1] / "android" / "variables.gradle"
if p.exists():
    t = p.read_text()
    t = re.sub(r"minSdkVersion = \d+", "minSdkVersion = 22", t)
    t = re.sub(r"compileSdkVersion = \d+", "compileSdkVersion = 34", t)
    t = re.sub(r"targetSdkVersion = \d+", "targetSdkVersion = 34", t)
    p.write_text(t)
    print("Patched Android SDK versions")
