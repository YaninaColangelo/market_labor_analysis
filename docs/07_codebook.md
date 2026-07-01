# Codebook metodologico

## Proposito del documento

Este Codebook documenta las reglas utilizadas para interpretar y codificar el contenido textual de ofertas laborales para roles de Data Analyst. No reemplaza al Data Dictionary: mientras el diccionario de datos describe variables, tipos y estructura del dataset, este documento define los criterios metodologicos para transformar texto libre en categorias analiticas.

El objetivo es establecer criterios consistentes, reproducibles y trazables para reducir la subjetividad del proceso de codificacion. El documento debe permitir que otro analista aplique las mismas reglas sobre un conjunto similar de ofertas y obtenga resultados comparables.

## Marco metodologico

El proyecto utiliza analisis de contenido aplicado a ofertas laborales. Cada oferta se interpreta como un documento organizacional que expresa necesidades, expectativas de valor, responsabilidades y capacidades requeridas.

El principio central del proceso es:

> Las organizaciones no demandan herramientas; demandan soluciones a problemas organizacionales. Las herramientas representan un medio para alcanzar un objetivo de negocio.

Por este motivo, la codificacion no comienza por la herramienta mencionada, sino por la necesidad organizacional que la oferta permite identificar. SQL, Python, Excel, Power BI u otras tecnologias se registran como evidencia observable, pero no deben utilizarse para inferir automaticamente la necesidad principal.

## Flujo logico de codificacion

El proceso de interpretacion debe seguir el siguiente orden:

```text
Oferta laboral
↓
Necesidad organizacional
↓
Resultado esperado
↓
Competencias requeridas
↓
Herramientas mencionadas
```

Este flujo evita una lectura tecnocentrica de las ofertas. Primero se identifica que problema intenta resolver la organizacion; luego se determina que resultado espera obtener, que competencias necesita el profesional y, finalmente, que herramientas aparecen como medios de trabajo.

## Estructura de la codificacion

Para cada oferta laboral, el analista debe responder cuatro preguntas en orden.

### 1. Que problema intenta resolver la organizacion

Esta dimension representa la necesidad organizacional principal. Puede aparecer de forma explicita en la descripcion del puesto o inferirse a partir de responsabilidades, objetivos del area, indicadores mencionados o destinatarios del trabajo analitico.

Ejemplos de problemas: mejorar la toma de decisiones, medir desempeno, integrar fuentes de datos, automatizar procesos, asegurar calidad del dato, optimizar operaciones, comprender clientes o cumplir requerimientos de reporting.

### 2. Que resultado espera obtener

Esta dimension describe el valor esperado por la organizacion. No se refiere a la tarea en si, sino al efecto que esa tarea deberia producir.

Ejemplos de resultados esperados:

- decisiones mas informadas;
- mayor visibilidad sobre indicadores;
- reduccion de trabajo manual;
- datos mas confiables;
- mejora de procesos internos;
- reportes consistentes para direccion o areas regulatorias.

### 3. Que competencias necesita el profesional

Esta dimension registra las capacidades requeridas para responder a la necesidad identificada. Las competencias pueden inferirse tanto de responsabilidades como de requisitos formales.

Una misma oferta puede contener multiples competencias. Por ejemplo, una posicion orientada a reporting ejecutivo puede requerir SQL, criterio analitico, comprension de negocio y comunicacion con stakeholders.

### 4. Que herramientas menciona la oferta

Esta dimension registra tecnologias, plataformas o aplicaciones mencionadas de forma observable. Las herramientas deben codificarse como evidencia textual y no como sustituto de la interpretacion organizacional.

Por ejemplo, Power BI puede estar asociado a reporting ejecutivo, seguimiento operativo o inteligencia comercial. La herramienta por si sola no define la necesidad.

## Reglas generales de codificacion

- Leer primero la descripcion completa de la oferta antes de revisar los requisitos.
- Buscar evidencia en todo el documento: titulo, descripcion, responsabilidades, requisitos, area, industria y modalidad del rol.
- Registrar una necesidad organizacional principal por oferta.
- Registrar necesidades secundarias cuando la oferta contenga mas de un proposito relevante.
- Una oferta puede contener multiples competencias.
- Una oferta puede contener multiples herramientas.
- Justificar la codificacion cuando exista ambiguedad, especialmente si la necesidad fue inferida.
- No inferir automaticamente la necesidad organizacional a partir de una herramienta.
- Priorizar responsabilidades y objetivos del rol por encima de listas genericas de requisitos.
- Si una oferta no puede clasificarse con las categorias existentes, registrar el caso para revision del Codebook.
- Mantener trazabilidad entre el codigo asignado y las frases de la oferta que lo respaldan.

## Catalogo inicial de necesidades organizacionales

### N01 - Apoyo a la toma de decisiones

**Definicion:** necesidad de convertir datos en informacion util para decidir, priorizar acciones o evaluar alternativas de negocio.

**Cuando utilizarlo:** cuando la oferta mencione apoyo a decisiones, generacion de insights, recomendaciones, analisis para direccion, estrategia o evaluacion de escenarios.

