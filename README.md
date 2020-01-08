# Powershell-Forensic-Analysis
A tool to Convert Powell-Shell EVTX into Human Readable format and then Export all The exeuted Artifact into CVS file includeing The path of the file that has been exeuted and some other useful Function associated with that event.It also,,Detect Base64 Encryption and decodes with in The CVS file. Plus extarcting all Ps1 and exe files that located on suspicious path such as "temp" Or "ProgramData" to a zip file for further analysis.


>Before Run The Script install The libraries And Run it as Admin
```
pip install lxml
pip install python-evtx
```
>Then Yo R Good To Go !

```
python WindowsPowerShell.py
```

Happy Hunting!! :shipit:

Powershell Version(2) can now parse("Microsoft-Windows-PowerShell%4Operational.evtx")Inculde ALL event that has Data(Note No dublication) 

Usage:

PowershellOperationAnalyzer.py "C:\Windows\System32\winevt\Logs\Microsoft-Windows-PowerShell%4Operational.evtx"

