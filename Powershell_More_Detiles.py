import re,os,csv
from lxml import etree
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view
from zipfile import ZipFile 

def Magic(evtx):
	ps_scripts_ran = []

	for xml, row in evtx_file_xml_view(evtx.get_file_header()):
		try:
			for entry in to_lxml(xml):
				R_ID = entry.xpath("/Event/System/EventRecordID")[0].text
				ctime = entry.xpath("/Event/System/TimeCreated")[0].get("SystemTime")
				Computer = entry.xpath("/Event/System/Computer")[0].text
				path = str(to_lxml(xml).xpath("/Event/EventData/Data")[4].text).strip()
				command = to_lxml(xml).xpath("/Event/EventData/Data[@Name='ScriptBlockText']")[0].text.encode('ascii','replace')
				IP= re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', command).group()
				Domin= re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', command) 
				Base64= re.search(r'"(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?"', command)
				ps_scripts_ran.append([R_ID, str(ctime).replace(" ", "Timee") + "Z",Computer,path,IP,Domin,Base64])
				
		except Exception :
			continue
	return ps_scripts_ran
	
def to_lxml(record_xml):
    utf8_parser = etree.XMLParser(encoding='utf-8')
    return etree.fromstring("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\" ?>%s" %
            record_xml.replace("xmlns=\"http://schemas.microsoft.com/win/2004/08/events/event\"", "").encode('utf-8'), parser=utf8_parser)
 




def OutPut(script_data):
	start = csv.writer(open("output.csv","w"))
	start.writerow(['RecordID','Time','Computer_Name','Scripte_runned_path', 'IP', 'Domin','Base64'])
	path_s=[]
	for entries in script_data:
		start.writerow([entries[0], entries[1], entries[2],entries[3],entries[4],entries[5],entries[6]])
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

    for root, subdirs, files in os.walk("C:\\Windows\\System32\winevt\\Logs"):
        for file_names in files:
            if file_names=="Microsoft-Windows-PowerShell%4Operational.evtx":
                with Evtx(os.path.abspath("C:\Windows\System32\winevt\Logs\\" + file_names)) as evtx:  #Here where the Magic Happen 
                    script_data = Magic(evtx)
                    z = OutPut(script_data)
	get_all_file_zip(z)
				




if __name__ == "__main__":
    main()
