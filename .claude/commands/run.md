Run a Python file or Jupyter notebook and show the output.

Steps:
1. If a file path is given, run it with `python <path>`
2. If no file is specified, find the most recently modified .py file and run it
3. Show the full output including any printed results
4. If matplotlib plots are generated, they will be saved as PNG files — read and display them
5. If there are errors, diagnose and fix them automatically
6. For Jupyter notebooks: use the IDE's notebook execution tools

For Docker execution (if local Python has issues):
```
docker compose run python <filepath>
```
