from pathlib import Path
import base64
import gzip
import hashlib

ROOT = Path('.')
TRANSPORT = ROOT / 'Research' / 'R32_E51AE_NATIVE' / 'transport'
OUT = ROOT / '.scratch' / 'e51ae_recovery'
OUT.mkdir(parents=True, exist_ok=True)

EXPECTED_FRAGMENT_SHA256 = '311b85839c81b8921b365012b467d4a3d36fd4a06c60d2e815067022d3049a5d'

names = [
    'E51AE_FRAGMENT.zag.gz.b64.part-00',
    'E51AE_FRAGMENT.zag.gz.b64.part-01',
    'E51AE_FRAGMENT.zag.gz.b64.part-02',
    'E51AE_FRAGMENT.zag.gz.b64.part-03',
    'E51AE_FRAGMENT.zag.gz.b64.part-031',
    'E51AE_FRAGMENT.zag.gz.b64.part-032',
    'E51AE_FRAGMENT.zag.gz.b64.part-033',
    'E51AE_FRAGMENT.zag.gz.b64.part-04',
]

part03 = ''.join((TRANSPORT / names[3]).read_text().split())
part030 = ''.join((TRANSPORT / 'E51AE_FRAGMENT.zag.gz.b64.part-030').read_text().split())
assert part03 == part030, 'part-03/part-030 recovery duplicate mismatch'

compressed_parts = []
for name in names:
    path = TRANSPORT / name
    assert path.exists(), name
    encoded = ''.join(path.read_text().split())
    compressed_parts.append(base64.b64decode(encoded, validate=True))

compressed = b''.join(compressed_parts)
fragment = gzip.decompress(compressed)
sha = hashlib.sha256(fragment).hexdigest()
assert sha == EXPECTED_FRAGMENT_SHA256, (sha, EXPECTED_FRAGMENT_SHA256)

out = OUT / 'E51AE_FRAGMENT.zag'
out.write_bytes(fragment)
print(f'e51ae_recovery_fragment_sha256,{sha}')
print(f'e51ae_recovery_fragment_bytes,{len(fragment)}')
print('e51ae_recovery_parts,' + ';'.join(names))
print('e51ae_recovery_duplicate_03_030_gate,1')

text = fragment.decode('utf-8')
lines = text.splitlines()
print(f'e51ae_recovery_lines,{len(lines)}')
for idx, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped.startswith('const E51AE') or stripped.startswith('fn e51ae_') or 'e51ae_run(' in stripped or 'e51ae_standalone' in stripped:
        print(f'e51ae_source_symbol,{idx},{stripped}')
