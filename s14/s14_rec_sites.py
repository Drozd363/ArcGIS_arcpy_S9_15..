import arcpy
arcpy.env.overwriteOutput = True

inputFc = arcpy.GetParameterAsText(0)           # rec_sites.shp
rasterElevation = arcpy.GetParameterAsText(1)      # elevation
resultFile = arcpy.GetParameterAsText(2)  # resultFile = "#"
newFields = arcpy.GetParameterAsText(3)   # newFields = '#'
#inputFc = r"E:\programin\semestr2\samrob\s14_GIS_FILE\Programming_in_GIS_2020_L9_s14\rec_sites.shp"
#rasterElevation = r"E:\programin\semestr2\samrob\s14_GIS_FILE\Programming_in_GIS_2020_L9_s14\elevation"
#resultFile = r"E:\programin\semestr2\samrob\s14_GIS_FILE\Programming_in_GIS_2020_L9_s14\rec_sites1.shp"
#newFields = 'HEIGHT'
if newFields == '#' or not newFields:
    newFields = 'HEIGHT'

# Changes occur in the input or a new file is created. Asked by the user
if resultFile == "#" or not resultFile:
    resultFile = inputFc
    arcpy.AddMessage("Changes occur in the input file")
else:
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
        height.append(evel.getOutput(0))
arcpy.AddMessage("The values of heights by coordinates are determined")

# new Field
arcpy.AddField_management(resultFile, newFields, "SHORT")
with arcpy.da.UpdateCursor(resultFile, newFields) as cursor:
    i = 0
    for row in cursor:
        row[0] = height[i]
        cursor.updateRow(row)
        i += 1
arcpy.AddMessage("Created {} field and height data is recorded".format(newFields))
