# Datos

## Procedencia

| | |
|---|---|
| **Dataset** | Foodie-Fi — *8-Week SQL Challenge, Case Study #3* |
| **Naturaleza** | **Sintético** (creado para un ejercicio educativo de SQL; no son clientes reales) |
| **Obtención** | Las tablas existen como sentencias `INSERT` SQL. `scripts/extract_raw_data.py` las extrae a CSV **sin modificar ningún valor**. |
| **Fuente usada** | Copia pública del script SQL en GitHub (URL por defecto en el script) |


## `raw/` — datos originales (solo lectura)

El notebook 01 calcula el hash SHA-256 de estos archivos al inicio y al final para demostrar que no se alteran.

**`plans.csv`** — catálogo de planes (5 filas)

| Columna | Descripción |
|---|---|
| `plan_id` | Identificador del plan (0–4) |
| `plan_name` | `trial`, `basic monthly`, `pro monthly`, `pro annual`, `churn` |
| `price` | Precio de lista (moneda **no especificada** en la fuente). Vacío en `churn`. |

**`subscriptions.csv`** — eventos de suscripción (2.650 filas)

| Columna | Descripción |
|---|---|
| `customer_id` | Cliente (1–1000) |
| `plan_id` | Plan que **comienza** en esa fecha |
| `start_date` | Fecha de inicio del plan (`YYYY-MM-DD`) |

## `processed/` — datos limpios (generados por el notebook 01)

### `foodie_fi_events_clean.csv` — una fila por evento (2.650 filas)

| Columna | Descripción |
|---|---|
| `customer_id`, `plan_id`, `plan_name`, `start_date` | Del original, con tipos correctos |
| `price` | Precio de lista; `0.0` para *trial* y *churn* |
| `is_paid_plan` | `True` si el plan tiene precio > 0 |
| `event_seq` | Orden del evento dentro del cliente (1 = trial) |
| `next_start_date` | Fecha del evento siguiente del mismo cliente (vacío si es el último) |
| `days_in_plan` | Días hasta el evento siguiente; si es el último, hasta el corte. Vacío en *churn* |
| `duration_is_censored` | `True` si `days_in_plan` se cortó en la fecha de observación (plan vigente) |
| `prev_plan_id`, `prev_plan_name` | Plan inmediatamente anterior |
| `is_first_event`, `is_last_event` | Posición dentro de la historia del cliente |
| `is_churn_event` | El evento es una cancelación |
| `is_conversion` | Paso de *trial* a un plan pago |
| `is_upgrade` | Cambio a un plan de mayor nivel (basic → pro monthly/annual, pro monthly → annual) |

### `foodie_fi_customers_clean.csv` — una fila por cliente (1.000 filas)

| Columna | Descripción |
|---|---|
| `customer_id` | Cliente |
| `trial_start_date`, `cohort_month` | Inicio del trial y cohorte (`YYYY-MM`) |
| `converted_to_paid` | Pasó a algún plan pago |
| `first_paid_plan`, `first_paid_date` | Primer plan pago y su fecha (vacío si nunca pagó) |
| `days_trial_to_paid` | Días entre inicio del trial y primer plan pago |
| `last_paid_plan` | Último plan pago contratado |
| `current_plan` | Plan vigente al corte, o `churned` |
| `is_churned`, `churn_date`, `churned_from_plan` | Cancelación, su fecha y el plan desde el que cancela |
| `n_events`, `n_upgrades`, `ever_upgraded` | Actividad del cliente |
| `plan_path` | Recorrido completo, p. ej. `trial > basic monthly > pro monthly > churn` |
| `last_event_plan`, `last_event_date` | Último evento registrado |
| `observation_end` | Fecha de corte de observación (**supuesto**: última fecha registrada) |
| `follow_up_days` | Días observados desde el inicio del trial hasta el churn o el corte |
| `paid_days` | Días como cliente pago hasta el churn o el corte (vacío si nunca pagó) |
| `is_censored` | `True` si el cliente sigue activo al corte (no se conoce su desenlace) |
| `annual_term_expired_no_event` | Plan anual vencido al corte sin evento posterior; se trata como activo (advertencia A1) |
