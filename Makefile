install:
	install ./minceware.py /usr/local/bin/minceware
	install -m 0644 -D ./README.rst /usr/local/share/doc/minceware/README.rst

uninstall:
	rm -f /usr/local/bin/minceware
	rm -rf /usr/local/share/doc/minceware

doc: README.html

README.html: README.rst
	rst2html ./README.rst ./README.html

doc-clean:
	rm -f ./README.html
