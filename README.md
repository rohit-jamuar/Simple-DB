# Simple-DB
An in-memory database similar to Redis. There's also support for nested transactions.

# Supported commands (read docstring to know more about each op)
1. SET *name* *value*
2. GET *name*
3. UNSET *name*
4. NUMEQUALTO *value*
5. END
6. BEGIN
7. COMMIT
8. ROLLBACK

# Run
python simple_database.py *file\_name*

The *file\_name* should have commands listed one per line. Execution will read file's contents on a per-line basis and  output the result to STDOUT.
