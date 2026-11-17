"""
Extrae las tablas `plans` y `subscriptions` de Foodie-Fi desde el script SQL
original (sentencias INSERT) y las guarda como CSV en data/raw/.

Principio: el CSV es una copia FIEL del origen. No se convierte ningún tipo
ni se corrige ningún valor; la limpieza ocurre en el notebook 01.

Uso:
    python scripts/extract_raw_data.py --source <ruta_local_o_URL> --out data/raw

Origen utilizado en este proyecto (8-Week SQL Challenge, Case Study #3 - Foodie-Fi):
    https://raw.githubusercontent.com/agneschintia/MySQL-Projects/myportfolio/
    8%20Week%20SQL%20Challenge/Foodie%20Fi/SQL%20Query.md
"""
import argparse
import csv
import re
import urllib.request
from pathlib import Path

DEFAULT_SOURCE = (
    "https://raw.githubusercontent.com/agneschintia/MySQL-Projects/myportfolio/"
    "8%20Week%20SQL%20Challenge/Foodie%20Fi/SQL%20Query.md"
)


def read_source(source: str) -> str:
    """Lee el SQL desde una URL o desde un archivo local."""
    if source.startswith("http"):
        with urllib.request.urlopen(source, timeout=60) as resp:
            return resp.read().decode("utf-8")
    return Path(source).read_text(encoding="utf-8")


def insert_block(text: str, table: str) -> str:
    """Devuelve el texto entre 'INSERT INTO <table> VALUES' y el ';' que cierra la sentencia."""
    marker = f"INSERT INTO {table} VALUES"
    start = text.index(marker) + len(marker)
    end = text.index(";", start)
    return text[start:end]


def parse_plans(block: str) -> list[tuple[str, str, str]]:
    # Formato: (0, "trial", 0), (1, "basic monthly", "9.90"), ..., (4, "churn", null)
    pattern = r'\(\s*(\d+)\s*,\s*"([^"]+)"\s*,\s*(?:"([^"]*)"|(\d+(?:\.\d+)?)|(null))\s*\)'
    rows = []
    for plan_id, name, quoted, number, _null in re.findall(pattern, block):
        price = quoted or number or ""  # null -> cadena vacía (se conserva como "sin precio")
        rows.append((plan_id, name, price))
    return rows


def parse_subscriptions(block: str) -> list[tuple[str, str, str]]:
    pattern = r"\(\s*'?(\d+)'?\s*,\s*'?(\d+)'?\s*,\s*'(\d{4}-\d{2}-\d{2})'\s*\)"
    return re.findall(pattern, block)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=DEFAULT_SOURCE)
    ap.add_argument("--out", default="data/raw")
    args = ap.parse_args()

    text = read_source(args.source)
    plans = parse_plans(insert_block(text, "plans"))
    sub_block = insert_block(text, "subscriptions")
    subs = parse_subscriptions(sub_block)

    # Chequeo independiente: cada línea de datos del bloque empieza con "(".
    # Si el regex perdió filas, estos dos conteos no coinciden.
    data_lines = sum(1 for ln in sub_block.splitlines() if ln.strip().startswith("("))
    assert len(subs) == data_lines, f"Filas parseadas ({len(subs)}) != líneas de datos ({data_lines})"
    assert len(plans) == 5, f"Se esperaban 5 planes, se obtuvieron {len(plans)}"

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "plans.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["plan_id", "plan_name", "price"])
        w.writerows(plans)
    with open(out / "subscriptions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["customer_id", "plan_id", "start_date"])
        w.writerows(subs)
    print(f"plans.csv: {len(plans)} filas | subscriptions.csv: {len(subs)} filas -> {out}")


if __name__ == "__main__":
    main()
