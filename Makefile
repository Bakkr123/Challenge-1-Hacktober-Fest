.PHONY: backend-install backend-test frontend-install frontend-build check

backend-install:
	python3 -m pip install -e './backend[dev]'

backend-test:
	cd backend && python3 -m pytest

frontend-install:
	cd frontend && npm install

frontend-build:
	cd frontend && npm run build

check: backend-test frontend-build
