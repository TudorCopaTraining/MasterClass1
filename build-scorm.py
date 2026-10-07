import os
import shutil
import zipfile

print("Building single sequential SCORM package (New Order)...")

# Updated order: 1. Intelligent Automation, 2. AI Ethics, 3. EDI, 4. Risk Assessment
files_to_bundle = [
    {"html": "IntelligentAutomation.html", "css": None},
    {"html": "AIEthics.html", "css": "aiethics.css"},
    {"html": "EDIinAI.html", "css": "EDIinAI.css"},
    {"html": "AIRiskAssessment.html", "css": "AIRiskassessment.css"},
]

output_zip = "Masterclass_Complete_SCORM.zip"
temp_dir = "temp_masterclass_build"

if os.path.exists(temp_dir):
  shutil.rmtree(temp_dir)
os.makedirs(temp_dir)

manifest_template = """<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="com.masterclass.complete" version="1.0"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1 imscp_rootv1p1.xsd
                              http://www.adlnet.org/xsd/adlcp_rootv1p2 adlnet_rootv1p2.xsd">
  <organizations default="masterclass_org">
    <organization identifier="masterclass_org">
      <title>Complete AI Masterclass</title>
      <item identifier="item_1" identifierref="res_1">
        <title>1. Intelligent Automation</title>
      </item>
      <item identifier="item_2" identifierref="res_2">
        <title>2. AI Ethics</title>
      </item>
      <item identifier="item_3" identifierref="res_3">
        <title>3. EDI in AI</title>
      </item>
      <item identifier="item_4" identifierref="res_4">
        <title>4. AI Risk Assessment</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="res_1" type="webcontent" adlcp:scormtype="sco" href="IntelligentAutomation.html">
      <file href="IntelligentAutomation.html"/>
    </resource>
    <resource identifier="res_2" type="webcontent" adlcp:scormtype="sco" href="AIEthics.html">
      <file href="AIEthics.html"/>
      <file href="aiethics.css"/>
    </resource>
    <resource identifier="res_3" type="webcontent" adlcp:scormtype="sco" href="EDIinAI.html">
      <file href="EDIinAI.html"/>
      <file href="EDIinAI.css"/>
    </resource>
    <resource identifier="res_4" type="webcontent" adlcp:scormtype="sco" href="AIRiskAssessment.html">
      <file href="AIRiskAssessment.html"/>
      <file href="AIRiskassessment.css"/>
    </resource>
  </resources>
</manifest>
"""

# Copy files into temp dir
for item in files_to_bundle:
  html_file = item["html"]
  css_file = item["css"]

  if os.path.exists(html_file):
    shutil.copy(html_file, os.path.join(temp_dir, html_file))
    print(f"[OK] Added HTML: {html_file}")
  else:
    print(f"[WARNING] Missing HTML file: {html_file}")

  if css_file and os.path.exists(css_file):
    shutil.copy(css_file, os.path.join(temp_dir, css_file))
    print(f"[OK] Added CSS: {css_file}")

# Write manifest directly into temp dir root
with open(os.path.join(temp_dir, "imsmanifest.xml"), "w") as f:
  f.write(manifest_template)
print("[OK] Generated master imsmanifest.xml")

# Zip contents directly so no outer folder is included
with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
  for filename in os.listdir(temp_dir):
    file_path = os.path.join(temp_dir, filename)
    if os.path.isfile(file_path):
      zipf.write(file_path, arcname=filename)

shutil.rmtree(temp_dir)
print(f"\nSuccessfully created clean single package: {output_zip}")
