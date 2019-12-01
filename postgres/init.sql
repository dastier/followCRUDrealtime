create table "users"
(
    id    bigserial    not null primary key,
    name  varchar(100) not null
);

CREATE OR REPLACE FUNCTION notify_event() RETURNS trigger AS
$BODY$

DECLARE
  subj text;

BEGIN
  IF (TG_OP = 'DELETE') THEN
    PERFORM pg_notify(
      'events',
      json_build_object(
        'operation', TG_OP,
        'record', row_to_json(OLD)
      )::text
    );
    RETURN OLD;
  ELSE
    PERFORM pg_notify(
      'events',
      json_build_object(
        'operation', TG_OP,
        'record', row_to_json(NEW)
      )::text
    );
  END IF;

  RETURN NEW;
  
END;





$BODY$
LANGUAGE 'plpgsql' VOLATILE COST 100;


-- create trigger:

CREATE TRIGGER notify_users_event
AFTER INSERT OR UPDATE OR DELETE ON users
  FOR EACH ROW
  EXECUTE PROCEDURE notify_event();