default: foo.dylib foo2.dylib foo_rpath.dylib

foo.dylib: src/foo.c
	$(CC) $< -o $@ -shared -install_name $@

foo2.dylib: src/foo.c
	$(CC) $< -o $@ -shared -install_name yoyo.dylib

foo_rpath.dylib: src/foo.c
	$(CC) $< -o $@ -shared -install_name $@
	install_name_tool -add_rpath @loader_path/../lib $@

clean:
	rm -f *.dylib
