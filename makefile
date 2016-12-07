make: memer.py
	#top wheat kex

run: make
	python app.py

clean:
	rm -f *~
	rm -f *.db
