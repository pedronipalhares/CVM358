from pathlib import Path

def ensure_datasets_dir():
    """Create and return the datasets directory path."""
    datasets_dir = Path('datasets')
    datasets_dir.mkdir(exist_ok=True)
    return datasets_dir 