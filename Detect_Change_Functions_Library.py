# -*- coding: utf-8 -*- 

##########################
# Library of functions for detect change program
##########################

import os
import shutil
import datetime
import arcpy
import csv
import json
import pandas
import smtplib

i = datetime.datetime.now()

def Create_Setup_Folder(Base_File_Path):
	'''
	Checks the Base_File_Path to see if Detect_Change_Workspace exists.  If it does not exist, create 
	Detect_Change_Workspace and within create Changes_Found and Feature_Classes folders.
	'''
	try:
		List= os.listdir(Base_File_Path)
		print List
		if "Detect_Change_Workspace" not in List:
			os.makedirs(Base_File_Path + "\\" + "Detect_Change_Workspace")
			os.makedirs(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found")
			os.makedirs(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes")
		elif "Detect_Change_Workspace" in List:
			pass
		return (True)
	except Exception as inst:
		return (inst)
	


	
def New_Feature_Class_Folder_Create(Base_File_Path,Dict):
	'''
	Loops through the setup dictionary and checks if a folder for each feature class already exists.
	If the folder does not exist, create a folder named after the feature class in the Feature_Classes
	folder.  Then create a folder and geodatabse in Changes_Found to hold today's changes.
	'''
	try:
		for k,v in Dict.items():
			List = os.listdir(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes")
			if v[0] not in List:
				os.makedirs(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" + "\\" + v[0])
			else:
				print v[0] + " already exists"
		os.makedirs(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)))
		for k,v in Dict.items():
			os.makedirs(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "\\" + v[0])
			# Creates new file gdb for export 
			GeodatabaseName = (("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "_" + v[0] + ".gdb")
			arcpy.CreateFileGDB_management(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "\\" + v[0], GeodatabaseName)
		return (True)
	except Exception as inst:
		return (inst)
	
	
def Detect_Change_Workspace_Folder_Creation(Base_File_Path,Dict):
	'''
	Checks if each feature class folder has a Yesterday folder.  If it does not exist, create both Yesterday and Today
	folders.  Then create a geodatabase in Today and export from the data source to the newly created database.
	'''
	try:

		for k,v in Dict.items():
			List = os.listdir(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0])
			if "Yesterday" not in List:
				os.makedirs(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Yesterday")
				os.makedirs(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Today")
				# Creates new file gdb for export 
				GeodatabaseName = ("%s.%s.%s" % (i.year, i.month, i.day) + "_" + v[0] + "_Export_GDB")
				arcpy.CreateFileGDB_management(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" + v[0] + "\\" + "Today", GeodatabaseName)
			else:
				pass
		return (True)
	except Exception as inst:
		return (inst)
		
	
def SetupExportFolders(Base_File_Path,Dict):
	'''
	For each feature class in the setup dictionary, reset the Today and Yesterday folders.  To do this, delete Yesterday
	and recreate it.  Then move the content of Today to Yesterday.  Finally, Make a new GDB in Today. 
	'''
	try:
		
		for k,v in Dict.items():
			shutil.rmtree(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Yesterday")
			os.makedirs(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Yesterday")
			
			files = os.listdir(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Today")
			files.sort()
			for f in files:
				src = Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Today" + "\\" + f
				dst = Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Yesterday" + "\\" + f
				shutil.move(src,dst)
			# Creates new file gdb for export
			GeodatabaseName = ("%s.%s.%s" % (i.year, i.month, i.day)+ "_" + v[0] + "_Export_GDB" + ".gdb")
			arcpy.CreateFileGDB_management(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Today", GeodatabaseName)
		return (True)
	except Exception as inst:
		return (inst)
		
		
def ExportFeatureClasses(Base_File_Path,Dict):
	'''
	For each feature class in the setup Dictionary, export from data source to its appropriate Feature_Classes folder using the 
	designated export method.  Export methods are either FTF or XML.  FTF simply stands for Feature to Feature.  XML includes
	both processes of Export XML Workspace Document and then Import XML Workspace Document.
	'''
	try:
		
		for k,v in Dict.items():
			print v[1]
			files = os.listdir(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Today")
			for f in files:
				extension = os.path.splitext(f)[1]
				print extension
				if extension == ".gdb":
					Input_GDB = f
				else:
					pass
				print f
			arcpy.env.workspace = v[1]
			if v[3] == "FTF":
				#outFeatureClass = ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + v[0] + "_Export"
				outFeatureClass = v[0] + "_Export"
				print outFeatureClass
				arcpy.FeatureClassToFeatureClass_conversion(v[1], (Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Today" + "\\" + Input_GDB), outFeatureClass, None, None, None)
			if v[3] == "XML":
				outLocationPath = Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Today" + "\\" + v[0] + ".xml"
				###<<< Export XML Function >>>###
				# Set local variables
				in_data = v[1]
				out_file = outLocationPath
				export_option = 'DATA'
				storage_type = 'BINARY'
				export_metadata = 'METADATA'
				# Execute ExportXMLWorkspaceDocument
				arcpy.ExportXMLWorkspaceDocument_management(in_data, out_file, export_option, storage_type, export_metadata)
				###<<< /Export XML Function >>>###
				
				###<<< Import XML to GDB Function >>>###
				# Set local variables
				target_gdb = Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Today" + "\\" + Input_GDB
				in_file = outLocationPath
				import_type = "DATA"
				config_keyword = "DEFAULTS"
				# Execute ImportXMLWorkspaceDocument
				arcpy.ImportXMLWorkspaceDocument_management(target_gdb, in_file, import_type, config_keyword)
				###<<< /Import XML to GDB Function >>>###
				# Rename feature class to reference easier
				arcpy.env.workspace = target_gdb
				# Set local veriables
				in_data = target_gdb + "\\" + v[4]
				out_data = target_gdb + "\\" + v[0] + "_Export"
				data_type = "FeatureClass"
				
				# The feature class must now be renamed so that there is a reliable name to reference it by.
				# Execute Rename
				arcpy.Rename_management(in_data,out_data,data_type)
			if v[3] == "CM":
				# Set local variables
				in_data = v[1]
				out_data = (Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" +"\\" +v[0] + "\\" + "Today" + "\\" + Input_GDB + "\\" + v[0] + "_Export")
				arcpy.Copy_management(in_data, out_data)
		return (True)
	except Exception as inst:
		return (inst)
		
		
def Detect_Change(Base_File_Path,Dict,Email_List,emailbody):
	'''
	For each feature class in the setup dictionary, compare Yesterday and Today to find adds,
	deletes, and changes.  Then record adds, deletes, and changes into separate csv files as
	well as export them into a geodatabase for that day.  Finally, format the body of the 
	email that will be sent to all individuals on the email list.
	'''
	try:
		
		for k,v in Dict.items():
			# To find the geodatabase filepath, we must search for the ffile the has a .gdb file extention
			Today_files = os.listdir(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" + "\\" + v[0] + "\\" + "Today")
			for f in Today_files:
				extension = os.path.splitext(f)[1]
				if extension == ".gdb":
					Today_Input_GDB = f
				else:
					pass
			# To find the geodatabase filepath, we must search for the ffile the has a .gdb file extention
			Yesterday_files = os.listdir(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" + "\\" + v[0] + "\\" + "Yesterday")
			for f in Yesterday_files:
				extension = os.path.splitext(f)[1]
				if extension == ".gdb":
					Yesterday_Input_GDB = f
				else:
					pass
			# Set the data sources for the rest of the function
			Today_Data_Source = Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" + "\\" + v[0] + "\\" + "Today" + "\\" + Today_Input_GDB + "\\" + v[0] + "_Export"
			Yesterday_Data_Source = Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" + "\\" + v[0] + "\\" + "Yesterday" + "\\" + Yesterday_Input_GDB + "\\" + v[0] + "_Export"
				
				
			# Check Yesterday shape type (Polygon, Polyline, or Point)
			desc = arcpy.Describe(Yesterday_Data_Source)
			Yesterday_Shape_Type = desc.shapeType
			
			# Check Today shape type (Polygon, Polyline, or Point)
			desc_1 = arcpy.Describe(Today_Data_Source)
			Today_Shape_Type = desc_1.shapeType
			
			###### For use later
			SQL_UniqueID_Value = (v[2])
			######
			
			#Get Yesterday field names
			Yesterday_fields = arcpy.ListFields(Yesterday_Data_Source)
			# Variable that will be equal to the index of the unique ID field
			Yesterday_Unique_Field_Position= 0
			# Iterate through fields in Yesterday_fields and break when field == unique ID field
			for field in Yesterday_fields:
				if field.name == (v[2]):
					break
				else:
					Yesterday_Unique_Field_Position += 1
			# Yesterday_Field_Structure will be used to compare records
			Yesterday_Field_Structure = {}
			# Yesterday_Field_Structure_By_Name will be used to compare records
			Yesterday_Field_Structure_By_Name = {}
			# CSV headers
			Yesterday_CSV_Headers = ["UniqueID"]
			
			Counter = 0
			
			values = {}
			values_1 = {}
			
			for field in Yesterday_fields:
				# Blob fields are not comparable, thus we do not want to include them in the list of field names
				if field.type == "Blob":
					pass
				else:
					values = {Counter: (field.name, field.type, Counter)}
					values_1 = {field.name: (field.name, field.type, Counter)}
					Yesterday_Field_Structure.update(values)
					Yesterday_Field_Structure_By_Name.update(values_1)
					Yesterday_CSV_Headers.append(field.name)
					Counter += 1
					
			# 
			Yesterday = {}
			
			
			values = {}
			
			Records_In_Cursor1 = 0
			
			Yesterday_Cursor = arcpy.da.SearchCursor(Yesterday_Data_Source, ['*'], None, None, None, None)
			if Yesterday_Shape_Type == "Polygon":
				for row in Yesterday_Cursor:
					row = row[:-2] + (round(row[-2],5),round(row[-1],5))
					values = {row[Yesterday_Unique_Field_Position]: row}
					Yesterday.update(values)
					Records_In_Cursor1 += 1
			if Yesterday_Shape_Type == "Polyline":
				for row in Yesterday_Cursor:
					new_row = row[:-1] + ((round(row[-1],6)),1)
					new_row = new_row[:-1]
					values = {row[Yesterday_Unique_Field_Position]: new_row}
					Yesterday.update(values)
					Records_In_Cursor1 += 1
			else:
				for row in Yesterday_Cursor:
					values = {row[Yesterday_Unique_Field_Position]: row}
					Yesterday.update(values)
					Records_In_Cursor1 += 1
				
			print Records_In_Cursor1
		###########################################################################################################################
		###########################################################################################################################
		###########################################################################################################################
				
			Today_fields = arcpy.ListFields(Today_Data_Source)
			# Variable that will be equal to the index of the unique ID field
			Today_Unique_Field_Position = 0
			
			for field in Today_fields:
				if field.name == (v[2]):
					break
				else:
					Today_Unique_Field_Position += 1
					
					
			Today_Field_Structure = {}
			Today_Field_Structure_By_Name = {}	
			Today_CSV_Headers = ["UniqueID"]
			
			Counter = 0
			
			values = {}
			values_1 = {}
			
			for field in Today_fields:
				if field.type == "Blob":
					pass
				else:
					values = {Counter: (field.name, field.type, Counter)}
					values_1 = {field.name: (field.name, field.type, Counter)}
					Today_Field_Structure.update(values)
					Today_Field_Structure_By_Name.update(values_1)
					Today_CSV_Headers.append(field.name)
					Counter += 1

			Today = {}

			
			values = {}
			
			
			Records_In_Cursor = 0
			
			Today_Cursor = arcpy.da.SearchCursor(Today_Data_Source, ['*'], None, None, None, None)
			if Today_Shape_Type == "Polygon":
				for row in Today_Cursor:
					row = row[:-2] + (round(row[-2],5),round(row[-1],5))
					values = {row[Today_Unique_Field_Position]: row}
					Today.update(values)
					Records_In_Cursor += 1
			if Today_Shape_Type == "Polyline":
				for row in Today_Cursor:
					new_row = row[:-1] + ((round(row[-1],6)),1)
					new_row = new_row[:-1]
					values = {row[Today_Unique_Field_Position]: new_row}
					Today.update(values)
					Records_In_Cursor += 1
			else:
				for row in Today_Cursor:
					values = {row[Today_Unique_Field_Position]: row}
					Today.update(values)
					Records_In_Cursor += 1
			
			print Records_In_Cursor
			print "Completed"

			
			############################################
			print i
			

			####
			#### <CSV Setup>
			####
			
			CHANGE_Today_CSV_NAME = (("Changes_Today" + v[0] +("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second))) +".csv")
			CHANGER_Today = open ((Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second))) + "\\" + v[0] + "\\" + CHANGE_Today_CSV_NAME, 'wb')
			CHANGE_Today_LOG = csv.writer(CHANGER_Today, quoting=csv.QUOTE_ALL)
			
			CHANGE_Yesterday_CSV_NAME = (("Changes_Yesterday" + v[0] + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second))) +".csv")
			CHANGER_Yesterday = open((Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second))) + "\\" + v[0] + "\\" + CHANGE_Yesterday_CSV_NAME, 'wb')
			CHANGE_Yesterday_LOG = csv.writer(CHANGER_Yesterday, quoting=csv.QUOTE_ALL)
			
			DELETES_CSV_NAME = (("Deletes_" + v[0] + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second))) +".csv")
			DELETES = open((Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second))) + "\\" + v[0] + "\\" + DELETES_CSV_NAME, 'wb')
			DELETES_LOG = csv.writer(DELETES, quoting=csv.QUOTE_ALL)
			
			ADDS_CSV_NAME = (("Adds_" + v[0] + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second))) +".csv")
			ADDS = open((Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second))) + "\\" + v[0] + "\\" + ADDS_CSV_NAME, 'wb')
			ADD_LOG = csv.writer(ADDS, quoting=csv.QUOTE_ALL)
			
			####
			#### </CSV Setup Completed>
			####
			
			####
			#### <GDB Export Setup>
			####
			
			GDB_Exports_ADDS = []
			
			GDB_Exports_CHANGES_Today = []
			
			GDB_Exports_CHANGES_Yesterday = []
			
			GDB_Exports_DELETES = []
			
			####
			#### </GDB Export Setup>
			####
			
			How_Many_Records = 0
			CHANGE_Today_LOG.writerow([g for g in Yesterday_CSV_Headers])
			CHANGE_Yesterday_LOG.writerow([g for g in Yesterday_CSV_Headers])
			DELETES_LOG.writerow([g for g in Yesterday_CSV_Headers])
			ADD_LOG.writerow([g for g in Today_CSV_Headers])
			for k,vv in Yesterday.items():
				try:
					Write_DELETES_LOG = False
					returned = Today.get(vv[Yesterday_Unique_Field_Position], None)
					if returned == None:
						print "Found Something"
						Record_Row = [vv[Yesterday_Unique_Field_Position]]
						for val in vv:
							Record_Row.append(val)
						DELETES_LOG.writerow(Record_Row)
						GDB_Exports_DELETES.append(vv[Yesterday_Unique_Field_Position])
						pass
					else:
						How_Many_Records += 1
						Record_Row_Yesterday = [vv[Yesterday_Unique_Field_Position]]
						Record_Row_Today = [returned[Today_Unique_Field_Position]]
						Write_Record_CSV = False
						for p,y in Yesterday_Field_Structure.items():
							Field_Type = y[1]
							Field_Name = y[0]
							
							if Field_Type == "GlobalID" or Field_Type == "Blob" or Field_Name == "OBJECTID":
								Record_Row_Yesterday.append(None)
								Record_Row_Today.append(None)
							else:
								Lookup_Correct_Compare_Index = Today_Field_Structure_By_Name.get(y[0])
								yesterday_index = y[2]
								today_index = Lookup_Correct_Compare_Index[2]
								Match_Value =(vv[yesterday_index] == returned[today_index])
								if Match_Value == False:
									Record_Row_Yesterday.append(vv[yesterday_index])
									Record_Row_Today.append(returned[today_index])
									Write_Record_CSV = True
								else:
									Record_Row_Yesterday.append(None)
									Record_Row_Today.append(None)
						if Write_Record_CSV == True:
							CHANGE_Yesterday_LOG.writerow(Record_Row_Yesterday)
							CHANGE_Today_LOG.writerow(Record_Row_Today)
							GDB_Exports_CHANGES_Yesterday.append(vv[Yesterday_Unique_Field_Position])
							GDB_Exports_CHANGES_Today.append(returned[Today_Unique_Field_Position])
						else:
							pass
				except Exception as inst:
					print (inst)
					pass
				
			for k,vvv in Today.items():
				try:
					returned = Yesterday.get(vvv[Today_Unique_Field_Position], None) 
					Record_Row = [vvv[Today_Unique_Field_Position]]
					if returned == None:
						print "AAAAAADDDDDDDDDDDDDDDDDDDDDDSSSS"
						for val in vvv:
							Record_Row.append(val)
						ADD_LOG.writerow(Record_Row)
						GDB_Exports_ADDS.append(vvv[Today_Unique_Field_Position])
				except Exception as inst:
					print (inst)
					pass
			print How_Many_Records
			
			CHANGER_Yesterday.close()
			CHANGER_Today.close()
			DELETES.close()
			ADDS.close()
			
			####
			####
			####
			
			if GDB_Exports_ADDS != []:
				SQL_Selection_wClause = ""
				for value_2 in GDB_Exports_ADDS:
					SQL_Selection_wClause += SQL_UniqueID_Value + " = " + "'%s'" % (value_2) + " or "
				
				print "I got Here"
			
				SQL_Selection_wClause_final = SQL_Selection_wClause[:-4]

				# Set the workspace
				arcpy.env.workspace = Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" + "\\" + v[0] + "\\" + "Today" + "\\" + Today_Input_GDB

				print "I got here 2"
			
				# Make a layer from the feature class
				arcpy.MakeFeatureLayer_management(Today_Data_Source, v[0] + "_ADDS") 
			
				print SQL_Selection_wClause_final

				# Within selected features, further select only those cities which have a population > 10,000   
				arcpy.SelectLayerByAttribute_management((v[0] + "_ADDS"), "NEW_SELECTION", SQL_Selection_wClause_final)
                 
				# Write the selected features to a new featureclass
				arcpy.CopyFeatures_management(v[0] + "_ADDS", Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "\\" + v[0] + "\\" + (("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "_" + v[0] + ".gdb") + "\\" + "ADDS_" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)))

				
			if GDB_Exports_CHANGES_Yesterday != []:
				SQL_Selection_wClause = ""
				for value_2 in GDB_Exports_CHANGES_Yesterday:
					SQL_Selection_wClause += SQL_UniqueID_Value + " = " + "'%s'" % (value_2) + " or "
				
				print "I got Here"
			
				SQL_Selection_wClause_final = SQL_Selection_wClause[:-4]

				# Set the workspace
				arcpy.env.workspace = Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" + "\\" + v[0] + "\\" + "Yesterday" + "\\" + Yesterday_Input_GDB

				print "I got here 2"
			
				# Make a layer from the feature class
				arcpy.MakeFeatureLayer_management(Yesterday_Data_Source, v[0] + "_CHANGES_YESTERDAY") 
			
				print SQL_Selection_wClause_final

				# Within selected features, further select only those cities which have a population > 10,000   
				arcpy.SelectLayerByAttribute_management((v[0] + "_CHANGES_YESTERDAY"), "NEW_SELECTION", SQL_Selection_wClause_final)
                 
				# Write the selected features to a new featureclass
				arcpy.CopyFeatures_management(v[0] + "_CHANGES_YESTERDAY", Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "\\" + v[0] + "\\" + (("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "_" + v[0] + ".gdb") + "\\" + "CHANGES_Yesterday_" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)))
				
			if GDB_Exports_CHANGES_Today != []:
				SQL_Selection_wClause = ""
				for value_2 in GDB_Exports_CHANGES_Today:
					SQL_Selection_wClause += SQL_UniqueID_Value + " = " + "'%s'" % (value_2) + " or "
				
				print "I got Here"
			
				SQL_Selection_wClause_final = SQL_Selection_wClause[:-4]

				# Set the workspace
				arcpy.env.workspace = Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" + "\\" + v[0] + "\\" + "Today" + "\\" + Today_Input_GDB

				print "I got here 2"
			
				# Make a layer from the feature class
				arcpy.MakeFeatureLayer_management(Today_Data_Source, v[0] + "_CHANGES_TODAY") 
			
				print SQL_Selection_wClause_final

				# Within selected features, further select only those cities which have a population > 10,000   
				arcpy.SelectLayerByAttribute_management((v[0] + "_CHANGES_TODAY"), "NEW_SELECTION", SQL_Selection_wClause_final)
                 
				# Write the selected features to a new featureclass
				arcpy.CopyFeatures_management(v[0] + "_CHANGES_TODAY", Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "\\" + v[0] + "\\" + (("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "_" + v[0] + ".gdb") + "\\" + "CHANGES_Today_" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)))
			
			if GDB_Exports_DELETES != []:
				SQL_Selection_wClause = ""
				for value_2 in GDB_Exports_DELETES:
					SQL_Selection_wClause += SQL_UniqueID_Value + " = " + "'%s'" % (value_2) + " or "
				
				print "I got Here"
			
				SQL_Selection_wClause_final = SQL_Selection_wClause[:-4]

				# Set the workspace
				arcpy.env.workspace = Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Feature_Classes" + "\\" + v[0] + "\\" + "Yesterday" + "\\" + Yesterday_Input_GDB

				print "I got here 2"
			
				# Make a layer from the feature class
				arcpy.MakeFeatureLayer_management(Yesterday_Data_Source, v[0] + "_DELETES") 
			
				print SQL_Selection_wClause_final

				# Within selected features, further select only those cities which have a population > 10,000   
				arcpy.SelectLayerByAttribute_management((v[0] + "_DELETES"), "NEW_SELECTION", SQL_Selection_wClause_final)
                 
				# Write the selected features to a new featureclass
				arcpy.CopyFeatures_management((v[0] + "_DELETES", Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "\\" + v[0] + "\\" + (("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "_" + v[0] + ".gdb") + "\\" + "DELETES_" + "%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)))
			
			
			#####
			#####
			#####
			
			CHANGER = open(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "\\" + v[0] + "\\" + ("Changes_Yesterday" + v[0] + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second))) +".csv", 'rb')
			
			DELETES = open(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "\\" + v[0] + "\\" + ("Deletes_" + v[0] + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second))) + ".csv", 'rb')
			
			ADDS = open(Base_File_Path + "\\" + "Detect_Change_Workspace" + "\\" + "Changes_Found" + "\\" + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second)) + "\\" + v[0] + "\\" + ("Adds_" + v[0] + ("%s.%s.%s__%s.%s.%s" % (i.year, i.month, i.day, i.hour, i.minute, i.second))) +".csv", 'rb')
			
			CSV_List = [CHANGER,DELETES,ADDS]
			CSV_Names = ["CHANGES","DELETES","ADDS"]
			
			
			Number_of_Records_Per_Column = []
			
			emailbody = emailbody + ("<br><br><font size='5'><u><b>" + v[0] + "</b></u></font>")
			
			CSV_incrementer = 0
			
			for csvs in CSV_List:
				Number_of_Rows_CSV = 0
				Details_YES_OR_NO = False
				if csvs == CHANGER:
					Details_YES_OR_NO = True
					print "I got here 444444"
				Email_CSV_Names = "<br><br><font size='4'><u>" + CSV_Names[CSV_incrementer] + "</u></font>"
				reader = csv.reader(csvs)
				jk = reader.next()
				List_of_Headers = []
				for columns in jk:
					Number_of_Records_Per_Column.append(0)
					List_of_Headers.append(columns)
				
				for row in reader:
					incrementer = 0
					for value_3 in row:
						if value_3!= "":
							Number_of_Records_Per_Column[incrementer] += 1
						incrementer += 1
					Number_of_Rows_CSV += 1
				Number_of_Records_Per_Column[0] = 0
				print Number_of_Records_Per_Column
				
				incrementer2000 = 0
				Email_CSV_Detail = ""
				
				if Details_YES_OR_NO == True:
					for value_4 in Number_of_Records_Per_Column:
						if value_4 != 0:
							Header_Name = List_of_Headers[incrementer2000]
							Email_CSV_Detail += ("<br>" + Header_Name + ": " + str(value_4))
						incrementer2000 += 1
						
				emailbody = emailbody + (Email_CSV_Names + ("<br>Total Number of records: " + str(Number_of_Rows_CSV)) + Email_CSV_Detail)
				Number_of_Records_Per_Column = []
				CSV_incrementer += 1
		print emailbody

		return (True, emailbody)
	except Exception as inst:
		print (inst)
		return (inst)
		
		
		
		
		
		
		
		
		
