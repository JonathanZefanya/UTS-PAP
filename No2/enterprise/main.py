import zipfile
import os
import re
import uuid
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET

# ====== CONFIG ======
INPUT_ZIP = "Apps.zip"
OUTPUT_VPP = "GeneratedProject.vpp"

# ====== PREP ======
temp = Path("temp_vpp")
if temp.exists():
    shutil.rmtree(temp)
(temp / "model" / "uml" / "classes").mkdir(parents=True)

# ====== PHP PARSER ======

class_re = re.compile(r"class\s+([A-Za-z_][A-Za-z0-9_]*)")
prop_re = re.compile(r"(public|private|protected|var)\s+\$([A-Za-z_][A-Za-z0-9_]*)")
method_re = re.compile(r"(public|private|protected)?\s*function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)")

classes = []

def parse_php(text):
    found = []
    for cls in class_re.finditer(text):
        name = cls.group(1)
        start = cls.end()
        end = len(text)

        body = text[start:end]

        # Properties
        props = [{"visibility": m.group(1), "name": m.group(2)}
                 for m in prop_re.finditer(body)]

        # Methods
        methods = [{"visibility": (m.group(1) or "public"), "name": m.group(2)}
                   for m in method_re.finditer(body)]

        found.append({
            "name": name,
            "properties": props,
            "methods": methods
        })
    return found


# ====== UNZIP SOURCE ======
extract_dir = Path("php_src")
if extract_dir.exists():
    shutil.rmtree(extract_dir)
extract_dir.mkdir()

with zipfile.ZipFile(INPUT_ZIP, 'r') as z:
    z.extractall(extract_dir)

for php in extract_dir.rglob("*.php"):
    txt = php.read_text(errors="ignore")
    parsed = parse_php(txt)
    classes.extend(parsed)


# ====== CREATE UML MODEL XML ======
def create_class_xml(cls):
    root = ET.Element("Class")
    root.set("id", str(uuid.uuid4()))
    root.set("name", cls["name"])

    # attributes
    for p in cls["properties"]:
        a = ET.SubElement(root, "Attribute")
        a.set("name", p["name"])
        a.set("visibility", p["visibility"])

    # operations
    for m in cls["methods"]:
        op = ET.SubElement(root, "Operation")
        op.set("name", m["name"])
        op.set("visibility", m["visibility"])

    return ET.ElementTree(root)


# generate class files
class_ids = {}
for cls in classes:
    cid = str(uuid.uuid4())
    class_ids[cls["name"]] = cid

    xml = create_class_xml(cls)
    xml.write(temp / f"model/uml/classes/{cid}.xml", encoding="utf-8")


# ====== CLASS DIAGRAM XML ======
diagram = ET.Element("Diagram")
diagram.set("type", "ClassDiagram")
diagram.set("id", str(uuid.uuid4()))

for cls in classes:
    node = ET.SubElement(diagram, "ClassNode")
    node.set("classId", class_ids[cls["name"]])

ET.ElementTree(diagram).write(temp / "model/uml/ClassDiagram.xml", encoding="utf-8")


# ====== PROJECT.XML ======
project = ET.Element("Project")
project.set("version", "1.0")
project.set("name", "GeneratedAppsProject")

ET.ElementTree(project).write(temp / "project.xml", encoding="utf-8")


# ====== PACKAGE INTO .VPP ======
with zipfile.ZipFile(OUTPUT_VPP, "w", zipfile.ZIP_DEFLATED) as vpp:
    for file in temp.rglob("*"):
        vpp.write(file, file.relative_to(temp))

print("VPP SUCCESSFULLY GENERATED:", OUTPUT_VPP)
