"""Export the actual, saved PNG outputs of the seven fault-chart notebook cells."""
from pathlib import Path
import base64
import hashlib
import io
import json

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / 'buoc_1_2_3_4_5_6_loi_be_mat_thep.ipynb'
FIG = ROOT / 'latex/figures/chuong4'
OUT = ROOT / 'outputs/minh_hoa_chuong4'
FIG.mkdir(parents=True, exist_ok=True)
notebook_bytes = NOTEBOOK.read_bytes()
notebook = json.loads(notebook_bytes)
expected = [
    '01_co_cau_loi', '02_pareto_loi', '03_loi_theo_thep_so_luong',
    '04_loi_theo_thep_ty_trong', '05_scatter_do_sang',
    '06_boxplot_do_day', '07_boxplot_dien_tich_log',
]
manifest = []
for name in expected:
    candidates = [(i, cell) for i, cell in enumerate(notebook['cells'])
                  if cell['cell_type'] == 'code' and name in ''.join(cell['source'])
                  and any('image/png' in output.get('data', {}) for output in cell.get('outputs', []))]
    assert len(candidates) == 1, (name, [i+1 for i, _ in candidates])
    i, cell = candidates[0]
    headings = []
    for preceding in notebook['cells'][:i]:
        if preceding['cell_type'] == 'markdown':
            for line in ''.join(preceding['source']).splitlines():
                if line.startswith('## 5.'):
                    headings = [line.lstrip('# ').strip()]
                elif line.startswith('### Hình '):
                    headings = headings[:1] + [line.lstrip('# ').strip()]
    outputs = [output for output in cell['outputs'] if 'image/png' in output.get('data', {})]
    assert len(outputs) == 1, name
    encoded = outputs[0]['data']['image/png']
    if isinstance(encoded, list):
        encoded = ''.join(encoded)
    png = base64.b64decode(encoded, validate=True)
    image = Image.open(io.BytesIO(png))
    image.verify()
    path = FIG / f'notebook_{name}.png'
    path.write_bytes(png)
    assert path.read_bytes() == png
    manifest.append({
        'figure_name': name, 'chapter_figure_number': len(manifest)+1,
        'notebook': NOTEBOOK.name, 'notebook_cell_index_1_based': i+1,
        'cell_id': cell.get('id'), 'execution_count': cell.get('execution_count'),
        'notebook_section': headings[0], 'notebook_figure_heading': headings[-1],
        'latex_image': f'figures/chuong4/notebook_{name}.png',
        'format': 'image/png', 'pixel_size': list(Image.open(io.BytesIO(png)).size),
        'sha256': hashlib.sha256(png).hexdigest(),
        'exact_saved_notebook_output': True,
    })
assert NOTEBOOK.read_bytes() == notebook_bytes, 'The notebook must remain unchanged.'
report = {'notebook_sha256': hashlib.sha256(notebook_bytes).hexdigest(),
          'figure_count': len(manifest), 'figures': manifest}
(OUT / 'notebook_bieu_do.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=True, indent=2))
