import pandas as pd

def norm_gstin(s):
    if len(s) != 15:
        return s
    d_map = {'O':'0', 'I':'1', 'L':'1', 'l':'1', 'S':'5', 'B':'8', 'Z':'2'}
    a_map = {'0':'O', '1':'I', '5':'S', '8':'B', '2':'Z'}
    c = list(s.upper())
    for i in (0, 1):
        c[i] = d_map.get(c[i], c[i])
    for i in range(2, 7):
        c[i] = a_map.get(c[i], c[i])
    for i in range(7, 11):
        c[i] = d_map.get(c[i], c[i])
    c[11] = a_map.get(c[11], c[11])
    c[12] = d_map.get(c[12], c[12])
    c[13] = 'Z'
    return ''.join(c)

raws = [
    '371HKXV5167LIZS',
    '19EOGXH4115YIZL',
    '27XUIXG0767DIZP',
    '07CPCXN0398PIZT',
    '24XORXG9365MIZ3',
    '37LDYXK0296FIZB',
    '27QHJXK0658UIZL',
    '03KGZXT1320RIZZ'
]
df = pd.read_csv('udyam_digital_data/mock_gstin_registry.csv')
for r in raws:
    n = norm_gstin(r)
    m = df[df['gstin'] == n]
    status = m['status'].values[0] if len(m) else 'NOT FOUND'
    print(f'{r} -> {n} | Found: {len(m)} | Status: {status}')
