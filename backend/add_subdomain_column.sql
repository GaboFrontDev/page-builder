-- Agregar columna subdomain a la tabla pages
ALTER TABLE pages ADD COLUMN subdomain VARCHAR;

-- Quitar índice único de subdomain si existe
DROP INDEX IF EXISTS ix_pages_subdomain;

-- Crear índice único compuesto en (subdomain, slug)
CREATE UNIQUE INDEX uq_subdomain_slug ON pages(subdomain, slug); 