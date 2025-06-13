# Contributor Guidelines

This repository contains a PyQt6 application to copy files using a persistent queue.

## General Rules

- Follow the SOLID principles when modifying the code.
- Use a Test Driven Development approach: new behavior must come with an automated test.
- Tests should be written with `pytest` inside the `tests/` directory.
- Before each commit, run:
  ```bash
  python -m py_compile main.py
  pytest --cov=.
  ```
- Python code must comply with PEP8.
- Commit messages must be short and written in French.
- Keep every file under **60 lines**, excluding blank lines. Check with
  `grep -v '^$' FILE | wc -l` before committing.
- Ensure test coverage is 100%. If not, refactor and add tests respecting SOLID principles before committing.
