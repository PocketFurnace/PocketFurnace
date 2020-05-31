from pocketfurnace.raknet.server import PyRakLibServer, ServerHandler
from pocketfurnace.raknet.utils.InternetAddress import InternetAddress

raklib = PyRakLibServer.PyRakLibServer(InternetAddress("192.168.0.24", 19132, 4))
handler = ServerHandler.ServerHandler(raklib, None)
handler.send_option("name", "MCPE;PocketFurnace powered server;390;1.14.60;0;10;0;PocketFurnacePoweredServer;0")
handler.send_option("packetLimit", "1")
handler.send_option("portChecking", "True")
