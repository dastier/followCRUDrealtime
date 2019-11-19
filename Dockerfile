FROM postgres:12.1
COPY postgres/init.sql /docker-entrypoint-initdb.d/
CMD ["/bin/sleep", "3600"]