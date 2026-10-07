import os
import shutil
import zipfile

# Map your exact files to their target SCORM zip names
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
    },  # Set to a CSS filename if you have one, or leave None
}

manifest_template = """<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="com.masterclass.scorm" version="1.0"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1 imscp_rootv1p1.xsd
                              http://www.adlnet.org/xsd/adlcp_rootv1p2 adlnet_rootv1p2.xsd">
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

  # Check and copy HTML file
  if os.path.exists(files["html"]):
    shutil.copy(files["html"], os.path.join(temp_dir, files["html"]))
  else:
    print(f"Warning: {files['html']} not found, skipping {zip_name}")
    shutil.rmtree(temp_dir)
    continue

  # Check and copy CSS file if specified and exists
  css_tag = ""
  if files["css"] and os.path.exists(files["css"]):
    shutil.copy(files["css"], os.path.join(temp_dir, files["css"]))
    css_tag = f'<file href="{files["css"]}"/>'

  # Generate the matching imsmanifest.xml
  manifest_content = manifest_template.format(
      html_file=files["html"], css_tag=css_tag
  )
  with open(os.path.join(temp_dir, "imsmanifest.xml"), "w") as f:
    f.write(manifest_content)

  # Zip everything up cleanly with the manifest at the root
  with zipfile.ZipFile(zip_name, "w") as zipf:
    for root, dirs, filenames in os.walk(temp_dir):
      for file in filenames:
        zipf.write(os.path.join(root, file), arcname=file)

  # Clean up temporary directory
  shutil.rmtree(temp_dir)
  print(f"Successfully created: {zip_name}")

print("\nAll SCORM packages generated successfully!")
