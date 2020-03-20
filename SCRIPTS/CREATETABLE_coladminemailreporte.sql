CREATE TABLE coladminemailreporte
(
  keyx serial NOT NULL,
  fechaalta date NOT NULL DEFAULT now(),
  correo character(50) NOT NULL DEFAULT ''::bpchar,
  nombre character(150) NOT NULL DEFAULT ''::bpchar,
  tiporeporte integer NOT NULL DEFAULT 0,
  estatusactivo integer NOT NULL DEFAULT 0
)
WITH (
  OIDS=FALSE
);
ALTER TABLE coladminemailreporte
  OWNER TO sysaforeglobal;
