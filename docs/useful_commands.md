# Show all files and directories

tree

# Exclude certain directories (like virtual environments)

tree -I "venv|.venv|.git|**pycache**"

# Limit to a specific depth

tree -L 2

# Show only directories

tree -d
