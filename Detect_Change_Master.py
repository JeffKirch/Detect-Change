######################
# Detect Change 3.0
# Setup for Detect Change 3.0 to run.
#
# Contact info: Jeff Kirchberg
# Contact email: Jeff.a.kirchberg@gmail.com
######################


import shutil
import csv
import json
import datetime
import os
import arcpy
import smtplib
from Detect_Change_Functions_Library import Create_Setup_Folder, New_Feature_Class_Folder_Create,Detect_Change_Workspace_Folder_Creation,SetupExportFolders,ExportFeatureClasses, Detect_Change

#Set Base file path of script to run

Base_File_Path= r'C:\Users\jkirchberg\Desktop\Detect_Change_3.0' # This is an example.  Input you're own output file path


#Dictionary of feature classes
#Dictionary schema {Key: (FeatureClassName,FilePath,Unique_ID,ExportMethod,XMLRename)}
#Key = Just a sequential number
#FeatureClassName = Name of feature class with quotes around the string
#FilePath = The file path to the feature class as a file path string (example: r'C:\GIS\Detect_Change_Project\Testing_Space')
#Unique_ID = The unique ID field of the feature class
#ExportMethod = "FTF" or Feature To Feature is the faster method but may fail to handle larger datasets.  "XML" or Export TO XML is the longer process, but more stable.  "CM" or Copy Management is a simalar process to FTF.  I'm not sure which method works faster.
#XMLRename = Export To XML method requires the renaming of a feature class.  Best practice is to rename the feature class to the same name as it is found in the orginal database.  



