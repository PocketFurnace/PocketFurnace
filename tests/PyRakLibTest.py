from pocketfurnace.raknet.server import PyRakLibServer, ServerHandler
from pocketfurnace.raknet.utils.InternetAddress import InternetAddress

raklib = PyRakLibServer.PyRakLibServer(InternetAddress("0.0.0.0", 19132, 4))
handler = ServerHandler.ServerHandler(raklib, None)
handler.send_option("servername", "MCPE;PocketFurnace;390 390;1.14.60;0;10")
