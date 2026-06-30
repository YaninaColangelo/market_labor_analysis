# Market Labor Analysis - Data Analyst Roles

Proyecto de análisis del mercado laboral para roles de Data Analyst en España y Argentina. El propósito es estudiar qué valor esperan generar las organizaciones al contratar analistas de datos, qué problemas buscan resolver y qué competencias profesionales aparecen asociadas a esas necesidades.

El enfoque principal no es tecnológico. SQL, Python, Power BI u otras herramientas se analizan como variables secundarias: señales del modo de trabajo esperado, no como objetivo final del proyecto.

## Propósito

Este repositorio permite organizar, limpiar, clasificar y analizar ofertas laborales de Data Analyst con una mirada orientada a negocio, organización y formación académica. El análisis busca responder preguntas como:

- Que necesidades organizacionales aparecen en las ofertas.
- Que competencias analíticas, comunicacionales y de negocio se demandan.
- Que herramientas se mencionan y con que tipo de necesidad se relacionan.
- Como varian las expectativas entre España y Argentina.
- Que brechas o alineamientos existen respecto de la formación de un analista.

## Estructura

```text
market-labor-analysis/
├── docs/              # Marco conceptual, objetivos, preguntas y diccionario
├── data/              # Datos brutos, procesados y diccionario editable
├── notebooks/         # Exploracion y analisis progresivo
├── src/               # Codigo modular del proyecto
├── database/          # Modelo SQL y consultas analiticas
├── visualizations/    # Graficos, dashboards y exportaciones
└── reports/           # Informes y hallazgos
```

## Como ejecutar el proyecto

1. Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

En macOS/Linux:

```bash
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar una limpieza inicial:

```bash
python -m src.data_cleaning
```

4. Abrir los notebooks en VS Code o Jupyter:

```bash
jupyter lab
```

## Flujo sugerido

1. Recolectar ofertas en `data/raw/ofertas_brutas.csv`.
2. Limpiar y normalizar campos con `src/data_cleaning.py`.
3. Clasificar necesidades, competencias y herramientas con `src/data_classification.py`.
4. Crear variables analiticas con `src/feature_engineering.py`.
5. Explorar resultados en notebooks.
6. Consolidar hallazgos en `reports/insights_clave.md` e `reports/informe_final.md`.

## Criterio de analisis

Cada oferta se interpreta como una expresion de una necesidad organizacional. Por ejemplo, una mencion a dashboards no se registra solamente como uso de Power BI, sino como posible necesidad de seguimiento de indicadores, control de gestion, visibilidad operativa o soporte a decisiones.

## Estado inicial

El repositorio incluye datos de ejemplo y funciones base para comenzar. Los datos semilla son ficticios y sirven para validar la estructura antes de cargar ofertas reales.
