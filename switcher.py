import subprocess
import sys
import time

# Bauland-NAS lokal: 192.168.2.250
# Bauland-NAS extern: 10.10.0.50

context_list = {"local": "192.168.2.250", "remote": "10.10.0.50"}

device_list = [
    {"driveletter":"H", "share": "BaulandGBR", "use": True},
    {"driveletter":"I", "share": "Bauland_intern", "use": True},
    {"driveletter":"J", "share": "Gesellschafter_intern", "use": True},
    {"driveletter":"K", "share": "Auslagerungen", "use": True},
    {"driveletter":"L", "share": "BFSW_Wohnen_GbR", "use": True},
    {"driveletter":"M", "share": "Wohnen_an_der_Elbe_GMBH", "use": True},
    {"driveletter":"N", "share": "B_S_Jahnring_28_GbR", "use": True},
    {"driveletter":"O", "share": "F_S_Vermietungs_GbR", "use": True},
    {"driveletter":"P", "share": "Scanner", "use": True},
    {"driveletter":"P", "share": "Posteingang", "use": True},
    {"driveletter":"Y", "share": "Home_Peter", "use": True},
    {"driveletter":"Z", "share": "Home_Olaf", "use": True},
]

current_context = None
default_context = "remote"
secondary_context = "local"

sp = subprocess.run("wmic netuse where LocalName='Z:' get Remotename /value", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
context_hint = str(sp.stdout.strip())
for key in context_list.keys():
    if context_list.get(key) in context_hint:
        print("Aktueller Kontext ist: {}".format(key))
        current_context = key

if current_context == None or current_context == secondary_context:
    switch_to_context = default_context
else:
    switch_to_context = secondary_context

print("Wechsel in den Kontext: {}".format(switch_to_context))
time.sleep(3)

#Clean list
print("Loesche alle Netzwerkverbindungen...")
sp = subprocess.run("net use * /delete /yes", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if sp.returncode == 0:
    print("Netzwerkverbindungen erfolgreich geloescht.")
else:
    print("Fehler beim loeschen der Netzwerkverbindungen.")
    sys.exit()

time.sleep(5)


for elem in device_list:
    sp = subprocess.run("net use {}: \\\{}\{} /PERSISTENT:YES".format(
                                                elem.get("driveletter"),
                                                context_list.get(switch_to_context),
                                                elem.get("share"),
                                                ), shell=True, check=True,
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if sp.returncode == 0:
        print("Netzlaufwerk {} erfolgreich konfiguriert: //{}/{}".format(elem.get("driveletter"),
                                                context_list.get(switch_to_context),
                                                elem.get("share")))
    else:
        print("Fehler beim loeschen der Netzwerkverbindungen.".format(elem.get("driveletter"),
                                                context_list.get(switch_to_context),
                                                elem.get("share")))
        sys.exit()
