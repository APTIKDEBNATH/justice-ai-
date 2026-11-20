with open("web/index.html", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find('id="landingView"')
end = text.find('id="authOverlay"')
landing_html = text[start:end]
lines = landing_html.split("\n")

print("--- LINES 25 TO 65 ---")
for idx in range(24, min(65, len(lines))):
    print(f"{idx+1}: {lines[idx]}")
