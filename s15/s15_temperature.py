import arcpy
import numpy as np
arcpy.env.overwriteOutput = True

cities = arcpy.GetParameterAsText(0)
inpraster = arcpy.GetParameterAsText(1)
clipzone = arcpy.GetParameterAsText(2)
resultdirec = arcpy.GetParameterAsText(3)
popsize = arcpy.GetParameterAsText(4)
#cities = r"E:\programin\semestr2\samrob\s15_GIS_FILE\Programming_in_GIS_2020_L9_s15\us_cities1.shp"
#inpraster = r"E:\programin\semestr2\samrob\s15_GIS_FILE\Programming_in_GIS_2020_L9_s15\us.tmax_nohads_ll_20140525_float.tif"
#clipzone = r"E:\programin\semestr2\samrob\s15_GIS_FILE\Programming_in_GIS_2020_L9_s15\us_boundaries1.shp"
#resultdirec = r"E:\programin\semestr2\samrob\s15_GIS_FILE\Programming_in_GIS_2020_L9_s15\Results"
#popsize = 3
arcpy.env.workspace = resultdirec

# create file with selection
arcpy.MakeFeatureLayer_management(cities, "layercities", "POPCLASS >= " + str(popsize))
citiesSelect = "us_cities_level_{}.shp".format(str(popsize))
arcpy.CopyFeatures_management("layercities", citiesSelect)
arcpy.AddMessage("Created a file with a selection of where 'POPCLASS >= {}'".format(str(popsize)))

# reproject and clip by mask(polygon)
arcpy.ProjectRaster_management(inpraster, "reproject_US_raster_temperature.tif", cities, geographic_transform = "WGS_1984_(ITRF00)_To_NAD_1983")
clip = arcpy.sa.ExtractByMask("reproject_US_raster_temperature.tif", clipzone)
clip.save("reproject_US_raster_temperature_extract_by_mask.tif")
arcpy.AddMessage("Made reproject and cut to the desired area")

# Data from raster cells. If the data is missing, there will be an attempt to search for an uncut raster
cursor = arcpy.da.SearchCursor(citiesSelect, "SHAPE@XY")
try:
    temperature = []
    for row in cursor:
        temp = arcpy.GetCellValue_management("reproject_US_raster_temperature_extract_by_mask.tif", str(row[0][0])+' '+str(row[0][1]))
        temperature.append(float(temp.getOutput(0).replace(",", ".")))
    arcpy.AddMessage("Data from raster cells was found")
except ValueError:
    cursor.reset()
    temperature = []
    for row in cursor:
        temp = arcpy.GetCellValue_management("reproject_US_raster_temperature.tif", str(row[0][0])+' '+str(row[0][1]))
        temperature.append(float(temp.getOutput(0).replace(",", ".")))
    arcpy.AddMessage("While trimming the raster behind the mask, the required data cells were lost."
                     " Therefore, whole raster, not truncated raster, is used to search for data."
                     " Data from raster cells was found")

# Add new fields and update
arcpy.AddField_management(citiesSelect, "TEMPERATUR", 'FLOAT')
arcpy.AddField_management(citiesSelect, "EXCESS", 'FLOAT')
with arcpy.da.UpdateCursor(citiesSelect, ["TEMPERATUR", "EXCESS"]) as Ucursor:
    i = 0
    for row in Ucursor:
        row[0] = temperature[i]
        row[1] = row[0] - np.mean(temperature)
        Ucursor.updateRow(row)
        i += 1
arcpy.AddMessage('Added new fields and records added')







