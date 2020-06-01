from pocketfurnace.raknet.server import PyRakLibServer, ServerHandler
from pocketfurnace.raknet.utils.InternetAddress import InternetAddress

raklib = PyRakLibServer.PyRakLibServer(InternetAddress("0.0.0.0", 19132, 4))
handler = ServerHandler.ServerHandler(raklib, None)
handler.send_option("name", "MCPE;PocketFurnace Server;390;1.14.60;0;10;0;PocketFurnace;Survival".encode("UTF-8"))
