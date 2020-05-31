import arcpy
arcpy.env.overwriteOutput = True
folderforgdb = r"E:\programin\semestr2\samrob\s12_GIS_FILE"
datapoints = r"E:\programin\semestr2\samrob\s12_GIS_FILE\Programming_in_GIS_2020_L7_s12\OSMpoints.shp"
clipzon = r"E:\programin\semestr2\samrob\s12_GIS_FILE\Programming_in_GIS_2020_L7_s12\CentralAmerica.shp"
nameGDB = 'salvador'
arcpy.CreateFileGDB_management(folderforgdb, nameGDB + '.gdb')
arcpy.AddMessage('Created new File GDB: {}.gdb'.format(nameGDB))
arcpy.env.workspace = folderforgdb + "\\" + nameGDB + '.gdb'
amenities = ['school', 'hospital', 'place_of_worship']
country = 'El Salvador'
arcpy.MakeFeatureLayer_management(clipzon, 'zoneclip', '"NAME" = ' + "'"+country + "'")
arcpy.Clip_analysis(datapoints, 'zoneclip', 'clipshp')
arcpy.AddMessage('Objects are cut for a given area ({})'.format(country))
for i in amenities:
    arcpy.MakeFeatureLayer_management('clipshp', 'clip', '"amenity" = ' + "'" + i + "'")
    arcpy.CopyFeatures_management('clip', 'zones_' + i)
    arcpy.AddField_management('zones_' + i, 'source', 'TEXT')
    arcpy.AddField_management('zones_' + i, 'GID', 'DOUBLE')
    with arcpy.da.UpdateCursor('zones_' + i, ['source', 'GID', 'id']) as cursor:
        for row in cursor:
            row[1] = row[2]
            row[0] = "OpenStreetMap"
            cursor.updateRow(row)
    arcpy.AddMessage('Created file for location '+i)
arcpy.Delete_management('clipshp')