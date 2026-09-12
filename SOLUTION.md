# Solution Writeup — TinyCorp Employee Portal

Flag: `FLAG{s1ngl3_qu0t3_5t0ps_th3_qu3ry}`

## The vulnerability

`app.py`'s `/login` route builds its SQL query by directly formatting
user input into a string:

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

This is a classic **SQL injection**. Because the username is inserted
straight into the query text (instead of being passed as a bound
parameter), a crafted username can change what the query actually asks
the database.

## The exploit

On the login form, submit:

- **Username:** `admin' -- `
- **Password:** *(anything, it's ignored)*

The resulting query becomes:

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = ''
```

`--` starts an SQL comment, so everything after it — including the
password check — is ignored. The query now just asks "find the user
named admin," which succeeds regardless of what password was submitted.
The app logs you in as `admin` and redirects to `/dashboard`, which
displays the flag.

Equivalent payloads that also work: `admin' OR '1'='1' -- ` or
`' OR role='admin' -- ` (with an empty username field), since both
manipulate the WHERE clause the same way.

## Why this matters (talking point for players)

The fix is to use parameterized queries, which keep user input as *data*
rather than letting it become part of the SQL *code*:

```python
cur.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password),
)
```

With this change, `admin' -- ` is treated as a literal (and nonexistent)
username, and the injection stops working entirely.

## Design notes (for whoever maintains this challenge)

- The flag is set via the `CTF_FLAG` environment variable in
  `docker-compose.yml` — change it there to mint a fresh flag per event,
  no code changes needed.
- The database is recreated fresh on every container start (see the
  `RUN rm -f tinycorp.db` line in the Dockerfile combined with
  `init_db()` running automatically on first request), so there's no
  persistent state between runs.
- `employee.html` deliberately nudges players toward the admin dashboard
  after a normal login, in case someone tries valid-looking employee
  creds first out of curiosity — it's a dead end by design, to make the
  "the real prize is somewhere else" structure explicit.
- To make this harder later: switch to parameterized queries but
  reintroduce a *second*, subtler vulnerability (e.g. an IDOR on a
  `/profile?id=` endpoint, or a broken session/JWT check) so players who
  assume "SQLi again" get thrown off.
