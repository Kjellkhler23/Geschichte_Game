import json
import os
import time
import streamlit as st
from colorama import init
from termcolor import colored

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def clear_console():
  os.system('cls' if os.name == 'nt' else 'clear')

zufriedenheit = 5
zufriedenheit_max = 20
zufriedenheit_min = 0

moral = 80
moral_max = 100
moral_min = 50

staerke = 20000
staerke_max = 35000
staerke_min = 10000

gegner = 20000
gegner_max = 20000
gegner_min = 1000


#tutorial
print(colored("Willkommen Spieler,\nWas du gleich erleben wirst, ist ein textbasiertes Spiel.\nDas bedeutet: Die Geschichte entfaltet sich allein durch Worte – deine Vorstellungskraft ist deine stärkste Waffe.\nDu wirst lesen, entscheiden und handeln, nur durch Text.\n\nDu bekommst Situationen beschrieben – manchmal ruhig, manchmal dramatisch –\nund **du wählst aus**, wie dein Charakter reagiert.\n\nManche Entscheidungen verändern den Lauf der Geschichte.\nAndere beeinflussen deine Truppe, die Moral – oder sogar dein Überleben.\nEs gibt **kein richtig oder falsch** – nur Konsequenzen.\n\nUm zu spielen, lies aufmerksam und entscheide dann:\n→ „Will ich kämpfen oder verhandeln?“\n→ „Vertraue ich dem Boten – oder lockt er in eine Falle?“\n **Deine Wahl formt die Geschichte.**","light_green")),
input("Wenn du fertig gelesen hast Drücke Enter (Das gilt für alle Texte in dem Spiel)")



next_decision = "tutorial"

with open('decisions.json', 'r') as file:
    data = json.load(file)

config = data.get("config", [])

def change_values(values):
    global zufriedenheit
    global zufriedenheit_min
    global zufriedenheit_max
    global staerke
    global staerke_max
    global staerke_min
    global moral
    global moral_max
    global moral_min
    global gegner
    global gegner_max
    global gegner_min
    ret_value = True

    zufriedenheit = zufriedenheit + values[0]
    if zufriedenheit > zufriedenheit_max:
        zufriedenheit = zufriedenheit_max

    if zufriedenheit < zufriedenheit_min:
        print("Zufriedenheit der Truppe ist zu niedrig!")
        ret_value = False

    staerke = staerke + values[1]
    if staerke > staerke_max:
        staerke = staerke_max

    if staerke < staerke_min:
        print("du hast nicht genug Truppen um sie zu besiegen")
        ret_value = False

    moral = moral + values[2]
    if moral > moral_max:
        moral = moral_max

    if moral < moral_min:
        print("Die Moral deiner Truppe ist schlecht, sie wenden sich gegen dich.")
        ret_value = False

    gegner = gegner + values[3]
    if gegner > gegner_max:
        gegner = gegner_max

    if gegner < gegner_min:
        print("Glückwunsch du hast die Goten besiegt!")
        ret_value = False
    
    
    return ret_value


def load_decision(name):
    for decision in data.get("decisions", []):
        if decision["name"] == name:
            return decision

while True:
    clear_console()
    current_decision = load_decision(next_decision)

    print(color.UNDERLINE + color.DARKCYAN + current_decision["text"] + color.END)

    if current_decision["dead_end"] == "yes" or current_decision["end_of_game"] == "yes":
        exit()

    input("")

    print(color.BOLD + color.GREEN + "Eigene Stärke:")
    print(staerke)
    print("")
    print(color.BOLD + color.CYAN + "Moral in %:")
    print(moral)
    print("")
    print(color.BOLD + color.RED + "Gegener Stärke:")
    print(gegner)
    print(color.END)

    print(current_decision["question"])
    print("")
    for antwort in current_decision.get("answers", []):
        print("[" + antwort["nummer"] + "]" + " " + antwort["question"])
    print("")
    entscheidung = input("Wie lautet deine Entscheidung?: ")


    for antwort in current_decision.get("answers", []):
        if entscheidung == antwort["nummer"]:
            next_decision = antwort["target"]
            values = antwort["values"]
            if change_values(values) == False:
                print("Sorry you lost, no bonus, try better next time")
                exit()