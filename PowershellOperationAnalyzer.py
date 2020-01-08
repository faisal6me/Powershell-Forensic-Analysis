import Evtx.Evtx as evtx
import Evtx.Views as e_views
import re,os,csv

schema="http://schemas.microsoft.com/win/2004/08/events/event"
def Magic():
    import argparse
    ps_scripts_ran = []
    parser = argparse.ArgumentParser()
    parser.add_argument("evtx", type=str)
    args = parser.parse_args()

    with evtx.Evtx(args.evtx) as log:
        for  each  in log.records():
            elm  =  each . lxml ()
            R_ID =(elm.xpath ("//event:EventID" ,  namespaces = {"event":schema })[0].text)
            Sour =(elm.xpath ("//event:Channel" ,  namespaces = {"event":schema })[0].text)
            ctime =(elm.xpath("//event:TimeCreated", namespaces={"event":schema})[0].get("SystemTime"))
            User =(elm.xpath ("//event:Security" ,  namespaces = {"event":schema })[0].get("UserID"))
            path = (elm.xpath("//EventData:Data[@Name='ScriptBlockText']/text()", namespaces={"EventData":schema}))
            exists = False
            for item in ps_scripts_ran:
                if item[4]== path:
                    exists = True
            if not exists:
                ps_scripts_ran.append([R_ID,Sour, str(ctime).replace(" ", " T") + "Z",User,path])

        return ps_scripts_ran



def OutPut(script_data):
    start = csv.writer(open("output.csv","w"))
    start.writerow(['EventID','Source','Time','SID','Command_line'])
    path_s=[]
    
    for entries in script_data:
        start.writerow([entries[0], entries[1], entries[2],entries[3],entries[4]])
        path_s.append(entries[4])
    return path_s





def main():

    script_data = Magic()
    z = OutPut(script_data)




if __name__ == "__main__":
    main()
