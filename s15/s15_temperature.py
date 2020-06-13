import arcpy
arcpy.env.overwriteOutput = True

cities = r"E:\programin\semestr2\samrob\s15_GIS_FILE\Programming_in_GIS_2020_L9_s15\us_cities1.shp"
inpraster = r"E:\programin\semestr2\samrob\s15_GIS_FILE\Programming_in_GIS_2020_L9_s15\us.tmax_nohads_ll_20140525_float.tif"
clipzone = r"E:\programin\semestr2\samrob\s15_GIS_FILE\Programming_in_GIS_2020_L9_s15\us_boundaries1.shp"
resultdirec = r"E:\programin\semestr2\samrob\s15_GIS_FILE\Programming_in_GIS_2020_L9_s15\Results"
popsize = 3
arcpy.env.workspace = resultdirec
#create file with selection
arcpy.MakeFeatureLayer_management(cities, "layercities", "POPCLASS >= " + str(popsize))
arcpy.CopyFeatures_management("layercities", "us_cities_level_{}.shp".format(str(popsize)))
arcpy.AddMessage("Created a file with a selection of where 'us_cities_level_{}.shp'".format(str(popsize)))

# reproject and clip by mask(polygon)
arcpy.ProjectRaster_management(inpraster, "reproject_US_raster_temperature.tif", cities, geographic_transform = "WGS_1984_(ITRF00)_To_NAD_1983")
clip = arcpy.sa.ExtractByMask("reproject_US_raster_temperature.tif", clipzone)
clip.save("reproject_US_raster_temperature_extract_by_mask.tif")
arcpy.AddMessage("Made reproject and cut to the desired area")