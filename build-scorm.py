import os
import shutil
import zipfile

print(f"Current working directory: {os.getcwd()}")
print("Files found in this directory:", os.listdir("."))
print("-" * 40)

packages = {
    "AIEthics_SCORM.zip": {"html": "AIEthics.html", "css": "aiethics.css"},
    "AIRiskAssessment_SCORM.zip": {
        "html": "AIRiskAssessment.html",
        "css": "AIRiskassessment.css",
    },
    "EDIinAI_SCORM.zip": {"html": "EDIinAI.html", "css": "EDIinAI.css"},
    "IntelligentAutomation_SCORM.zip": {
        "html": "IntelligentAutomation.html",
        "css": None,
    },
}

manifest_template = """<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="com.masterclass.scorm" version="1.0"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1 imscp_rootv1p1.xsd
                              http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <organizations default="default_org">
    <organization identifier="default_org">
      <title>Masterclass SCORM Package</title>
      <item identifier="item_1" identifierref="resource_1">
        <title>Lesson</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="resource_1" type="webcontent" adlcp:scormtype="sco" href="{html_file}">
      <file href="{html_file}"/>
      {css_tag}
    </resource>
  </resources>
</manifest>
"""

for zip_name, files in packages.items():
  temp_dir = "temp_build"
  os.makedirs(temp_dir, exist_ok=True)

  # Check HTML
  html_file = files["html"]
  if not os.path.exists(html_file):
    print(f"[ERROR] HTML file missing: '{html_file}' -> Skipping {zip_name}")
    shutil.rmtree(temp_dir, ignore_errors=True)
    continue

  shutil.copy(html_file, os.path.join(temp_dir, html_file))
  print(f"[OK] Copied HTML: {html_file}")

  # Check CSS (optional)
  css_tag = ""
  css_file = files["css"]
  if css_file:
    if os.path.exists(css_file):
      shutil.copy(css_file, os.path.join(temp_dir, css_file))
      css_tag = f'<file href="{css_file}"/>'
      print(f"[OK] Copied CSS: {css_file}")
    else:
      print(f"[WARNING] CSS file '{css_file}' not found, proceeding without it.")

  # Generate manifest
  manifest_content = manifest_template.format(
      html_file=html_file, css_tag=css_tag
  )
  with open(os.path.join(temp_dir, "imsmanifest.xml"), "w") as f:
    f.write(manifest_content)

  # Zip archive
  with zipfile.ZipFile(zip_name, "w") as zipf:
    for root, dirs, filenames in os.walk(temp_dir):
      for file in filenames:
        zipf.write(os.path.join(root, file), arcname=file)

  shutil.rmtree(temp_dir, ignore_errors=True)
  print(f"--> Successfully created: {zip_name}\n")

print("Build script finished execution.")
