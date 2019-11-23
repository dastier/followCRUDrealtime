#!/bin/bash
GPASSWORD=postgres psql -h localhost -U postgres -d docker -c "select * from users"