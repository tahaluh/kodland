import os
from PIL import Image, ImageOps

folder_path = './images'

image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')

output_path = os.path.join(folder_path, 'mirrored')
os.makedirs(output_path, exist_ok=True)

for filename in os.listdir(folder_path):
    if filename.lower().endswith(image_extensions):
        full_path = os.path.join(folder_path, filename)
        image = Image.open(full_path)

        mirrored = ImageOps.mirror(image)

        new_filename = f"{os.path.splitext(filename)[0]}_flipped{os.path.splitext(filename)[1]}"
        mirrored.save(os.path.join(output_path, new_filename))

        print(f"Espelhado: {filename} → {new_filename}")

print("✅ Todas as imagens foram espelhadas com sucesso.")
