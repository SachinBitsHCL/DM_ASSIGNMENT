from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'
FEATURES_DIR = DATA_DIR / 'features'
ERRORS_DIR = DATA_DIR / 'errors'
REPORTS_DIR = ROOT / 'reports'
MODELS_DIR = ROOT / 'models'
DOCS_DIR = ROOT / 'docs'
