VIRTUAL = . env/bin/activate &&

setup:
	virtualenv -p python3 env
	$(VIRTUAL) pip install -r requirements.txt
.PHONY: setup

clean:
	rm -rf env/
.PHONY: clean

env:
	$(VIRTUAL) /bin/bash
.PHONY: env

run:
	$(VIRTUAL) python tesla/server.py
.PHONY: run
