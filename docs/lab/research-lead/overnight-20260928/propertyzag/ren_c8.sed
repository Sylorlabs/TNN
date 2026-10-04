s/(^|[^A-Za-z0-9_])z_alloc([^A-Za-z0-9_]|$)/\1z8_alloc\2/g
s/(^|[^A-Za-z0-9_])get32([^A-Za-z0-9_]|$)/\1z8_get32\2/g
s/(^|[^A-Za-z0-9_])set32([^A-Za-z0-9_]|$)/\1z8_set32\2/g
s/(^|[^A-Za-z0-9_])main([^A-Za-z0-9_]|$)/\1z8_main\2/g
