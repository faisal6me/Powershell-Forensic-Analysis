import re,os,csv
from lxml import etree
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view
from zipfile import ZipFile 
import base64



def Magic(evtx):
	ps_scripts_ran = []

	for xml, row in evtx_file_xml_view(evtx.get_file_header()):
		try:
			for entry in to_lxml(xml):
				
				R_ID = entry.xpath("/Event/System/EventRecordID")[0].text
				#print R_ID
				ctime = entry.xpath("/Event/System/TimeCreated")[0].get("SystemTime")
				#print ctime
				Computer = entry.xpath("/Event/System/Computer")[0].text
				#print Computer
				user = entry.xpath("/Event/System/Security")[0].text
				#print user
				paths = str(to_lxml(xml).xpath("/Event/EventData/Data")[0].text)
				path=""
				for line in paths.split("\n"):
					#print path
					if "HostApplication" in line:
						line.split("HostApplication=")[1]
						path=line
					else:
						path="No Exe"
				ps_scripts_ran.append([R_ID, str(ctime).replace(" ", "Timee") + "Z",Computer,path])

		except Exception :
			continue
	return ps_scripts_ran
	
	
	
	
def to_lxml(record_xml):
    utf8_parser = etree.XMLParser(encoding='utf-8')
    return etree.fromstring("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\" ?>%s" %
            record_xml.replace("xmlns=\"http://schemas.microsoft.com/win/2004/08/events/event\"", "").encode('utf-8'), parser=utf8_parser)
 
	
def to_Baes64(Coded):
	x=Coded[3]
	decodedBase64=[]
	for each in x:
		try:
			if len(each) % 4 == 0 and re.search('^[A-Za-z0-9+\/=]+\Z', each):
				decodedBase64.append(base64.b64decode(each))
		except Exception :
			continue
	return decodedBase64
	
	
	
	

def OutPut(script_data):
	start = csv.writer(open("output.csv","w"))
	start.writerow(['RecordID','Time','Computer_Name','Exeution'])
	path_s=[]
	for entries in script_data:
		start.writerow([entries[0], entries[1], entries[2],entries[3]])
		path_s.append(entries[3])
	return path_s
		

def get_all_file_zip(directory):
	with ZipFile('my_python_files.zip','w') as zip:
		for each in directory:
			if "TEMP" or "ProgramData" in each:
				try:
					zip.write(each)					
				except WindowsError:
					continue
			else:
				pass
		
					
	
		
def main():

    for root, subdirs, files in os.walk("C:\\Users\\%Userprofile%\\Desktop\\POershell\\Mail"):
        for file_names in files:
            if file_names=="WindowsPowerShell.evtx":
                with Evtx(os.path.abspath("C:\\Users\\\%Userprofile%\\Desktop\\POershell\\Mail\\" + file_names)) as evtx: 
                    script_data = Magic(evtx)
					#to_Baes64(script_data)
                    z =OutPut(script_data)

		#get_all_file_zip(z)
				




if __name__ == "__main__":
    main()



















































"""

import xml.etree.cElementTree as ET
import re

with open("WindowsEvent.xml") as f:
    xml = f.read()
tree = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")

print tree
"""








































"""

from xml.dom import minidom

filename = "WindowsEvent.xml"
file = open(filename, "r")

xmldoc = minidom.parse(file)
itemlist = xmldoc.getElementsByTagName('HostApplication=')
print(len(itemlist))
"""
