import json
seen = set()
out = []
with open('training_items.jsonl') as f:
    for line in f:
        it = json.loads(line)
        if it['id'] in seen:
            print('Skipping duplicate:', it['id'])
            continue
        seen.add(it['id'])
        out.append(line)
with open('training_items.jsonl', 'w') as f:
    f.writelines(out)
print('Wrote', len(out), 'unique items')
