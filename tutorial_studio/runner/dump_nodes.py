import xml.etree.ElementTree as ET
import sys
sys.stdout.reconfigure(encoding='utf-8')

filename = sys.argv[1] if len(sys.argv) > 1 else "ui_dump.xml"
tree = ET.parse(filename)
for n in tree.iter("node"):
    b = n.attrib.get("bounds", "")
    t = n.attrib.get("text", "")
    d = n.attrib.get("content-desc", "")
    c = n.attrib.get("class", "")
    click = n.attrib.get("clickable", "")
    if t or d or click == "true":
        content = (d if d else t).replace("\n", " | ")
        print(f"clickable={click} bounds={b} text='{t}' desc='{content}' class={c}")
