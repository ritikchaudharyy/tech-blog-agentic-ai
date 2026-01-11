import os
import subprocess

print("🚀 Starting Tech Blog Agent Pipeline...\n")

steps = [
    ("HTML Renderer", "python renderer.py"),
    ("SEO Generator", "python seo_generator.py")
]

for name, command in steps:
    print(f"▶ Running {name}...")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ {name} failed. Stopping pipeline.")
        exit(1)
    print(f"✅ {name} completed.\n")

print("🎉 PIPELINE COMPLETE")
print("📦 Output ready in /output folder")
