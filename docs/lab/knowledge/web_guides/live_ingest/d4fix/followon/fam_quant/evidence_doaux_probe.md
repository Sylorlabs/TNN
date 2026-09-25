# Do-auxiliary alert verification — key dumps (2026-09-24, qdbg_bin, frozen spec, no fixes)
# Parent alert sentence is NOT in FAM-QUANT battery; verified by grep (only need.txt query strings contain does/did).

## q-1 (frozen)
TK1|last||wrote,report,last|A||every|chapter,elena,every,harbor,marsh|winter
PK1|write||elena,marsh|chapter,every,harbor,winter|A|chapter,elena,every,harbor,marsh,winter|elena,marsh|chapter,every,harbor,winter||every
TK2|last||wrote,report,last|A||one|chapter,elena,harbor,marsh,one|winter
PK2|write||elena,marsh|chapter,harbor,one,winter|A|chapter,elena,harbor,marsh,one,winter|elena,marsh|chapter,harbor,one,winter||one
CONTRA|6

## q-2 (frozen)
TK1|
PK1|
TK2|
PK2|
CONTRA|0

## q-3 (frozen)
TK1|last||used,last|A||many|boats,many,new,pier|summer
PK1|use||boats,many|new,pier,summer|A|boats,many,new,pier,summer|boats,many|new,pier,summer||many
TK2|last||used,last|A||few|boats,few,new,pier|summer
PK2|use||boats,few|new,pier,summer|A|boats,few,new,pier,summer|boats,few|new,pier,summer||few
CONTRA|6

## q-4 (frozen)
TK1|keep||keeps|A||all|archive|all,charts,original
PK1|keep||archive|all,charts,original|A|all,archive,charts,original|archive|all,charts,original||all
TK2|keep||keeps|A|1||archive|charts,original
PK2|keep||archive|charts,original|A|archive,charts,original|archive|charts,original|1|
CONTRA|6

## parent hypothetical (NOT in battery — root-cause reproduction)
TK1|hold||holds|A||one|vault|ledger,north,one,wing
PK1|hold||vault|ledger,north,one,wing|A|ledger,north,one,vault,wing|vault|ledger,north,one,wing||one
TK2|hold||does,hold|A|1|one|vault|ledger,north,one,wing
PK2|do||vault|ledger,north,one,wing|A|ledger,north,one,vault,wing|vault|ledger,north,one,wing|1|one
CONTRA|0
