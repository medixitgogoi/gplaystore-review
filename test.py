# =====================================================
# GEMINI 2.5 CSV ANALYSIS
# =====================================================

import google.generativeai as genai
from datetime import datetime
import os
import time

# 1. CONFIGURE API
API_KEY = "AIzaSyDUT6c5iS7n4xlQPCwH6qqnttSlPr3Do94"  # Replace with your actual key
genai.configure(api_key=API_KEY)

# 2. UPLOAD CSV FILE DIRECTLY
csv_file_path = "pain_points.csv" 

# Check if file exists
if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"❌ File not found: {csv_file_path}")

print(f"🚀 Uploading {csv_file_path} ({os.path.getsize(csv_file_path)/1000:.1f}KB)...")

uploaded_file = genai.upload_file(
    path=csv_file_path,
    mime_type="text/csv",
    display_name="App Reviews Data"
)

print(f"📁 File URI: {uploaded_file.uri}")

# --- CRITICAL STEP: WAIT FOR PROCESSING ---
print("⏳ Waiting for file processing...")
while uploaded_file.state.name == "PROCESSING":
    print(".", end="", flush=True)
    time.sleep(2)
    uploaded_file = genai.get_file(uploaded_file.name)

if uploaded_file.state.name != "ACTIVE":
    raise Exception(f"❌ Upload failed: {uploaded_file.state.name}")

print(f"\n✅ File Ready: {uploaded_file.name}")

# 3. SELECT MODEL
# Based on your list, 'gemini-2.5-pro' is the best choice for deep analysis.
# If you want speed, change this to 'gemini-2.5-flash'.
model_name = 'gemini-2.5-pro' 
print(f"🤖 Using Model: {model_name}")

model = genai.GenerativeModel(model_name)

# 4. ANALYZE CSV FILE
print("🧠 Analyzing data...")

prompt = """
This is a CSV file containing raw app reviews.

**ANALYZE THE DATA AND GENERATE A REPORT:**

1. **Top 10 Pain Points:** Extract specific issues with quote examples and frequency counts.
2. **Categorization:** Group issues into Monetization, Bugs, UI/UX, Support, Deceptive Practices.
3. **Sentiment Split:** Calculate estimated % of Negative, Positive, and Mixed reviews.
4. **Priority Matrix:** Identify "Quick Wins" (low effort, high impact) vs "Strategic Fixes" (high effort, high impact).
5. **30/60/90 Day Plan:** A concrete roadmap to improve the app rating.

Format the output as a professional Markdown report.
"""

# Increased timeout to 600s because 2.5-Pro can take time to think deeply
response = model.generate_content(
    [uploaded_file, prompt],
    request_options={"timeout": 600} 
)

# 5. SAVE REPORT
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_file = f'analysis_{timestamp}.md'

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(f"# Analysis Report\n\n")
    f.write(f"**Model:** {model_name}\n")
    f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("---\n\n")
    f.write(response.text)

print(f"\n✅ DONE! Report saved to: {report_file}")