MIT License

Copyright (c) 2019 faisal6me

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

import re,os,csv
from lxml import etree
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view


def Magic(evtx):
	ps_scripts_ran = []
	for xml, row in evtx_file_xml_view(evtx.get_file_header()):
		try:
			for entry in lxml(xml):
				R_ID = entry.xpath("/Event/System/EventRecordID")[0].text
				ctime = entry.xpath("/Event/System/TimeCreated")[0].get("SystemTime")
				Computer = entry.xpath("/Event/System/Computer")[0].text
				path = str(lxml(xml).xpath("/Event/EventData/Data")[4].text).strip()
				command = lxml(xml).xpath("/Event/EventData/Data[@Name='ScriptBlockText']")[0].text.encode('ascii','replace')
				ps_scripts_ran.append([R_ID, str(ctime).replace(" ", "Timee") + "Z",Computer,path,command])
		except Exception :
			continue
	return ps_scripts_ran
	
	
	
"""This Function Used To change The XML encoding From  EVTX which is XML Version =01 to Microsoft 2004 format utf-8"""
def lxml(raw): 
    utf8_parser = etree.XMLParser(encoding='utf-8')
    return etree.fromstring("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\" ?>%s" %
            raw.replace("xmlns=\"http://schemas.microsoft.com/win/2004/08/events/event\"", "").encode('utf-8'), parser=utf8_parser)

	

def OutPut(script_data):
	start = csv.writer(open("output.csv","w"))
	start.writerow(['RecordID','Time','Compter_Name','Scripte_Runed_path', 'Other_Finding'])
	for entries in script_data:
		start.writerow([entries[0], entries[1], entries[2],entries[3],entries[4]])

		
def main():

    for any, dirs, files in os.walk("C:\\Windows\\System32\winevt\\Logs"):
        for file_names in files:
            if file_names=="Microsoft-Windows-PowerShell%4Operational.evtx":
                with Evtx(os.path.abspath("C:\Windows\System32\winevt\Logs\\" + file_names)) as evtx:  #Here where the Magic Happen 
                    script_data = Magic(evtx)
                    OutPut(script_data)
				
		print os.getcwd()


if __name__ == "__main__":
    main()
