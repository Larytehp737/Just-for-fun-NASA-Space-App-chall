import pyvips

def split_image_into_tiles(image_path, tile_size=(256, 256), output_dir="tiles"):
    """
    Split an image into smaller tiles and save them to the output directory.
    Each tile will be of size 'tile_size' (default: 256x256).
    """
    image = pyvips.Image.new_from_file(image_path)

    # Define the size of the output tiles
    width, height = image.width, image.height
    tile_width, tile_height = tile_size

    tiles = []

    for y in range(0, height, tile_height):
        for x in range(0, width, tile_width):
            # Crop the image to create a tile
            tile = image.crop(x, y, tile_width, tile_height)
            tile_filename = f"{output_dir}/tile_{x}_{y}.png"
            tile.write_to_file(tile_filename)
            tiles.append(tile_filename)

    return tiles
