def generate_deepzoom(input_path, output_basename, tile_size=32, overlap=0, suffix=".jpg"):
    # Import paresseux pour éviter d'imposer pyvips si non utilisé au runtime
    try:
        import pyvips  # type: ignore
    except Exception as e:
        raise RuntimeError("pyvips est requis pour la génération de tuiles DZI. Veuillez installer libvips et pyvips.") from e

    image = pyvips.Image.new_from_file(input_path, access="sequential")
    image.dzsave(output_basename, tile_size=tile_size, overlap=overlap, suffix=suffix)


#if __name__ == "__main__":
    #input_image = "backend/data/sydneyflooding_oli.jpg"
    #output_name = "output/slide"
    #generate_deepzoom(input_image, output_name, tile_size=256, suffix=".jpg")
