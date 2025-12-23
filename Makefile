.PHONY: test smoke regression report

test:
	pytest -v

smoke:
	pytest -v -m smoke

regression:
	pytest -v -m regression

report:
	pytest -v api_tests --html=report.html --self-contained-html
