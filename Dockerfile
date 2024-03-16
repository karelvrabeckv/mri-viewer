FROM kitware/trame:py3.9

COPY --chown=trame-user:trame-user . /local-app
COPY --chown=trame-user:trame-user ./docker /deploy

ENV TRAME_CLIENT_TYPE=vue3
RUN /opt/trame/entrypoint.sh build
