from PIL import Image

def compress_tile(input_path, output_path, quality=75):
    """
    Compress the image tile before saving it.
    """
    img = Image.open(input_path)
    img.save(output_path, format="PNG", quality=quality)

def compress_all_tiles(directory="tiles"):
    """
    Compress all tiles in the given directory.
    """
    for tile_file in os.listdir(directory):
        input_path = os.path.join(directory, tile_file)
        output_path = os.path.join(directory, f"compressed_{tile_file}")
        compress_tile(input_path, output_path)
