import re
with open('c:/Users/ertyui/ZCodeProject/nusa-sandbox/pc_portal_sandbox/portal_file_sandbox.html', 'r', encoding='utf-8') as f:
    text = f.read()

names = re.findall(r'class="order-name">([^<]+)', text)
specs = re.findall(r'class="file-spec">([^<]+)', text)
print("Orders found:", len(names))
for n, s in zip(names, specs):
    print(f"  - {n.strip()} | {s.strip()}")
