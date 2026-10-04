s/(^|[^A-Za-z0-9_])z_alloc([^A-Za-z0-9_]|$)/\1z2_alloc\2/g
s/(^|[^A-Za-z0-9_])get32([^A-Za-z0-9_]|$)/\1z2_get32\2/g
s/(^|[^A-Za-z0-9_])set32([^A-Za-z0-9_]|$)/\1z2_set32\2/g
s/(^|[^A-Za-z0-9_])emit([^A-Za-z0-9_]|$)/\1z2_emit\2/g
s/(^|[^A-Za-z0-9_])i64s([^A-Za-z0-9_]|$)/\1z2_i64s\2/g
s/(^|[^A-Za-z0-9_])e64([^A-Za-z0-9_]|$)/\1z2_e64\2/g
s/(^|[^A-Za-z0-9_])main([^A-Za-z0-9_]|$)/\1z2_main\2/g
