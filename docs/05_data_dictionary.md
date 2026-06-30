# Data dictionary

Este documento describe conceptualmente los campos principales del dataset. El archivo editable se encuentra en `data/dictionary/data_dictionary.xlsx`.

## Campos identificatorios

| Campo | Descripcion | Tipo esperado |
|---|---|---|
| id_oferta | Identificador unico de la oferta | Texto |
| fecha_publicacion | Fecha en que fue publicada o recolectada | Fecha |
| fuente | Portal o sitio de origen | Texto |
| url | Enlace a la oferta | Texto |

## Contexto laboral

| Campo | Descripcion | Tipo esperado |
|---|---|---|
| pais | Pais de la oferta | Categoria |
| ciudad | Ciudad o ubicacion declarada | Texto |
| empresa | Nombre de la empresa | Texto |
| industria | Sector economico principal | Categoria |
| modalidad | Remoto, hibrido o presencial | Categoria |
| seniority | Junior, semi senior, senior o no especificado | Categoria |

## Contenido de la oferta

| Campo | Descripcion | Tipo esperado |
|---|---|---|
| titulo_puesto | Nombre del rol publicado | Texto |
| descripcion | Texto completo o resumen de la oferta | Texto largo |
| responsabilidades | Tareas esperadas | Texto largo |
| requisitos | Requisitos declarados | Texto largo |

## Variables analiticas

| Campo | Descripcion | Tipo esperado |
|---|---|---|
| necesidad_organizacional | Problema principal que la empresa busca resolver | Categoria |
| competencias_requeridas | Competencias detectadas en la oferta | Lista |
| herramientas_mencionadas | Herramientas o tecnologias solicitadas | Lista |
| formacion_requerida | Carrera, area o nivel formativo solicitado | Texto |
| valor_esperado | Tipo de valor que el rol promete generar | Categoria |
| nivel_orientacion_negocio | Intensidad del foco en negocio | Entero 1-5 |

## Criterio de calidad

Cada variable derivada debe conservar trazabilidad hacia el texto original de la oferta. Cuando una necesidad sea inferida, debe poder justificarse mediante palabras clave, responsabilidades o contexto del rol.
