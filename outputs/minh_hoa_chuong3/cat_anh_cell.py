"""Crop recorded VS Code screenshots without changing their cell content."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
CAPTURES = ROOT / 'outputs/minh_hoa_chuong3/captures'
FIGURES = ROOT / 'latex/figures/chuong3'
records = json.loads((CAPTURES / 'manifest.json').read_text(encoding='utf-8'))
assert len(records) == 6
for record in records:
    source = CAPTURES / record['name']
    rect = record['rectangle']
    box = (rect['left'], rect['top'], rect['left'] + rect['width'],
           rect['top'] + rect['height'])
    with Image.open(source) as image:
        assert 0 <= box[0] < box[2] <= image.width
        assert 0 <= box[1] < box[3] <= image.height
        cropped = image.crop(box)
        destination = FIGURES / record['name']
        cropped.save(destination)
        with Image.open(destination) as saved:
            assert saved.tobytes() == cropped.tobytes()
    record['source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    record['figure_sha256'] = hashlib.sha256(destination.read_bytes()).hexdigest()
    record['processing'] = 'Crop only; native VS Code cell content unchanged'
(CAPTURES / 'manifest.json').write_text(
    json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
print('Saved 6 crops of actual VS Code notebook cells.')
