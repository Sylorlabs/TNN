#!/usr/bin/env python3
"""Build the frozen Task-4 prior-art corpus entries.txt from templates.

Each entry: @<id>, T:<title>, K:<keywords>, body (// description + template
with {{SLOTS}}), @end. No frozen expected outputs appear anywhere.
"""
import os

T4 = os.path.expanduser("~/workspace/tnn-lab/coding/reflection/task4")
TPL = os.path.join(T4, "corpus", "templates")

ENTRIES = [
    {
        "id": "E-HUFFMAN",
        "title": "Prior art: byte-alphabet Huffman codec",
        "kw": "huffman,codec,compress,decompress,prefix,tree,encode,decode,bitstream",
        "tpl": "b1_huffman.zag",
        "desc": [
            "Prior art: byte-alphabet Huffman codec (human-written template).",
            "How it works: count symbol frequencies over the input; build the code",
            "tree by repeatedly joining the two lightest nodes, breaking ties by",
            "smallest symbol so the build is deterministic; read code lengths by",
            "depth-first walk (a lone symbol gets code \"0\"); pack code bits MSB-first;",
            "decode by walking the tree bit by bit. I/O: huff rt <hexbytes> prints",
            "nbits, the bitstream as hex, and the decoded bytes as hex.",
            "Slots: {{ALPHABET}} = alphabet size (byte alphabet: 256).",
        ],
    },
    {
        "id": "E-SQL",
        "title": "Prior art: tiny SQL engine over CSV tables",
        "kw": "sql,engine,select,where,join,query,csv,table",
        "tpl": "b2_sql.zag",
        "desc": [
            "Prior art: tiny SQL engine over CSV tables (human-written template).",
            "How it works: load each CSV into typed columns (a column is integer iff",
            "every value parses as an integer; raw text is kept for byte-exact output);",
            "tokenize the query respecting single quotes; parse SELECT list, FROM,",
            "optional JOIN..ON equality, optional WHERE with ANDed comparisons",
            "(=,!=,<,>,<=,>=; integer compare on int columns else byte-wise), optional",
            "ORDER BY with a stable insertion sort; nested-loop join. I/O:",
            "sql <dbdir> \"<query>\" prints a header line then |-separated rows.",
            "Slots: none (table paths arrive via argv).",
        ],
    },
    {
        "id": "E-PEEPHOLE",
        "title": "Prior art: peephole optimizer for a stack VM",
        "kw": "peephole,optimizer,stack,vm,instruction,fold",
        "tpl": "b3_peephole.zag",
        "desc": [
            "Prior art: peephole optimizer for a stack VM (human-written template).",
            "How it works: parse the text program into ops; repeatedly scan and apply",
            "local rewrites until fixpoint: fold PUSH a,PUSH b,OP into PUSH (a OP b)",
            "for ADD/SUB/MUL/DIV (no DIV-by-zero in scope); PUSH 0,ADD -> x;",
            "PUSH 1,MUL -> x; DUP,POP -> x; PUSH a,NEG -> PUSH -a;",
            "PUSH a,PUSH a,SUB -> PUSH 0. Every rewrite preserves stack semantics by",
            "construction. I/O: peep <progfile> prints the optimized program.",
            "Slots: {{MAXOPS}} = op arena capacity (4096).",
        ],
    },
    {
        "id": "E-BTREE",
        "title": "Prior art: order-4 B-tree with split and merge",
        "kw": "btree,b-tree,split,merge,insert,delete",
        "tpl": "b4_btree.zag",
        "desc": [
            "Prior art: order-4 B-tree with split and merge (human-written template).",
            "How it works: nodes hold up to ORDER-1 sorted keys; insert splits full",
            "children on the way down around the median; delete borrows from a sibling",
            "with enough keys or merges, and shrinks the root when it empties; merged",
            "or abandoned nodes are flagged dead and skipped at print. I/O:",
            "btree <opsfile> with ops 'i <k>' insert, 'd <k>' delete (absent key is a",
            "no-op), 'p' print; print shows one line per live node plus ROOT <id>.",
            "Slots: {{ORDER}} = B-tree order (4).",
        ],
    },
    {
        "id": "E-SNAKE",
        "title": "Prior art: playable snake game",
        "kw": "snake,game,grid,moves,food,collision",
        "tpl": "b5_snake.zag",
        "desc": [
            "Prior art: playable snake game (human-written template).",
            "How it works: the body is a head-first list of grid cells; food positions",
            "arrive as a fixed script; each move steps the head, eating grows the body",
            "by one and advances the score and the food script; hitting a wall ends",
            "the run as DEAD_WALL, hitting the body (tail cell excluded when not",
            "growing) ends it as DEAD_SELF. I/O: snake <moves> <foodlist> prints",
            "BOARD, SNAKE, FOOD, SCORE, STATUS lines for the final state.",
            "Slots: {{W}} = grid width (10), {{H}} = grid height (8).",
        ],
    },
]

def main():
    out_lines = []
    for e in ENTRIES:
        tpl = open(os.path.join(TPL, e["tpl"])).read()
        assert "@end" not in tpl.split("\n"), "template contains @end"
        if "{{" not in tpl:
            print("note: template", e["tpl"], "has no {{slots}}")
        out_lines.append("@" + e["id"])
        out_lines.append("T:" + e["title"])
        out_lines.append("K:" + e["kw"])
        for d in e["desc"]:
            out_lines.append("// " + d)
        out_lines.extend(tpl.split("\n"))
        out_lines.append("@end")
    # kb_install treats a trailing newline fine; ensure file ends with newline
    text = "\n".join(out_lines) + "\n"
    dest = os.path.join(T4, "corpus", "entries.txt")
    open(dest, "w").write(text)
    print("wrote", dest, len(text), "bytes", len(ENTRIES), "entries")

if __name__ == "__main__":
    main()