# Work
Dict= {1:("RoadCenterline",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.ReferenceData\LocalGovernment.JC.RoadCenterline',"CENTERLINEID","CM",None),
2:("Sign",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.FacilitiesStreets\LocalGovernment.JC.Sign',"FACILITYID","CM","Sign"),
3:("Sidewalk",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.FacilitiesStreets\LocalGovernment.JC.Sidewalk',"FACILITYID","CM","Sidewalk"),
4:("LandscapeArea",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.FacilitiesStreets\LocalGovernment.JC.LandscapeArea' ,"FACILITYID","CM",None),
5:("PavementMarkingLine",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.FacilitiesStreets\LocalGovernment.JC.PavementMarkingLine',"FACILITYID","CM","PavementMarkingLine"),
6:("StreetPavement",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.FacilitiesStreets\LocalGovernment.JC.StreetPavement',"FACILITYID","CM","StreetPavement"),
7:("Support",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.FacilitiesStreets\LocalGovernment.JC.Support',"FACILITYID","CM","Support"),
8:("Tree",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.FacilitiesStreets\LocalGovernment.JC.Tree',"FACILITYID","CM","Tree"),
9:("x_MowingArea",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.FacilitiesStreets\LocalGovernment.JC.x_MowingArea',"FACILITYID","CM","x_MowingArea"),
10:("BrushZones",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.InfrastructureOperations\LocalGovernment.JC.BrushZones',"DISTRICTID","CM",None),
11:("MosquitoZones",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.InfrastructureOperations\LocalGovernment.JC.MosquitoZones',"DISTRICTID","CM",None),
12:("MowingZones",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.InfrastructureOperations\LocalGovernment.JC.MowingZones',"DISTRICTID","CM",None),
13:("SweepZones",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.InfrastructureOperations\LocalGovernment.JC.SweepZones',"DISTRICTID","CM",None),
14:("InletStructures",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.Stormwater\LocalGovernment.JC.y_STORMINF_InletStructures',"Cartegraph_ID","CM","y_STORMINF_InletStructures"),
15:("PipeCulverts",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.Stormwater\LocalGovernment.JC.y_STORMINF_PipeCulverts',"Cartegraph_ID","CM","y_STORMINF_PipeCulverts"),
16:("PipeInlets",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.Stormwater\LocalGovernment.JC.y_STORMINF_PipeInlets',"Cartegraph_ID","CM","y_STORMINF_PipeInlets"),
17:("PipeOutlets",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.Stormwater\LocalGovernment.JC.y_STORMINF_PipeOutlets',"Cartegraph_ID","CM","y_STORMINF_PipeOutlets"),
18:("StorageAreaPolys",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.Stormwater\LocalGovernment.JC.y_STORMINF_StorageAreaPolys',"Cartegraph_ID","CM","y_STORMINF_StorageAreaPolys"),
19:("StormManhole",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.Stormwater\LocalGovernment.JC.y_STORMINF_StormManhole',"Cartegraph_ID","CM","y_STORMINF_StormManhole"),
20:("Fiber",r'\\jc-gis\Files\GisData\db_connections\LocalGovernment_SDE\DEFAULTversion\DEFAULT LocalGov.sde\LocalGovernment.JC.x_Utilities\LocalGovernment.JC.x_Fiber',"FACILITYID","CM","x_Fiber"),
}
 
Email_List = ['jkirchberg@johnsoncitytn.org']

emailbody = ""


#Functions = [Create_Setup_Folder(Base_File_Path), New_Feature_Class_Folder_Create(Base_File_Path,Dict), Detect_Change_Workspace_Folder_Creation(Base_File_Path,Dict), SetupExportFolders(Base_File_Path,Dict), ExportFeatureClasses(Base_File_Path,Dict), Detect_Change(Base_File_Path,Dict,Email_List,emailbody)]

Function_names = ("Create_Setup_Folder", "New_Feature_Class_Folder_Create", "Detect_Change_Workspace_Folder_Creation", "SetupExportFolder", "ExportFeatureClasses", "Detect_Change")
Functions = {"Create_Setup_Folder" : Create_Setup_Folder(Base_File_Path), "New_Feature_Class_Folder_Create" : New_Feature_Class_Folder_Create(Base_File_Path,Dict), "Detect_Change_Workspace_Folder_Creation" : Detect_Change_Workspace_Folder_Creation(Base_File_Path,Dict), "SetupExportFolder" : SetupExportFolders(Base_File_Path,Dict), "ExportFeatureClasses" : ExportFeatureClasses(Base_File_Path,Dict), "Detect_Change" : Detect_Change(Base_File_Path,Dict,Email_List,emailbody)}

successBool = True
ReturnedValues = ()
iter = 0    
#Iterate through scripts
for Function_name in Function_names:

	try:
		if successBool == True:
			ReturnedValues = Functions[Function_name]
			if type(ReturnedValues) is tuple:
				LengthOfReturnedValues = len(ReturnedValues)
				if LengthOfReturnedValues == 1:
					successBool = ReturnedValues
				elif LengthOfReturnedValues == 2:
					successBool = ReturnedValues[0]
					emailbody = ReturnedValues[1]
			else:
				successBool = ReturnedValues
			if successBool != True:
				emailbody = emailbody + '<br><font color="red">' + Function_names[iter] + ' failed with error: ' + str(successBool) + '</font><br>'
			else:
				emailbody = emailbody + "<br>" + Function_names[iter] + " ran successfully.<br>"
		iter +=1
	except Exception as inst:
		emailbody = emailbody + '<br><font color="blue">' + str(Function_name) + ' failed with error: ' + str(inst) + '</font><br>'

emailintro = "Hello,<br><br>Here are the results of the scripts ran this evening:<br>"
emailEnd = "<br>Have a great evening!<br><br>"

today = datetime.datetime.now().strftime("%Y-%m-%d")
emailintro = "Hello,<br><br>Here are the results of the scripts ran this evening:<br>"
emailEnd = "<br><br>Have a great evening!<br><br>"

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

msg = MIMEMultipart()
msg['Subject'] = 'Script Report Detect Change 3.0, ' + today
msg['From'] = 'youremail@gmail.com' # The will be the email that you will send from
msg['To'] = 'example@gmail.com'  # This will be the email list that you send to
body = emailintro + emailbody + emailEnd
	
msg.attach(MIMEText(body,'html'))
	
server=smtplib.SMTP('smtp.gmail.com', 587)  # This will differ depending on your email service
server.starttls()
server.login('youremail@gmail.com','yourpassword') # The email that you are sending from and password
server.sendmail('youremail@gmail.com',Email_List, msg.as_string())
server.quit()


