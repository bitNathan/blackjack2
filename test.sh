# test.sh
#!/bin/bash
PYTHONPATH=. pytest --cov=app "$@"
