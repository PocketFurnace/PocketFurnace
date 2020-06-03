from pocketfurnace.PocketFurnace import PocketFurnace
from pocketfurnace.utils.config.PropertiesConfig import PropertiesConfig
import base64
import time
import os

# license
license_done = False
# lang
lang_code = None
lang_done = False


print(PocketFurnace.logo)
print("Version: " + str(PocketFurnace.version))
print("API: " + str(PocketFurnace.api))
print("Authors: " + PocketFurnace.authors)

time.sleep(2.4)

while not license_done:
    print("Alguna licencia")
    print("You accept the license [y/n]: ")
    license = input()

    if license == "y":
        license_done = True
    elif license == "n":
        print("Ending the program...")
        time.sleep(1.9)
        exit(1)


while not lang_done and license_done:
    print("English => eng")
    print("Spanish => esp")
    print("Select a language: ")
    lang = input()

    if lang == "eng" or lang == "esp":
        lang_code = lang
        lang_done = True


while license_done and lang_done:
    print("Generating resources [server.properties]..... 15%")
    properties = PropertiesConfig("path_include?" + "server.properties") # require instance
    # general server properties
    properties.set("SERVER_GENERAL", "motd", "MCPE Server running on PocketFurnace")
    properties.set("SERVER_GENERAL", "sub-motd", "PocketFurnace")
    properties.set("SERVER_GENERAL", "server-port", 19132)
    properties.set("SERVER_GENERAL", "language", lang_code)
    properties.set("SERVER_GENERAL", "max-players", 20)
    properties.set("SERVER_GENERAL", "white-list", False)
    properties.set("SERVER_GENERAL", "hardcore", False)
    properties.set("SERVER_GENERAL", "pvp", True)
    properties.set("SERVER_GENERAL", "force-gamemode", False)
    properties.set("SERVER_GENERAL", "force-resources", False)
    properties.set("SERVER_GENERAL", "bug-report", True)

    # world properties
    properties.set("WORLD", "announce-player-achievements", True)
    properties.set("WORLD", "spawn-protection", 16)
    properties.set("WORLD", "gamemode", 0)
    properties.set("WORLD", "difficulty", 1)
    properties.set("WORLD", "view-distance", 10)
    properties.set("WORLD", "auto-save", True)
    properties.set("WORLD", "generator-settings", "")
    properties.set("WORLD", "level-name", "world")
    properties.set("WORLD", "level-seed", "")
    properties.set("WORLD", "level-_type", "DEFAULT")
    properties.set("WORLD", "spawn-animals", False)
    properties.set("WORLD", "spawn-mobs", True)
    properties.set("WORLD", "allow-flight", False)
    properties.set("WORLD", "allow-nether", False)
    properties.set("WORLD", "allow-end", False)
    properties.set("WORLD", "achievements", False)
    # network properties
    properties.set("NETWORK", "enable-query", True)
    properties.set("NETWORK", "enable-rcon", False)
    properties.set("NETWORK", "rcon.password", base64.b64encode(os.urandom(20))[3:10].decode())
    # auth properties
    properties.set("AUTH", "xbox-auth", True)
    time.sleep(2.2)
    print("Generating resources..... 30%")
    time.sleep(1.2)
    print("Generating resources..... 60%")
    time.sleep(2.2)
    print("Generating resources..... 85%")
    time.sleep(2.2)
    print("Generating resources..... 100%")
    time.sleep(2.2)
    # normal start server
    exit(1)








