# GDAL TMS
# brew install gdal (macOS) | sudo apt-get install -y gdal-bin (Linux)
gdal2tiles.py -z 0-8 -r near -w none input_big.tif tiles/tms
