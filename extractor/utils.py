from pathlib import Path

def ensure_datasets_dir():
    """Create and return the datasets directory path."""
    # Get the project root directory (parent of the extractor directory)
    project_root = Path(__file__).parent.parent
    datasets_dir = project_root / 'datasets'
    datasets_dir.mkdir(exist_ok=True)
    return datasets_dir 