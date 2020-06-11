import arcpy
arcpy.env.overwriteOutput = True

inputFc = r"E:\programin\semestr2\samrob\s14_GIS_FILE\Programming_in_GIS_2020_L9_s14\rec_sites.shp"
rasterElevation = r"E:\programin\semestr2\samrob\s14_GIS_FILE\Programming_in_GIS_2020_L9_s14\elevation"
resultFile = r"E:\programin\semestr2\samrob\s14_GIS_FILE\Programming_in_GIS_2020_L9_s14\rec_sites1.shp"
newFields = 'HEIGHT'

# created result file
arcpy.CopyFeatures_management(inputFc, resultFile)
arcpy.AddMessage("A new file has been created with changes")
# check coordinate systems for coincidence
if arcpy.Describe(resultFile).spatialReference.name == arcpy.Describe(rasterElevation).spatialReference.name:
    arcpy.AddMessage("Coordinate systems coincide")
else:
    proj = arcpy.Describe(rasterElevation).spatialReference.name
    arcpy.Project_management(resultFile, resultFile, proj)
    arcpy.AddMessage("The coordinate systems did not match. Reprojected")
# determine the value of heights in the specified coordinates
height = []
with arcpy.da.SearchCursor(resultFile, 'SHAPE@XY') as cursor:
    for row in cursor:
        evel = arcpy.GetCellValue_management(rasterElevation, str(row[0][0])+' '+str(row[0][1]))
        height.append(evel)
arcpy.AddMessage("The values of heights by coordinates are determined")



