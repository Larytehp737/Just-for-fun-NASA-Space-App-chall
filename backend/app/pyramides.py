import pyvips

def generate_deepzoom(input_path, output_basename, tile_size=256, overlap=0, suffix=".jpg"):
    # Charger l'image source
    image = pyvips.Image.new_from_file(input_path, access="sequential")
    
    # Sauvegarder en DeepZoom
    image.dzsave(output_basename, tile_size=tile_size, overlap=overlap, suffix=suffix)


## Exemple d'utilisation
#if __name__ == "__main__":
    ## Donne ton image en entrée
    #input_image = "./nasa_test.jpg"

    ## Nom de sortie (sans extension)
    #output_name = "output/slide"
    #generate_deepzoom(input_image, output_name, tile_size=256, suffix=".jpg")
