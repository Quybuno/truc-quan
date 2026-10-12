"""Cắt vùng dashboard từ ảnh chụp Sky nguyên gốc; không thay nội dung UI."""
from datetime import datetime, timezone, timedelta
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'outputs/minh_hoa_chuong4/captures/dashboard_a400_kscatch_original.jpg'
TARGET = ROOT / 'latex/figures/chuong4/dashboard_a400_kscatch.png'
BOUNDS = (395, 235, 1258, 815)

image = Image.open(SOURCE)
assert image.size == (1346, 1025)
cropped = image.crop(BOUNDS)
TARGET.parent.mkdir(parents=True, exist_ok=True)
cropped.save(TARGET)
manifest = {
    'source': SOURCE.relative_to(ROOT).as_posix(),
    'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'image': TARGET.relative_to(ROOT).as_posix(),
    'image_sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest(),
    'capture_tool': 'computer-use @oai/sky.get_window_state',
    'browser': 'Microsoft Edge', 'url': 'http://127.0.0.1:8510',
    'captured_at': datetime.now(timezone(timedelta(hours=7))).isoformat(),
    'source_pixels': list(image.size), 'crop_bounds_xyxy': list(BOUNDS),
    'output_pixels': list(cropped.size), 'crop_only': True,
    'filters_visible': {'Steel_Type': ['A400'], 'Fault_Type_Clean': ['K_Scatch'],
                        'Steel_Plate_Thickness': [40, 300]},
    'kpi_visible': {'N': '390', 'Labels': '1', 'Median_Area': '6.281,5',
                    'Median_Thickness': '40,0'},
    'independent_kpi_check': 'outputs/buoc_6/test_results.json',
}
(ROOT / 'outputs/minh_hoa_chuong4/dashboard_capture.json').write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'output': str(TARGET), 'size': list(cropped.size), 'crop_only': True}, ensure_ascii=True))
