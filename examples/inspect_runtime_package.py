from pathlib import Path

print("PROTOCOLS")
for path in sorted(Path("protocols").glob("*.md")):
    print(f"- {path.name}")

print()
print("PERSONAS")
for path in sorted(Path("personas").glob("*.md")):
    print(f"- {path.stem}")
