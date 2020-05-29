import arcpy
arcpy.env.overwriteOutput = True
inrast = arcpy.GetParameterAsText(0)
outcont = arcpy.GetParameterAsText(1)
interval = arcpy.GetParameterAsText(2)
if interval == '#' or not interval:
    interval = "25"
basecont = arcpy.GetParameterAsText(3)
if basecont == '#' or not basecont:
    basecont = "0"

try:
    arcpy.gp.Contour_sa(inrast, outcont, interval, "0", "1")
    arcpy.AddMessage("Created contour!")
except:
    arcpy.GetMessage(0)