from pathlib import Path
import xml.etree.ElementTree as ET
import re

def parse_bounds(b_str):
    m = re.findall(r'\d+', b_str)
    if len(m) == 4:
        return [int(x) for x in m]
    return [0, 0, 0, 0]

xml_file = Path(__file__).resolve().parent.parent / "output" / "ui_dump.xml"
tree = ET.parse(str(xml_file))
root = tree.getroot()

for node in root.iter("node"):
    text = node.attrib.get("text", "")
    desc = node.attrib.get("content-desc", "")
    bounds = parse_bounds(node.attrib.get("bounds", ""))
    cx = (bounds[0] + bounds[2]) // 2
    cy = (bounds[1] + bounds[3]) // 2
    if text or desc:
        t = text if text else desc
        t_clean = t.encode('ascii', errors='ignore').decode()
        print(f"[{bounds[0]},{bounds[1]} - {bounds[2]},{bounds[3]}] Center: ({cx}, {cy}) -> {t_clean}")
