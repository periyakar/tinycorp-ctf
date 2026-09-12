# TinyCorp Employee Portal

**Category:** Web Exploitation
**Difficulty:** Beginner
**Points suggestion:** 100–150

## Description

TinyCorp just launched their internal employee portal. IT swears it's
secure. Can you get into the admin dashboard?

You don't have any valid admin credentials. You'll have to find another
way in.

**Access:** run the app (see below) and open it in your browser.

## Running it

**Option A — Docker (recommended):**

```
docker compose up --build
```

Then visit http://localhost:5000

**Option B — plain Python:**

```
pip install -r requirements.txt
python3 app.py
```

Then visit http://localhost:5000

## Hints (release progressively if needed)

1. *"The login form talks to a database. What happens if your username
   isn't just a username?"*
2. *"You don't need the admin's real password — you just need the
   database to stop checking for one."*
3. *"Try ending your username with something that makes the rest of the
   query stop mattering."*

## Rules

- This app is intentionally vulnerable — that's the whole point. Please
  don't scan/attack it if it's ever deployed anywhere other than an
  isolated CTF environment.
- Flag format: `FLAG{...}`
