import pyvips

def generate_deepzoom(input_path, output_basename, tile_size=32, overlap=0, suffix=".jpg"):

    image = pyvips.Image.new_from_file(input_path, access="sequential")
    image.dzsave(output_basename, tile_size=tile_size, overlap=overlap, suffix=suffix)


#if __name__ == "__main__":
    #input_image = "backend/data/sydneyflooding_oli.jpg"
    #output_name = "output/slide"
    #generate_deepzoom(input_image, output_name, tile_size=256, suffix=".jpg")
