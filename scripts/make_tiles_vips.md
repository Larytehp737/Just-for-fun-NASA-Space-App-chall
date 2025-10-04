# Deep Zoom avec libvips
brew install vips     # macOS
# sudo apt-get install -y libvips  # Linux
vips dzsave input_big.tif tiles/image --layout dz --suffix .png
# Résultat: tiles/image.dzi + tiles/image_files/
