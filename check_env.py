import sys

for p in ['numpy', 'scipy', 'sklearn', 'torch', 'transformers', 'datasets', 'joblib']:
    try:
        m = __import__(p)
        ver = getattr(m, '__version__', 'installed')
        print(f"{p}: {ver}")
    except ImportError:
        print(f"{p}: NOT installed")
