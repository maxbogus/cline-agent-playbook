.DEFAULT_GOAL := check
.PHONY: check status

check:
	@python3 scripts/check_repo.py

status:
	@git status --short