**Cuando NO utilizarlo:** no usarlo solo porque se mencionan dashboards o reportes. Debe existir evidencia de que el analisis sera utilizado para decidir o recomendar acciones.

**Ejemplos de expresiones frecuentes:**

- "apoyar la toma de decisiones";
- "generar insights accionables";
- "presentar recomendaciones al negocio";
- "analisis para la direccion";
- "identificar oportunidades de mejora".

### N02 - Medicion del desempeno

**Definicion:** necesidad de monitorear resultados, indicadores, cumplimiento de objetivos o evolucion de metricas relevantes para un area o proceso.

**Cuando utilizarlo:** cuando la oferta mencione KPIs, performance, seguimiento de objetivos, metricas comerciales, indicadores operativos o evaluacion periodica de resultados.

**Cuando NO utilizarlo:** no usarlo si la medicion aparece solo como una tarea instrumental sin relacion clara con seguimiento de resultados.

**Ejemplos de expresiones frecuentes:**

- "seguimiento de KPIs";
- "monitoreo de indicadores";
- "analisis de performance";
- "control de objetivos";
- "tableros de seguimiento".

### N03 - Integracion de datos

**Definicion:** necesidad de reunir, conectar o consolidar informacion proveniente de distintas fuentes para construir una vision mas completa y util del negocio.

**Cuando utilizarlo:** cuando la oferta mencione integracion de fuentes, consolidacion de bases, extraccion de datos, cruce de informacion entre sistemas o preparacion de datasets para analisis.

**Cuando NO utilizarlo:** no usarlo solo porque se menciona SQL. Debe existir evidencia de combinacion, consolidacion o disponibilizacion de datos.

**Ejemplos de expresiones frecuentes:**

- "integrar datos de diferentes fuentes";
- "consolidar informacion";
- "cruzar bases de datos";
- "extraer y preparar datasets";
- "centralizar informacion".

### N04 - Automatizacion de procesos

**Definicion:** necesidad de reducir tareas manuales, acelerar rutinas analiticas o estandarizar procesos repetitivos mediante soluciones basadas en datos.

**Cuando utilizarlo:** cuando la oferta mencione automatizacion de reportes, scripts, optimizacion de rutinas, reduccion de tiempos manuales o mejora de flujos recurrentes.

**Cuando NO utilizarlo:** no usarlo solo porque se menciona Python. Debe existir evidencia de eliminacion de trabajo manual o mejora de eficiencia en procesos.

**Ejemplos de expresiones frecuentes:**

- "automatizar reportes";
- "reducir tareas manuales";
- "optimizar procesos recurrentes";
- "desarrollar scripts de automatizacion";
- "mejorar tiempos de procesamiento".

### N05 - Calidad del dato

**Definicion:** necesidad de asegurar que los datos sean confiables, consistentes, completos y adecuados para su uso analitico o de gestion.

**Cuando utilizarlo:** cuando la oferta mencione validacion, limpieza, consistencia, control de calidad, definicion de metricas, documentacion de datos o deteccion de errores.

**Cuando NO utilizarlo:** no usarlo cuando la limpieza de datos aparezca como tarea menor sin evidencia de preocupacion organizacional por confiabilidad o gobernanza.

**Ejemplos de expresiones frecuentes:**

- "validar calidad de datos";
- "asegurar consistencia de la informacion";
- "limpieza y depuracion de bases";
- "documentar definiciones de metricas";
- "detectar inconsistencias".

### N06 - Optimizacion operativa

**Definicion:** necesidad de mejorar procesos, recursos, tiempos, costos o desempeno operativo mediante analisis de datos.

**Cuando utilizarlo:** cuando la oferta se oriente a operaciones, eficiencia, mejora de procesos, identificacion de desvíos, tiempos de atencion, productividad o reduccion de costos.

**Cuando NO utilizarlo:** no usarlo para cualquier mencion general a "mejora" si no hay evidencia de proceso operativo o funcionamiento interno.

**Ejemplos de expresiones frecuentes:**

- "mejora de procesos";
- "analisis de desvíos operativos";
- "optimizar tiempos de atencion";
- "eficiencia operativa";
- "identificar cuellos de botella".

### N07 - Inteligencia comercial

**Definicion:** necesidad de comprender clientes, ventas, mercado, productos o comportamiento comercial para generar oportunidades de crecimiento o mejorar decisiones comerciales.

**Cuando utilizarlo:** cuando la oferta mencione analisis de clientes, ventas, pricing, segmentacion, campanas, comportamiento de usuarios, mercado o rentabilidad comercial.

**Cuando NO utilizarlo:** no usarlo si la oferta pertenece a un area comercial pero las responsabilidades se limitan a reporting administrativo sin analisis de clientes, ventas o mercado.

**Ejemplos de expresiones frecuentes:**

- "analisis de clientes";
- "seguimiento de ventas";
- "segmentacion de usuarios";
- "identificar oportunidades comerciales";
- "analisis de mercado";
- "rentabilidad por producto".

