s/(^|[^A-Za-z0-9_])z2_alloc([^A-Za-z0-9_]|$)/\1z_alloc\2/g
s/(^|[^A-Za-z0-9_])z2_get32([^A-Za-z0-9_]|$)/\1get32\2/g
s/(^|[^A-Za-z0-9_])z2_set32([^A-Za-z0-9_]|$)/\1set32\2/g
s/(^|[^A-Za-z0-9_])z2_emit([^A-Za-z0-9_]|$)/\1emit\2/g
s/(^|[^A-Za-z0-9_])z2_i64s([^A-Za-z0-9_]|$)/\1i64s\2/g
s/(^|[^A-Za-z0-9_])z2_e64([^A-Za-z0-9_]|$)/\1e64\2/g
s/(^|[^A-Za-z0-9_])z2_main([^A-Za-z0-9_]|$)/\1main\2/g
