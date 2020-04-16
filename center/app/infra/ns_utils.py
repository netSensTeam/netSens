import os

def getPackages(dir, includePrivates=False):
    names = os.listdir(dir)
    for name in names:
        if name[0] == '_' and not includePrivates:
            continue
        name_parts = os.path.basename(name).split('.')
        if len(name_parts) > 1 and name_parts[1] != 'py':
            continue
        yield name_parts[0]