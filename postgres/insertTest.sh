#!/bin/bash
export PGPASSWORD=postgres
psql -h localhost -U postgres -d docker -c "insert into users (name) values ('op')"