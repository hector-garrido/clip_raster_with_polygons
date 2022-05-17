import os
from dotenv import load_dotenv

from functions_clip_raster import clip_raster_with_poly

################################################################################

load_dotenv()

shp_path = os.getenv('SHP_PATH')
field = os.getenv('FIELD')
raster_path = os.getenv('RASTER_PATH')
folder_path = os.getenv('FOLDER_PATH')

################################################################################

#os.mkdir('clipped_raster_files')

clip_raster_with_poly(shp_path, field, raster_path, folder_path)