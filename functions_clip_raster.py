
import os
from osgeo import gdal, ogr
#import gdal
#import ogr

################################################################################

def create_clip_polys(inPath, field, folder_path):

    driverSHP = ogr.GetDriverByName('ESRI Shapefile')
    ds = driverSHP.Open(inPath)

    if ds is None:
        print('layer not open')

    lyr = ds.GetLayer()
    spatialRef = lyr.GetSpatialRef()

#    schema = []
#    ldefn = lyr.GetLayerDefn()
#    for n in range(ldefn.GetFieldCount()):
#        fdefn = ldefn.GetFieldDefn(n)
#        print(fdefn.name)

    for feature in lyr:

        fieldVal = feature.GetField(field)

        os.mkdir(folder_path+'/' + str(fieldVal))

        outds = driverSHP.CreateDataSource(folder_path+'/'+str(fieldVal)+'/clip.shp')

        outlyr = outds.CreateLayer(str(fieldVal)+'/clip.shp',
                                    srs=spatialRef,
                                    geom_type=ogr.wkbPolygon)

        outDfn = outlyr.GetLayerDefn()
        ingeom = feature.GetGeometryRef()
        outFeat = ogr.Feature(outDfn)
        outFeat.SetGeometry(ingeom)
        outlyr.CreateFeature(outFeat)

#-of GTiff 
def clip_command(raster_path, poly_path, out_path):

    os.system('gdalwarp -dstnodata -9999 -q -ot Int16 -cutline ' + poly_path + ' -crop_to_cutline' + ' ' + raster_path + ' ' + out_path)

def clip_raster(inPath, field, raster_path, folder_path):
    
    driverSHP = ogr.GetDriverByName('ESRI Shapefile')
    ds = driverSHP.Open(inPath)
    if ds is None:
        print('layer not open')
    lyr = ds.GetLayer()

    for feature in lyr:
        fieldVal = feature.GetField(field)
        print(fieldVal)
        clip_command(raster_path,
                folder_path+'/'+str(fieldVal),
                folder_path+'/'+str(fieldVal)+'/dem.tif')

def clip_raster_with_poly(shp_path, field, raster_path, folder_path):

    os.mkdir(folder_path)

    #primero los shp
    create_clip_polys(shp_path,
            field,
            folder_path)

    #ahora los raster
    clip_raster(shp_path,
            field,
            raster_path,
            folder_path)
