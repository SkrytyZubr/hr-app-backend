# [Work in progress]

# Alembic

## Modul for db migration, use for changing anything in db

Generate new revision after any changes in db -->
`alembic revision --autogenerate -m "<descritpion>"`

Set new revision as current (adjust db) -->
`alembic upgrade head`