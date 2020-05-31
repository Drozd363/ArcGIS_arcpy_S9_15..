import arcpy
arcpy.env.overwriteOutput = True
folderforgdb = r'E:\programin\semestr2\samrob\s12_GIS_FILE'
datapoints = r"E:\programin\semestr2\samrob\s12_GIS_FILE\Programming_in_GIS_2020_L7_s12\OSMpoints.shp"
clipzon = r"E:\programin\semestr2\samrob\s12_GIS_FILE\Programming_in_GIS_2020_L7_s12\CentralAmerica.shp"
nameGDB = 'salvador'
arcpy.CreateFileGDB_management(folderforgdb, nameGDB + '.gdb')
arcpy.env.workspace = folderforgdb + "\\" + nameGDB + '.gdb'
amenities = ['school', 'hospital', 'place_of_worship']
country = 'El Salvador'
arcpy.MakeFeatureLayer_management(clipzon, 'zoneclip', '"NAME" = ' + "'"+country +"'")
arcpy.Clip_analysis(datapoints, 'zoneclip', 'clip.shp')

