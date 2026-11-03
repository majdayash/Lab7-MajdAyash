# Lab 7 – Python testing

Flask REST API (from Lab 5) that adds, reads, updates and deletes users in a SQLite database,
now tested with pytest.

## Run

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The app creates `database.db` on first run, fills it with the users in `initial_users`, and listens on `http://localhost:5001`
(port 5000 is taken by AirPlay Receiver on macOS).

## Endpoints

| # | Endpoint | Method | Description |
|---|----------|--------|-------------|
| 1 | `/api/users` | GET | Get the list of all users in the database |
| 2 | `/api/users/<user_id>` | GET | Get a single user record that matches the id |
| 3 | `/api/users/add` | POST | Create a new user record |
| 4 | `/api/users/update` | PUT | Update a user record |
| 5 | `/api/users/delete/<user_id>` | DELETE | Delete a user record |

## Postman

`postman/` contains the **Flask user app** collection (one request per endpoint, each with a saved example)
and the **Flask user app - local** environment, which defines `base_url`. All requests use `{{base_url}}`.
Import both files in Postman and select the environment.

## Tests

```bash
pytest
```

| File | What it tests |
|------|---------------|
| `test_user_Majd_Ayash.py` | Graded activity: initial users on first run, `insert_user`, `get_users`, `get_user_by_id`, `update_user`, `delete_user` and the API endpoints (status code and data) |
| `test_capitalize.py` | `capital_case` in `capitalize.py` |
| `test_wallet.py` | `Wallet` in `wallet.py`, using fixtures |
| `test_hello_add.py` | The `/add` endpoint in `hello_add.py` |

Each user test runs against its own temporary database, so `database.db` is never touched.
