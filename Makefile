VIRTUAL = . env/bin/activate &&

setup:
	virtualenv env
	$(VIRTUAL) pip install -r requirements.txt
.PHONY: setup

clean:
	rm -rf env/
.PHONY: clean
