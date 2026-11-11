# Foodie-Fi · Análisis de clientes de un servicio de suscripción

Proyecto de Data Analytics en **Python** (pandas, NumPy, matplotlib/seaborn, Jupyter) sobre el ciclo de vida de clientes de un servicio
de streaming por suscripción: **conversión, cohortes, retención/churn y segmentación**, con foco en recomendaciones de negocio.

> **Estado:** en desarrollo · Etapa 1 de 5 completada. Este README se ampliará con hallazgos y recomendaciones cuando existan los análisis.

## Preguntas de negocio
1. ¿Qué proporción de las pruebas gratuitas (trial) se convierte en clientes de pago, y a qué plan?
2. ¿Cómo evoluciona la retención de cada cohorte mensual de clientes?
3. ¿Cuándo y desde qué plan cancelan los clientes?
4. ¿Qué recorridos de plan (trial → … → churn) son los más frecuentes y cuáles se asocian con más cancelaciones?
5. ¿Qué segmentos conductuales de clientes existen y cuánto valen?
6. ¿Qué acciones concretas podrían mejorar conversión y retención?

## Hoja de ruta

| 1. Carga, limpieza y validación 
| 2. EDA: embudo y comportamiento 
| 3. Cohortes, retención y churn 
| 4. Segmentación de clientes 
| 5. Insights y recomendaciones

## Estructura del repositorio

```
foodie-fi-subscription-analytics/
├── README.md
├── requirements.txt
├── data/
│   ├── README.md                 # procedencia y diccionario de datos
│   ├── raw/                      # originales (solo lectura): plans.csv, subscriptions.csv
│   └── processed/                # datasets limpios generados por el notebook 01
├── notebooks/                    # un notebook por etapa, numerados
├── reports/
│   └── figures/                  # gráficos exportados (PNG)
└── scripts/
    └── extract_raw_data.py       # reconstruye data/raw/ desde el SQL original
```

El notebook 01 corre de punta a punta y regenera `data/processed/` y las figuras. Probado con pandas 2.2.3 y 3.0.6 (resultados idénticos).

## Datos y limitaciones

- **Dataset sintético** (*8-Week SQL Challenge, Case Study #3*): no representa un negocio real, por lo que las conclusiones no son generalizables.
- **Sin atributos demográficos ni de canal:** la segmentación es **conductual** (recorrido de planes y tiempos).
- **Ingresos estimados** a partir de precios de lista (moneda no especificada en la fuente), no de pagos reales.
- **Censura desigual:** los trials comienzan durante 2020 y la observación llega hasta el 30-abr-2021; cada cohorte tiene una ventana de seguimiento distinta.
- Detalles y decisiones de limpieza: ver notebook 01 y [`data/README.md`](data/README.md).

## Calidad de los datos (resultado de la etapa 1)

- 2.650 eventos de 1.000 clientes; sin nulos reales, duplicados ni claves huérfanas; fechas validadas.
- 8 reglas de negocio críticas verificadas (trial de 7 días, churn terminal, sin downgrades, etc.): **0 violaciones**.
- Cifras del caso de estudio publicado reproducidas exactamente (eventos desde 2021 por plan: 8 / 60 / 63 / 71).
- **Dos advertencias documentadas** que condicionan la interpretación de la retención:
  - **A1:** 19 de 25 planes anuales ya vencidos al corte no registran ningún evento posterior (renovación implícita o churn no registrado); se tratan como activos y quedan marcados.
  - **A2:** ningún evento ocurre pasados 184 días del inicio de un plan mensual, y 308 de 441 clientes activos en plan mensual superan ese plazo sin evento. La retención de largo plazo en planes mensuales **no es informativa**.

## Stack
Python · pandas · NumPy · matplotlib · seaborn · Jupyter
