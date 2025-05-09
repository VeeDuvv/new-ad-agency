# Show all files and directories

tree

# Exclude certain directories (like virtual environments)

tree -I "venv|.venv|.git|**pycache**"
tree -I "venv|.venv|.git|**pycache**|node*modules|*.pyc|_.pyo|_.pyd|_.so|_.dll|\_.class|dist|build|coverage|.pytest_cache|.coverage|.tox|.eggs|\*.egg-info|.DS_Store|.idea|.vscode"

# Limit to a specific depth

tree -L 2

# Show only directories

tree -d
