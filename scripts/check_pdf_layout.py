"""Reject intersecting text from separate PDF lines (Poppler bbox-layout XML)."""
import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()
ns = {"p": "http://www.w3.org/1999/xhtml"}
pages = root.findall(".//p:page", ns)
errors = []
for number, page in enumerate(pages, 1):
    words = []
    for line_number, line in enumerate(page.findall(".//p:line", ns)):
        for word in line.findall("p:word", ns):
            box = tuple(float(word.attrib[key]) for key in ("xMin", "yMin", "xMax", "yMax"))
            words.append((line_number, "".join(word.itertext()), box))
    for i, (line_a, text_a, a) in enumerate(words):
        for line_b, text_b, b in words[i + 1:]:
            if line_a == line_b:
                continue
            dx = min(a[2], b[2]) - max(a[0], b[0])
            dy = min(a[3], b[3]) - max(a[1], b[1])
            # Font boxes include unused ascender/descender space, so adjacent
            # lines can intersect slightly even when their visible glyphs do not.
            height = min(a[3] - a[1], b[3] - b[1])
            if dx > 1 and dy > 0.35 * height:
                errors.append(f"Page {number}: {text_a!r} intersects {text_b!r} ({dx:.1f} x {dy:.1f} pt)")
print(f"PDF layout: {len(pages)} page(s); {len(errors)} text intersections.")
for error in errors[:20]:
    print(error)
if not pages or errors:
    sys.exit(1)
