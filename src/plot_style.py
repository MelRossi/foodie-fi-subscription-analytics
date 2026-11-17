"""
Paleta y estilo de gráficos compartidos por todos los notebooks.

Uso en un notebook:
    import sys; sys.path.insert(0, str(PROJECT_ROOT / "src"))
    from plot_style import apply_style, PALETTE, PLAN_COLORS, OUTCOME_COLORS, SEQ_CMAP, PLAN_ES, path_es, pct, num, miles, PCT_AXIS
    apply_style()

Criterio de color (para que un mismo color signifique siempre lo mismo):
- Cada PLAN tiene un color fijo (PLAN_COLORS) en todos los gráficos.
- Mejora de plan = verde salvia, cancelación = coral, "sin cambios" = gris neutro.
- El verde azulado (teal) es el color de acento para gráficos que no distinguen planes.
"""
import matplotlib as mpl
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter

PALETTE = {
    "ink": "#1F2A37",      # texto principal
    "muted": "#5B6675",    # ejes y etiquetas secundarias
    "grid": "#E8ECF0",     # líneas de guía
    "mist": "#D9E0E6",     # gris neutro claro
    "slate": "#AEBBC6",    # gris azulado
    "teal": "#2A9D8F",     # acento
    "navy": "#264653",     # azul petróleo
    "gold": "#E9C46A",     # dorado
    "orange": "#F4A261",   # naranja
    "coral": "#E76F51",    # coral
    "sage": "#8AB17D",     # verde salvia
}

PLAN_COLORS = {
    "trial": PALETTE["slate"],
    "basic monthly": PALETTE["teal"],
    "pro monthly": PALETTE["navy"],
    "pro annual": PALETTE["gold"],
    "churn": PALETTE["coral"],
}

OUTCOME_COLORS = {
    "Mejoró de plan y sigue activo": PALETTE["sage"],
    "Mejoró de plan y luego canceló": PALETTE["orange"],
    "Sin cambios": PALETTE["mist"],
    "Canceló sin mejorar de plan": PALETTE["coral"],
}

# Nombres para MOSTRAR (los datos conservan los nombres originales en inglés)
PLAN_ES = {
    "trial": "Prueba gratuita", "basic monthly": "Básico mensual", "pro monthly": "Pro mensual",
    "pro annual": "Pro anual", "churn": "Cancelación",
}
_PATH_CORTO = {"trial": "Prueba", "basic monthly": "Básico", "pro monthly": "Pro mensual",
               "pro annual": "Pro anual", "churn": "Cancelación"}


def path_es(path: str) -> str:
    """'trial > basic monthly > churn' → 'Prueba → Básico → Cancelación'."""
    return " → ".join(_PATH_CORTO[p] for p in path.split(" > "))


# Formato numérico en español (coma decimal, punto de miles)
def pct(x, d=1):
    return f"{x * 100:.{d}f} %".replace(".", ",")


def num(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def miles(x):
    return f"{x:,.0f}".replace(",", ".")


PCT_AXIS = FuncFormatter(lambda v, _: f"{v * 100:.0f} %")

# Mapa secuencial (blanco azulado → teal → petróleo) para heatmaps
SEQ_CMAP = LinearSegmentedColormap.from_list("foodie_seq", ["#F3F7F8", "#9AD3CB", "#2A9D8F", "#264653"])


def apply_style() -> None:
    """Aplica el estilo global de matplotlib/seaborn."""
    sns.set_theme(style="white", context="notebook")
    mpl.rcParams.update({
        "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
        "axes.edgecolor": "#C9D1D9", "axes.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "axes.grid.axis": "y", "grid.color": PALETTE["grid"], "grid.linewidth": 0.8, "axes.axisbelow": True,
        "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.titlecolor": PALETTE["ink"], "axes.titlepad": 12,
        "axes.labelcolor": PALETTE["muted"], "axes.labelsize": 10,
        "xtick.color": PALETTE["muted"], "ytick.color": PALETTE["muted"],
        "text.color": PALETTE["ink"], "font.size": 10,
        "legend.frameon": False,
    })
