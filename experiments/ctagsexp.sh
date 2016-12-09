#ctags testHeader.h --regex="/^[ \t]*(export)?[ \t]*enum[ \t]+([a-zA-Z0-9_]+)/\2/e,enums/" --output=ctagoutput

ctags testHeader.h --regex="/^[ \t]*(export)?[ \t]*enum[ \t]+([a-zA-Z0-9_]+)/\2/e,enums/" --output=ctagoutput
cat ctagoutput