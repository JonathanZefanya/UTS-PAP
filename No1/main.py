import os
import re

input_file = "company.puml"
output_dir = "generated_java"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

classes = re.findall(r"class\s+(\w+)\s*\{([^}]*)\}", content, re.MULTILINE | re.DOTALL)

for cls_name, body in classes:
    attrs, methods = [], []
    for line in body.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("'"):
            continue
        if "(" in line and ")" in line:
            name = re.sub(r"[+\-#]", "", line).strip()   # ← fixed here
            methods.append(name)
        elif ":" in line:
            name = re.sub(r"[+\-#]", "", line).strip()   # ← fixed here too
            attrs.append(name)

    lines = []
    lines.append(f"public class {cls_name} " + "{")
    lines.append("")
    for attr in attrs:
        parts = attr.split(":")
        if len(parts) == 2:
            var_name = parts[0].strip()
            var_type = parts[1].strip()
        else:
            var_name, var_type = parts[0].strip(), "String"
        lines.append(f"    private {var_type} {var_name};")
    lines.append("")

    for method in methods:
        m = re.match(r"(\w+)\s*\((.*?)\)\s*:?(\w+)?", method)
        if m:
            name, params, rtype = m.groups()
            rtype = rtype if rtype else "void"
            lines.append(f"    public {rtype} {name}({params}) " + "{")
            lines.append("        // TODO: implement")
            if rtype != "void":
                lines.append("        return null;")
            lines.append("    }")
            lines.append("")
    lines.append("}")
    java_code = "\n".join(lines)

    with open(os.path.join(output_dir, f"{cls_name}.java"), "w", encoding="utf-8") as out:
        out.write(java_code)

print(f"✅ Generated {len(classes)} Java classes in folder '{output_dir}'")
