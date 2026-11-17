"""
Exporta todos los notebooks a HTML en docs/ (para publicarlos con GitHub Pages)
y regenera docs/index.html con el listado.

Uso (desde la raíz del repo, con el entorno instalado):
    python scripts/export_html.py

Importante: ejecutá antes los notebooks con 'Restart & Run All' para que el HTML refleje los resultados actuales.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NB_DIR, DOCS = ROOT / "notebooks", ROOT / "docs"
DOCS.mkdir(exist_ok=True)

notebooks = sorted(NB_DIR.glob("*.ipynb"))
for nb in notebooks:
    subprocess.run([sys.executable, "-m", "jupyter", "nbconvert", "--to", "html",
                    "--output-dir", str(DOCS), str(nb)], check=True)

TITULOS = {
    "01_data_loading_cleaning_validation": "01 · Carga, limpieza y validación de datos",
    "02_eda_funnel_and_behavior": "02 · Embudo de conversión y comportamiento",
    "03_cohorts_retention_churn": "03 · Cohortes, retención y cancelación",
    "04_customer_segmentation": "04 · Segmentación conductual de clientes",
    "05_insights_and_recommendations": "05 · Conclusiones y recomendaciones",
}
items = "\n".join(f'    <li><a href="{nb.stem}.html">{TITULOS.get(nb.stem, nb.stem)}</a></li>' for nb in notebooks)
(DOCS / "index.html").write_text(f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Foodie-Fi · Análisis de clientes de suscripción</title>
<style>body{{font-family:system-ui,sans-serif;max-width:760px;margin:3rem auto;padding:0 1rem;line-height:1.55;color:#222}}
a{{color:#1f6feb}}li{{margin:.35rem 0}}</style></head><body>
<h1>Foodie-Fi · Análisis de clientes de un servicio de suscripción</h1>
<p>Notebooks de análisis en Python (pandas, NumPy, matplotlib, seaborn). Dataset sintético con fines educativos.</p>
<ul>
{items}
</ul>
<p>Código y datos: ver el repositorio de GitHub.</p>
</body></html>
""", encoding="utf-8")
print(f"Exportados {len(notebooks)} notebooks a {DOCS.relative_to(ROOT)}/")
