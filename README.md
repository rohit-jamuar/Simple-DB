# Simple-DB
An in-memory database similar to Redis. There's also support for nested transactions.

## Supported commands (read docstring to know more about each op)
1. SET *name* *value*
2. GET *name*
3. UNSET *name*
4. NUMEQUALTO *value*
5. BEGIN
6. COMMIT
7. ROLLBACK
8. END

## Run
1. `python simple_database.py`, or
2. If you have a list of commands written in a file: `cat file_name | python simple_database.py`

- The database interactions happen over command-line.
- Database driver will read contents on a per-line basis andoutput the result to STDOUT.
- It is assumed that all dB interactions conclude with a __END__ command.
