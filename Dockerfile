FROM python:3.7-alpine

EXPOSE 8000
VOLUME /app/db
WORKDIR /app/src

COPY setup.* pyproject.toml ./
COPY pinnwand ./pinnwand
RUN pip --no-cache-dir install .

ENTRYPOINT ["python", "-m", "pinnwand"]
CMD ["http"]
