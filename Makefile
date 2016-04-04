# Cleans out the bytecode files
squeaky-clean: clean
	rm *.pyc

# Cleans out the folder but keeps the .pyc bytecode files
# This makes it faster the next time you run
clean:
	rm *~ *.ppm
