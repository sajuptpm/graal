import os
import re

log_path = os.path.join(os.environ['TEMP'], 'job_138689506087.log')
with open(log_path, 'r', encoding='utf-16', errors='ignore') as f:
    text = f.read()

pattern = re.compile(r"Testing library:\s*([^\r\n]+)(.*?)(?=Testing library:|\Z)", re.DOTALL)
matches = pattern.findall(text)

print(f"Total libraries tested: {len(matches)}")
reasons = {}

for coord, block in matches:
    coord = coord.strip()
    # find errors
    errs = []
    for line in block.splitlines():
        if "Error:" in line or "Caused by:" in line or "Fatal error:" in line:
            clean = line.split("UNKNOWN STEP")[-1].strip()
            # strip timestamp
            clean = re.sub(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z\s*", "", clean)
            errs.append(clean)
    reasons[coord] = errs[:3]

for coord, errs in list(reasons.items())[:15]:
    print(f"\n[{coord}]")
    for e in errs:
        print("  *", e)
