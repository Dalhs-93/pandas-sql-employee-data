# Setup

To set up this repo you will need to have uv installed, you can install uv by running `pip install uv`.
uv will manage the dependencies for you.

Navigate to the root directory of the repo and run:
```bash
uv sync
uv pip install -e .
uv pip install -e ".[dev]"
```
If `uv` is not recognised then go to the Troubleshooting section below.

Then you can run:
```bash
uv run python scripts/sql_db.py # This will create the database and populate it with the data from the csv file
uv run python scripts/data_quality_eval.py # Q1 produces a csv file with the output data in data/script_output
uv run python scripts/data_gov_access_control.py # Q2 produces a csv file with the output data in data/script_output
uv run python scripts/data_cleaning.py # Q3 produces a csv file with the output data in data/script_output
uv run python scripts/data_lineage_logging.py # Q4 produces a log file with the output data in data/script_output
uv run pytest
```

which creates a csv or log file with the output data for each script.

# General notes

I am using uv for package management as it has detailed dependency resolution, is faster, and less verbose than pip.

Finally, I created a tests directory. Pytests can be run for the Python scripts by running `uv run pytest`, see the README.md in the tests dir for more details.

If you have any issues setting this up please let me know benldale93@gmail.com.

### Troubleshooting: If `uv` is not recognised

If you get a "command not found" or "not recognized" error after installing `uv`, you need to add it to your PATH:

**Windows (PowerShell):**
```powershell
# Find where uv was installed
python -m site --user-base

# Add the Scripts directory to your PATH (replace <USER_BASE> with the path from above)
setx PATH "$Env:PATH;<USER_BASE>\Scripts"

# Restart your terminal for changes to take effect
```

**macOS/Linux:**
```bash
# Add to your shell profile (~/.zshrc for macOS, ~/.bashrc for Linux)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# Reload your shell configuration
source ~/.zshrc
```

After updating your PATH, restart your terminal and try running `uv sync` again.

Navigate to the root directory of the repo and run:
```bash
pip install -r requirements.txt
pip install -e .
pip install -e ".[dev]"
```

Then you can run the scripts without the `uv run` prefix:
```bash
python scripts/sql_db.py # This will create the database and populate it with the data from the csv file
python scripts/data_quality_eval.py # Q1 produces a csv file with the output data in data/script_output
python scripts/data_gov_access_control.py # Q2 produces a csv file with the output data in data/script_output
python scripts/data_cleaning.py # Q3 produces a csv file with the output data in data/script_output
python scripts/data_lineage_logging.py # Q4 produces a log file with the output data in data/script_output
python -m pytest
```
