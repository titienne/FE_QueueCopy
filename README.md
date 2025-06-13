# Queue Copy GUI

This project is a small Python application built with PyQt6. It lets you queue file and folder copies with a persistent task list.

## Features

- Drag-and-drop area to select multiple files or folders to copy.
- Separate area for selecting the destination folder.
- Persistent queue stored in `~/.queue_copy_gui/tasks.json`, surviving restarts and crashes.
- Automatic resume of interrupted copies.
- Simple interface with a **Start Copy** button to process tasks sequentially.

## Installation

1. Clone this repository.
2. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main file:
```bash
python main.py
```
Drop your files or folders, then a destination folder. Tasks start when you press the button.

## Translations

The interface detects the user's system language by default. You can override it with the `APP_LANG` environment variable or via the **Language** menu in the application. Available languages are:

- French (`fr`)
- Spanish (`es`)
- Portuguese (`pt`)
- German (`de`)
- Dutch (`nl`)

Example to force French from the command line:
```bash
APP_LANG=fr python main.py
```

## Development

The project follows the SOLID principles and a Test Driven Development approach. Tests must be written with `pytest` inside the `tests/` directory.

Run the tests with:
```bash
pytest
```
All files must remain under **60 lines**, blank lines excluded. Use
`grep -v '^$' FILE | wc -l` to count lines. Ensure `pytest --cov=. -q` reports
100% coverage while respecting SOLID principles.

## License

This project is distributed under the GPLv3 license. See the `LICENSE` file for details.
