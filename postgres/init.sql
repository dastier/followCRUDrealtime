create table "users"
(
    id    bigserial    not null primary key,
    name  varchar(100) not null
);

CREATE OR REPLACE FUNCTION notify_event() RETURNS trigger AS
$BODY$
BEGIN
  PERFORM pg_notify(
    'events',
    json_build_object(
      'operation', TG_OP,
      'record', row_to_json(NEW)
    )::text
  );
  RETURN new;
END;
$BODY$
LANGUAGE 'plpgsql' VOLATILE COST 100;


-- create trigger:

CREATE TRIGGER notify_users_event
BEFORE INSERT OR UPDATE OR DELETE ON users
  FOR EACH ROW
  EXECUTE PROCEDURE notify_event();