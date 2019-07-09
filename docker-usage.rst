Deployment example

``.env`` file

::

    DATABASE_URI=sqlite:////app/db/pinnwand.sqlite
    LOG_LEVEL=INFO

Build

::

    docker build . -t pinnwand

Run

::

    docker run \
        --env-file .env \
        -p 8000:8000 \
        -v "pinnwand_db:/app/db" \
        pinnwand

**TODO** run as user
