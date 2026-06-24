import re
import subprocess
from pathlib import Path

bench = Path("BONUS-llama-cpp-optimization/llama.cpp/build/bin/llama-bench.exe")
model = "models/qwen2.5-1.5b-instruct-q4_k_m.gguf"

cmd = [
    str(bench), "-m", model,
    "-t", "1",
    "-ngl", "99",
    "-p", "0", "-n", "64",
    "-r", "2",
]

result = subprocess.run(cmd, capture_output=True, text=True)
stdout = result.stdout

print("Stdout type:", type(stdout))
for line in stdout.splitlines():
    if "tg64" in line:
        print("Line:", repr(line))
        for char in line:
            print(f"char: {repr(char)} code: {ord(char)}")

# Let's try matching with a simpler regex that doesn't use the ± character
TG_RE_simple = re.compile(r"\|\s*tg64\s*\|\s*([0-9.]+)")
m = TG_RE_simple.search(stdout)
print("Simple match:", m)
if m:
    print("Simple group 1:", m.group(1))

# Let's try matching with a regex that handles any character or whitespace before ±
TG_RE_any = re.compile(r"\|\s*tg64\s*\|\s*([0-9.]+)\s*.")
m = TG_RE_any.search(stdout)
print("Any match:", m)
if m:
    print("Any group 1:", m.group(1))
