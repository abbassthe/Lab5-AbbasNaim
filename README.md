# Lab 5 — Postman and APIs

Abbas Naim · Software Tools Lab

Repository: https://github.com/abbassthe/Lab5-AbbasNaim

This Flask app adds, lists, updates and deletes users in SQLite. The Postman collection is named **Flask user app**. It includes all five required endpoints, response examples, and checks for the full CRUD sequence.

## Run

Use Python 3.10 or newer:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python seed.py
python app.py
```

On Windows, activate with `.venv\Scripts\activate` and use `python` in place of `python3` if needed. SQLite is part of Python; no separate SQLite pip package is required.

The server runs at `http://127.0.0.1:5001`. Port 5001 avoids the macOS AirPlay service often using port 5000. The environment file already contains this URL. The app creates `database.db` automatically. `seed.py` adds one fictional sample user only when the database is empty.

## Postman

1. Import both JSON files from `postman/`.
2. Select the **Flask local** environment.
3. Run **Flask user app** in its numbered order, starting with **01 Add user**.
4. Open the saved example below each request to see a captured response.

Every URL starts with `{{base_url}}`. The POST request stores the generated `user_id` in the environment; later requests use `{{user_id}}`. The PUT request sends the ID as a JSON number. The sequence creates Omar Saleh, reads the record, updates the address and phone, verifies persistence, deletes the record and confirms it is gone. It leaves pre-existing users intact.

The installed Postman lightweight client can send individual requests without an account. Importing collections and environments into the full desktop workspace requires sign-in. The supplied files can also be run without an account using Newman:

```sh
npx --yes newman run "postman/Flask user app.postman_collection.json" -e "postman/Flask local.postman_environment.json"
```

## Endpoints

| Method | Path | Result |
| --- | --- | --- |
| GET | `/api/users` | List all users (200) |
| GET | `/api/users/<user_id>` | Get one user (200 or 404) |
| POST | `/api/users/add` | Add a user (201) |
| PUT | `/api/users/update` | Update a user (200 or 404) |
| DELETE | `/api/users/delete/<user_id>` | Delete a user (200 or 404) |

POST requires `name`, `email`, `phone`, `address` and `country` as nonempty strings. PUT requires those fields plus a positive integer `user_id`. Invalid input returns 400, a non-JSON body returns 415, and missing records return 404. Errors are JSON. SQL statements bind values with placeholders.

## Files and evidence

- `app.py`: Flask routes and request validation.
- `database.py`: SQLite schema and CRUD functions.
- `database.db`: sample database included in the submission ZIP; generated locally for GitHub clones.
- `postman/`: collection with eight saved examples and the local environment.
- `Lab5-Report.docx`: lab report with screenshots.
- `screenshots/`: actual Postman and browser captures.
- `evidence/`: HTTP responses, unit tests, Newman results and Git history.
- `test_api.py`: tests using an isolated temporary database.

```sh
python -m unittest -v test_api.py
```

## Git workflow

The SQLite layer was committed and pushed to `main` first. The `feature/rest-api` branch was created and pulled from `origin/main`. Flask routes were added and tested on that branch before merging into `main`. The Postman files, report and evidence are committed with the finished submission.

## References

- Lab5-Postman and APIs course handout.
- [Postman quick start](https://learning.postman.com/docs/getting-started/quick-start/)
- [Sending requests](https://learning.postman.com/docs/use/send-requests/requests/)
