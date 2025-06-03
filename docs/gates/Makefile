all: gates.html

%.html: %.md
	pandoc -t revealjs -s -o $@ $< --variable theme=sky -V revealjs-url=https://unpkg.com/reveal.js@5.2.0 
