-- Modelo relacional inicial para ofertas de Data Analyst.

CREATE TABLE IF NOT EXISTS ofertas (
    id_oferta TEXT PRIMARY KEY,
    fecha_publicacion DATE,
    fuente TEXT,
    url TEXT,
    pais TEXT,
    ciudad TEXT,
    empresa TEXT,
    industria TEXT,
    titulo_puesto TEXT,
    descripcion TEXT,
    responsabilidades TEXT,
    requisitos TEXT,
    modalidad TEXT,
    seniority TEXT,
    formacion_requerida TEXT
);

CREATE TABLE IF NOT EXISTS clasificacion_ofertas (
    id_oferta TEXT PRIMARY KEY,
    necesidad_organizacional TEXT,
    valor_esperado TEXT,
    competencias_requeridas TEXT,
    herramientas_mencionadas TEXT,
    nivel_orientacion_negocio INTEGER,
    FOREIGN KEY (id_oferta) REFERENCES ofertas(id_oferta)
);
