import re
import sys

path = sys.argv[1]
items = {}
with open(path, encoding='euc-jp') as f:
    for line in f:
        # コメント行なのでスキップ
        if line.startswith(';'):
            continue
        line = line.strip()

        sepIndex = line.find(' ')
        key = line[:sepIndex]
        value = line[sepIndex+1:]

        # 特殊なキーはスキップ
        if key.startswith('<') or key.startswith('>') or key.startswith('?'):
            continue
        if key.endswith('<') or key.endswith('>') or key.endswith('?'):
            continue

        # 数字拡張が存在すればスキップ
        if '#' in key:
            continue

        # 送り仮名を削除
        if re.search(r'[a-z]$', key) != None:
            key = key[:-1]
    
        for word in value.split('/'):
            annoIndex = word.find(';')
            if annoIndex >= 0:
                word = word[:annoIndex]
            if len(word) == 0:
                continue
            old_values = items.get(key)
            if old_values == None:
                items[key] = [word]
            else:
                old_values.append(word)

if len(sys.argv) >= 3:
    with open(sys.argv[2], encoding='utf-8', mode='w') as f:
        keys = sorted(items.keys())
        keys = sorted(keys, reverse=True, key=lambda x: len(x))
        for k in keys:
            if k == '':
                continue
            v = items[k]
            #print(k, v)
            values = set(v)
            f.write(k + '\t' + '\t'.join(sorted(list(values))) + '\n')

