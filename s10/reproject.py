import arcpy
arcpy.env.overwriteOutput = True

arcpy.env.workspace = arcpy.GetParameterAsText(0)
input = arcpy.GetParameterAsText(1)
#arcpy.env.workspace = r"E:\programin\semestr2\samrob\S10_GIS_FILE"
#input = "CountyLines.shp"

inputSR = arcpy.Describe(input).SpatialReference
inputSRname = inputSR.name
arcpy.AddMessage("Coordinate systems will be changed to {}".format(inputSRname))
listfc = arcpy.ListFeatureClasses()
for fclas in listfc:
    clasSR = arcpy.Describe(fclas).SpatialReference
    clasSRname = clasSR.name
    if clasSRname != inputSRname:
        output = fclas[:-4] + "_projected.shp"
        arcpy.Project_management(fclas, output, inputSR)
        arcpy.AddMessage("The coordinate system file '{}' has been changed to {}".format(fclas, str(inputSRname)))
    else:
        arcpy.AddMessage("The coordinate system of the file '{}' does not need to be changed".format(fclas))
