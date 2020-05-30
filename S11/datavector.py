import arcpy

facilshp =r"E:\programin\semestr2\samrob\S11_GIS_FILE\Progr_GIS_s11\facilities.shp"
zipshp = r"E:\programin\semestr2\samrob\S11_GIS_FILE\Progr_GIS_s11\zip.shp"
arcpy.env.workspace = r"E:\programin\semestr2\samrob\S11_GIS_FILE\Progr_GIS_s11\Results"
distanc = '3000'
fieldname = 'FACILITY'
fieldval = 'COLLEGE'
arcpy.env.overwriteOutput = True

# make feature layers, select attributes
arcpy.MakeFeatureLayer_management(facilshp, 'facilitiesss')
arcpy.MakeFeatureLayer_management(zipshp, 'zip')
arcpy.AddMessage('Make feature layers')
arcpy.SelectLayerByLocation_management('facilitiesss', 'WITHIN_A_DISTANCE', 'zip', distanc+' meters', 'NEW_SELECTION')
arcpy.SelectLayerByAttribute_management('facilitiesss', 'SUBSET_SELECTION', "{} = '{}'".format(fieldname, fieldval))
arcpy.AddMessage("Selecting objects within {} meters with '{}' values in the field '{}'".format(distanc, fieldval, fieldname))


# create a new feature class similar to facilities.shp in Results directory
create_shp = "facilities_Distance_{}.shp".format(distanc)
arcpy.CreateFeatureclass_management(arcpy.env.workspace, create_shp, "POINT", spatial_reference="facilitiesss")

#create fields
insertfields = ['ADDRESS', 'NAME', 'FACILITY', 'XY']
for f in insertfields:
    arcpy.AddField_management(create_shp, f, "TEXT")
searchfields = ['ADDRESS', 'NAME', 'FACILITY', 'SHAPE@XY']
with arcpy.da.InsertCursor(create_shp, searchfields) as cursorI, arcpy.da.SearchCursor("facilitiesss", searchfields) as cursorS:
    for row in cursorS:
        cursorI.insertRow(row)
arcpy.AddMessage("Created file. Created fields and records: {}".format(create_shp))

# facilities_Distance_3000.shp created and update field COLLEGE_NAME
fieldnew = fieldval[:6] + 'NAME'
arcpy.AddField_management(create_shp, fieldnew, "DOUBLE")

fac_idval = []
with arcpy.da.SearchCursor("facilitiesss", 'FAC_ID') as cursorSS:
    for row in cursorSS:
        fac_idval.append(row)

i = 0
with arcpy.da.UpdateCursor(create_shp, fieldnew) as cursorU:
    for row in cursorU:
        row = fac_idval[i]
        cursorU.updateRow(row)
        i += 1
arcpy.AddMessage('Created field {} and updated in a file {}'.format(fieldnew, create_shp))