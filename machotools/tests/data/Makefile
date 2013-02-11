foo.dylib: src/foo.c
	$(CC) $< -o $@ -shared -install_name $@

foo2.dylib: src/foo.c
	$(CC) $< -o $@ -shared -install_name yoyo.dylib

clean:
	rm -f *.dylib
