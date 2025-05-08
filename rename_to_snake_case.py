import os
import re

folder = "images"

def camel_to_snake(name):
    name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    return name.lower()

for filename in os.listdir(folder):
    old_path = os.path.join(folder, filename)

    if os.path.isfile(old_path):
        name, ext = os.path.splitext(filename)
        new_name = camel_to_snake(name) + ext
        new_path = os.path.join(folder, new_name)

        if old_path != new_path:
            print(f'Renaming: {filename} -> {new_name}')
            os.rename(old_path, new_path)

print("✅ Renomeado com sucesso.")
