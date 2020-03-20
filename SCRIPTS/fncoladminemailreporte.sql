-- Function: fncoladminemailreporte()

-- DROP FUNCTION fncoladminemailreporte();

CREATE OR REPLACE FUNCTION fncoladminemailreporte()
  RETURNS TABLE(descripcion text, total integer) AS
$BODY$
	DECLARE

    iTotalAmbosVacios   INTEGER;
    iTotalDispositivos   INTEGER;
    iTotalCelular       INTEGER;
    iTotalNull          INTEGER;
    iOpcion             INTEGER;
    fechaActual         DATE;
	
	BEGIN	
        iOpcion = 1;
	SELECT CURRENT_DATE -1 INTO fechaActual;
	
	SELECT 
            SUM(CASE  WHEN b.iddispositivo    =  ''   AND  b.telefonopromotor  = '' THEN  1 ELSE 0 END) AS totalAmbosVacios, 
            SUM(CASE  WHEN b.iddispositivo    <> ''   THEN  1 ELSE 0 END) AS totalDispositivo,
            SUM(CASE  WHEN b.iddispositivo    =  ''   AND  b.telefonopromotor <> '' THEN  1 ELSE 0 END) AS totalCelular, 
            SUM(CASE  WHEN b.telefonopromotor IS NULL AND  b.telefonopromotor IS NULL THEN 1 ELSE 0 END) AS totalNull INTO  iTotalAmbosVacios,iTotalDispositivos,iTotalCelular,iTotalNull
            FROM colinfxpromotores a
            LEFT JOIN promotoressms b ON (a.empleado =  b.empleado) 
            WHERE motivosuspension = ''  AND fechasuspension = '1900-01-01' AND a.empleado != 0 AND claveconsar !=0;
		
            descripcion := 'Promotores sin APP móvil y con celular registrado';
            total := iTotalCelular;
            return next;
            descripcion := 'Promotores sin APP móvil y sin celular ';
            total := iTotalNull;
            return next;
            descripcion := 'Promotores con APP móvil';
            total := iTotalDispositivos;
            return next;

            iopcion = iopcion + 2;
            iTotalDispositivos = 0;
            iTotalCelular = 0;

        IF (iOpcion = 3 ) THEN


	Select COUNT(*) INTO iTotalDispositivos from bitacoranotificacion  where  fechaalta = fechaActual; -- Conteo de notificaciones PUSH
	Select COUNT(*) INTo iTotalCelular from bitacorasms where fechaalta = fechaActual; -- Conteo de SMS enviados

	    descripcion := 'Conteo de notificaciones PUSH';
            total := iTotalDispositivos;
            return next;
            descripcion := 'Conteo de SMS enviados';
            total := iTotalCelular;
            iopcion = iopcion + 1;
            iTotalCelular = 0;
            iTotalDispositivos = 0;
            return next;
        END IF;		
        
        IF (iOpcion = 4 ) THEN


	Select COUNT(*) INTO iTotalCelular from promotoressms where fechaaccesomenu = fechaActual;    -- Acceso al Menu
	
	    descripcion := 'Acceso al Menu';
            total := iTotalCelular;
            return next;
            iopcion = iopcion + 1;
            iTotalCelular = 0;
            iTotalDispositivos = 0;
        END IF;				

	
        
		
	
	END;                                              
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION fncoladminemailreporte()
  OWNER TO sysaforeglobal;
