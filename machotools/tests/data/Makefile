default: main foo.dylib foo2.dylib foo_rpath.dylib bar.1.0.0.dylib bar.2.0.0.dylib

main: bar.1.0.0.dylib src/main.c
	$(CC) src/main.c -o $@ bar.1.0.0.dylib

foo.dylib: src/foo.c
	$(CC) $< -o $@ -shared -install_name $@

foo2.dylib: src/foo.c
	$(CC) $< -o $@ -shared -install_name yoyo.dylib

foo_rpath.dylib: src/foo.c
	$(CC) $< -o $@ -shared -install_name $@
	install_name_tool -add_rpath @loader_path/../lib $@

bar.1.0.0.dylib: src/bar.c
	$(CC) -DBAR_VERSION=1 $< -o $@ -shared -install_name $@

bar.2.0.0.dylib: src/bar.c
	$(CC) -DBAR_VERSION=2 $< -o $@ -shared -install_name $@

foo.bundle: src/bar.c
	$(CC) $< -o $@ -bundle

clean:
	rm -f *.dylib
	rm -f main
