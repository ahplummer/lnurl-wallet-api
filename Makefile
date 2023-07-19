.PHONY: default
default: displayhelp ;

displayhelp:
	@echo Use "tests, runlocal, or run" with make, pretty please...

tests:
	@echo Running Coverage output
	cd src; python -m unittest discover; cd ..;

runlocal:
	@echo Running locally
	python src/flaskdriver.py

run:
	@echo Docker things
	docker build -t lnurl-wallet .
	docker run -it -e users=${users} -p 8511:8511 lnurl-wallet