from pocketfurnace.utils.config.JsonConfig import JsonConfig

config = JsonConfig(r"C:\Users\Jose Luis\Downloads\Servidor\PocketFurnace\test.json", {
    "ping": "pong"
})
config.remove("pong")

print(config.get("ping"))
