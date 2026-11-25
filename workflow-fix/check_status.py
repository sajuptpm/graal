import subprocess
import json

runs = {
    "reachability-metadata-dedicated-layer.yml": 45461118315,
    "reachability-metadata-layered.yml": 45523145309,
    "reachability-metadata-layered-future-defaults.yml": 45527017023,
    "reachability-metadata-future-defaults.yml": 45527086227
}

for name, rid in runs.items():
    raw = subprocess.check_output(['gh', 'run', 'view', str(rid), '--json', 'status,conclusion,jobs,name'])
    data = json.loads(raw)
    counts = {}
    for j in data.get('jobs', []):
        key = f"{j['status']}:{j['conclusion'] or 'pending'}"
        counts[key] = counts.get(key, 0) + 1
    print(f"\n[{name}] (Run {rid})")
    print(f"Overall Status: {data['status']} | Conclusion: {data['conclusion']}")
    print(f"Jobs Summary: {counts}")
