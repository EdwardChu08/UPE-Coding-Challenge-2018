init:
	pip3 install -r requirements.txt
clean:
	rm -f logs/*.log
	rm -f *.pyc
	rm -rf __pycache__