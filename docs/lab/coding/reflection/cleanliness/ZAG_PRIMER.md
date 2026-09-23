# Zag — compact primer for code generation

Zag is a small statically-typed language. Write idiomatic Zag, nothing else.

## Functions
```
fn name(a:i64, b:i64)i64 {
  return a+b;
}
fn main()void {
  ...
}
```
- Every program has `fn main()void`.
- Return type comes AFTER the parens: `fn f(x:i32)i32 { ... }`.
- Call: `name(3, 4)`.

## Types and locals
- `i64` (signed 64-bit int), `i32`, `u8` (byte), `[]u8` (byte slice), `[]i64`.
- Declare: `let x:i64=7;`  Assign: `x=8;`
- Cast: `x as i64`. Int to string: `_zag_i64_to_str(x)`.

## Control flow
```
while(cond){
  ...
}
if(a>b){
} else {
}
```
- Conditions are expressions: `i<10`, `y!=0`, `a==b`.
- `return x;` returns from a function.

## Strings and printing
- String literal: `"hello"`. Assign to a slice: `let s:[]u8="beekeeper";`
- There is no strlen: pass the length explicitly, e.g. `count_ch(s, 9, 101)`.
- Print: `_zag_print("text");`  Print int: `_zag_print(_zag_i64_to_str(n));`
- Newline: `_zag_print("\n");`
- Byte at index: `s[i]` (a u8). Compare bytes: `s[i]==101` (101 = 'e').

## Slices
- Fixed demo arrays are written inline, e.g.:
```
fn main()void {
  let n:i64=4;
  let a0:i64=9; let a1:i64=3; let a2:i64=7; let a3:i64=1;
  // bubble sort a0..a3 ascending, then print "1 3 7 9\n"
}
```
  Prefer individual locals over slice allocation for tiny fixed inputs.
- To print a space-separated list: print each number, then `" "`, and `"\n"` at the end.

## Slices (dynamic)
- Writable copy of a string: `let out:[]u8=_zag_strdup(s);` — returns a mutable
  []u8 of the same length. Write bytes: `out[i]=s[n-1-i];` (writes through a
  []u8 work; never write into a string literal — literals are read-only).
- Raw bytes: `let p:*u8=_zag_malloc(n) as *u8;` with `p[i]=v;` (only if needed).
- `_zag_print` takes a string literal or a []u8 — never a `*u8`.

## Rules
- No imports, no stdlib, no comments needed unless logic is non-obvious.
- Keep functions short, names descriptive, nesting shallow.
- The program must compile with `znc` and print EXACTLY the expected output.

## Example (complete program)
```
fn gcd(a:i64,b:i64)i64 {
  let x:i64=a;
  let y:i64=b;
  while(y!=0){
    let t:i64=x%y;
    x=y;
    y=t;
  }
  return x;
}
fn main()void {
  _zag_print(_zag_i64_to_str(gcd(1071,462)));
  _zag_print("\n");
}
```
This prints `21` followed by a newline.