### N08 - Cumplimiento y reporting

**Definicion:** necesidad de producir informacion estructurada, periodica y confiable para cumplir requerimientos internos, ejecutivos, regulatorios o de control.

**Cuando utilizarlo:** cuando la oferta mencione reportes recurrentes, reporting ejecutivo, cumplimiento normativo, auditoria, control interno, reportes regulatorios o entregables formales.

**Cuando NO utilizarlo:** no usarlo para cualquier visualizacion o dashboard si no existe evidencia de obligacion, periodicidad, control o destinatario formal.

**Ejemplos de expresiones frecuentes:**

- "reporting mensual";
- "reportes para gerencia";
- "cumplimiento regulatorio";
- "informes de control";
- "preparacion de reportes ejecutivos";
- "auditoria de informacion".

## Codificacion de competencias

Las competencias describen capacidades del profesional. Pueden inferirse de responsabilidades, requisitos, objetivos del rol y forma en que la oferta describe la interaccion con otras areas.

### Competencias tecnicas

Capacidades para extraer, transformar, modelar, visualizar o automatizar datos mediante herramientas especificas.

Ejemplos:

- manejo de SQL;
- procesamiento con Python o R;
- uso avanzado de Excel;
- construccion de dashboards;
- modelado de datos;
- documentacion tecnica.

### Competencias analiticas

Capacidades para formular preguntas, explorar informacion, interpretar patrones, evaluar evidencia y construir conclusiones.

Ejemplos:

- pensamiento analitico;
- analisis estadistico;
- interpretacion de indicadores;
- identificacion de tendencias;
- evaluacion de hipotesis;
- lectura critica de datos.

### Competencias de negocio

Capacidades para comprender objetivos organizacionales, procesos, metricas, clientes, productos o restricciones del contexto.

Ejemplos:

- comprension de KPIs de negocio;
- lectura de procesos comerciales u operativos;
- orientacion a resultados;
- conocimiento sectorial;
- capacidad de traducir preguntas de negocio en analisis.

### Competencias transversales

Capacidades que permiten que el analisis tenga impacto organizacional, especialmente en entornos colaborativos.

Ejemplos:

- comunicacion de hallazgos;
- storytelling con datos;
- trabajo con stakeholders;
- autonomia;
- priorizacion;
- documentacion;
- colaboracion interdisciplinaria.

## Codificacion de herramientas

Las herramientas constituyen evidencia observable dentro de la oferta, pero no representan por si mismas la necesidad organizacional. Deben registrarse como menciones explicitas, manteniendo la forma normalizada definida en el Data Dictionary.

Herramientas frecuentes:

- SQL;
- Python;
- Excel;
- Power BI;
- Tableau;
- Looker;
- R.

Si una herramienta aparece asociada a una responsabilidad, registrar ambas dimensiones por separado. Por ejemplo, "automatizar reportes con Python" debe codificarse como automatizacion de procesos y, adicionalmente, Python como herramienta mencionada.

## Procedimiento de validacion

Antes de iniciar la recoleccion definitiva, el Codebook debe validarse mediante una prueba piloto con un conjunto reducido de ofertas. Esta prueba permite evaluar si las categorias son comprensibles, suficientes y aplicables de manera consistente.

### Pasos de la prueba piloto

1. Seleccionar una muestra inicial de ofertas de España y Argentina.
2. Codificar cada oferta aplicando este Codebook.
3. Registrar casos ambiguos, categorias insuficientes y expresiones no contempladas.
4. Comparar resultados entre analistas, si participa mas de una persona.
5. Ajustar definiciones, criterios de inclusion o criterios de exclusion.
6. Documentar todo cambio metodologico en la tabla de control de versiones.

Durante la prueba piloto podran incorporarse nuevos codigos o redefinirse categorias existentes. Una vez iniciada la recoleccion definitiva, los cambios metodologicos deben controlarse con mayor cuidado para preservar la comparabilidad del estudio.

## Manejo de ambiguedades

Cuando una oferta permita mas de una interpretacion, el analista debe:

- conservar la categoria principal que tenga mayor respaldo textual;
- registrar necesidades secundarias si corresponde;
- anotar la frase o seccion que justifica la decision;
- marcar el caso para revision si la categoria asignada no resulta estable;
- evitar inferencias basadas exclusivamente en herramientas o en supuestos sobre la industria.

## Control de versiones metodologicas

| Version | Fecha | Cambio realizado | Justificacion |
|---|---|---|---|
| 0.1 | 2026-07-01 | Creacion inicial del Codebook con ocho codigos de necesidades organizacionales | Establecer criterios base para la prueba piloto |
|  |  |  |  |
|  |  |  |  |

## Criterio de cierre

El Codebook se considera operativo cuando las categorias permiten clasificar la mayoria de las ofertas de la prueba piloto, las decisiones ambiguas pueden justificarse con evidencia textual y otro analista puede aplicar las mismas reglas sin depender de interpretaciones personales no documentadas.
