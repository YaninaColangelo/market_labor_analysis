-- Consultas analiticas iniciales.

-- Distribucion de necesidades por pais.
SELECT
    o.pais,
    c.necesidad_organizacional,
    COUNT(*) AS cantidad_ofertas
FROM ofertas o
JOIN clasificacion_ofertas c ON o.id_oferta = c.id_oferta
GROUP BY o.pais, c.necesidad_organizacional
ORDER BY o.pais, cantidad_ofertas DESC;

-- Herramientas mencionadas segun necesidad organizacional.
SELECT
    c.necesidad_organizacional,
    c.herramientas_mencionadas,
    COUNT(*) AS cantidad_ofertas
FROM clasificacion_ofertas c
GROUP BY c.necesidad_organizacional, c.herramientas_mencionadas
ORDER BY cantidad_ofertas DESC;

-- Comparacion de orientacion a negocio por pais.
SELECT
    o.pais,
    AVG(c.nivel_orientacion_negocio) AS promedio_orientacion_negocio
FROM ofertas o
JOIN clasificacion_ofertas c ON o.id_oferta = c.id_oferta
GROUP BY o.pais;
