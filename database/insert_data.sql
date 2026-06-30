-- Datos semilla para pruebas locales.

INSERT INTO ofertas (
    id_oferta, fecha_publicacion, fuente, url, pais, ciudad, empresa, industria,
    titulo_puesto, descripcion, responsabilidades, requisitos, modalidad, seniority, formacion_requerida
) VALUES
(
    'OF-001', '2026-06-01', 'Ejemplo Interno', 'https://example.com/oferta-001',
    'España', 'Madrid', 'DataRetail Iberia', 'Retail', 'Data Analyst',
    'Buscamos analista para mejorar el seguimiento de ventas, margenes y comportamiento de clientes.',
    'Construir reportes comerciales; analizar indicadores; colaborar con equipos de ventas y marketing.',
    'SQL; Power BI; Excel avanzado; capacidad de comunicar hallazgos.',
    'Hibrido', 'Semi Senior', 'Administracion, Economia, Ingenieria o similar'
);

INSERT INTO clasificacion_ofertas (
    id_oferta, necesidad_organizacional, valor_esperado, competencias_requeridas,
    herramientas_mencionadas, nivel_orientacion_negocio
) VALUES
(
    'OF-001',
    'Seguimiento de indicadores y performance',
    'Mejorar decisiones comerciales',
    'analisis comercial; visualizacion; comunicacion',
    'SQL; Power BI; Excel',
    5
);
