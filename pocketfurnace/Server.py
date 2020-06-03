import base64
import os
from pathlib import Path
from logzero import logger
from pocketfurnace.utils.config.PropertiesConfig import PropertiesConfig
from pocketfurnace.utils.config.YamlConfig import YamlConfig


class ServerError(Exception):
    pass


class Server:
    BROADCAST_CHANNEL_ADMINISTRATIVE = "pocketfurnace.broadcast.admin"
    BROADCAST_CHANNEL_USERS = "pocketfurnace.broadcast.user"

    tick_sleeper = None
    ban_by_name = None
    ban_by_ip = None
    operators = None
    whitelist = None
    is_running = True
    has_stopped = False
    plugin_manager = None
    profiling_tickrate = 20
    updater = None
    async_pool = None
    """counts the ticks since the server start"""
    tick_counter = 0
    next_tick = 0
    tick_average = {20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20}
    use_average = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
    current_tps = 20
    current_use = 0

    do_title_tick = True
    send_usage_ticker = 0
    dispatch_signals = False
    logger = None
    memory_manager = None
    console = None
    command_map = None
    crafting_manager = None
    resource_manager = None
    max_players = None
    online_mode = True
    auto_save = None
    rcon = None

    entity_metadata = None
    player_metadata = None
    level_metadata = None

    network = None
    network_compression_async = None

    auto_tick_rate = True
    auto_tick_rate_limit = 20
    always_tick_players = False
    base_tick_rate = 1

    auto_save_ticker = 0
    auto_save_ticks = 6000

    language = None
    force_language = False

    server_id = None

    auto_loader = None
    data_path = None
    plugin_path = None

    unique_players = None

    query_handler = None

    query_regenerate_task = None

    # properties: Jose will add the properties stuff
    property_cache = []

    config = None
    players = None
    logged_in_players = None
    player_list = None
    levels = None
    level_default = None

    def __init__(self, data_path, plugin_path):
        self.instance = self

        # TODO: SleeperHandler
        self.tick_sleeper = ''

        try:
            if not Path(data_path + "worlds/").is_dir():
                os.mkdir(data_path + "worlds/", 0o777)

            if not Path(data_path + "players/").is_dir():
                os.mkdir(data_path + "players/", 0o777)

            if not Path(plugin_path).is_dir():
                os.mkdir(plugin_path, 0o777)

            self.data_path = os.path.realpath(data_path)
            self.plugin_path = os.path.realpath(plugin_path)

            logger.info("Loading pocketfurnace.yml")
            if not os.path.exists(data_path + "pocketfurnace.yml"):
                # testing for some entries in pocketfurnace.yml
                config = YamlConfig(data_path + "pocketfurnace.yml", {
                    "test": "test"
                })
                config.save()

            logger.info("Loading server properties...")
            if not os.path.exists(data_path + "server.properties"):
                # general server properties
                properties = PropertiesConfig(data_path + "server.properties")
                properties.set("SERVER_GENERAL", "motd", "MCPE Server running on PocketFurnace")
                properties.set("SERVER_GENERAL", "sub-motd", "PocketFurnace")
                properties.set("SERVER_GENERAL", "server-port", 19132)
                properties.set("SERVER_GENERAL", "language", "eng")
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

            # based on pmmp entries, remember separate this in sections as planned
            properties = PropertiesConfig(data_path + "server.properties")
            conf_sec = dict()
            conf_sec["motd"] = properties.getString("SERVER_GENERAL", "motd")
            conf_sec["sub-motd"] = properties.getString("SERVER_GENERAL", "sub-motd")
            conf_sec["server-port"] = properties.getInt("SERVER_GENERAL", "server-port")
            conf_sec["server-ip"] = "0.0.0.0"
            conf_sec["view-distance"] = properties.getInt("WORLD", "view-distance")
            conf_sec["white-list"] = properties.getBoolean("SERVER_GENERAL", "white-list")
            conf_sec["achievements"] = properties.getBoolean("WORLD", "achievements")
            conf_sec["announce-player-achievements"] = properties.getBoolean("WORLD", "announce-player-achievements")
            conf_sec["spawn-protection"] = properties.getInt("WORLD", "spawn-protection")
            conf_sec["max-players"] = properties.getInt("SERVER_GENERAL", "max-players")
            conf_sec["allow-flight"] = properties.getBoolean("WORLD", "allow-flight")
            conf_sec["spawn-animals"] = properties.getBoolean("WORLD", "spawn-animals")
            conf_sec["spawn-mobs"] = properties.getBoolean("WORLD", "spawn-mobs")
            conf_sec["gamemode"] = properties.getInt("WORLD", "gamemode")
            conf_sec["force-gamemode"] = properties.getBoolean("SERVER_GENERAL", "force-gamemode")
            conf_sec["hardcore"] = properties.getBoolean("SERVER_GENERAL", "hardcore")
            conf_sec["pvp"] = properties.getBoolean("SERVER_GENERAL", "pvp")
            conf_sec["difficulty"] = properties.getInt("WORLD", "difficulty")
            conf_sec["generator-settings"] = properties.getString("WORLD", "generator-settings")
            conf_sec["level-name"] = properties.getString("WORLD", "level-name")
            conf_sec["level-seed"] = properties.getString("WORLD", "level-seed")
            conf_sec["level-_type"] = properties.getString("WORLD", "level-_type")
            conf_sec["allow-nether"] = properties.getBoolean("WORLD", "allow-nether")
            conf_sec["allow-end"] = properties.getBoolean("WORLD", "allow-end")
            conf_sec["enable-query"] = properties.getBoolean("NETWORK", "enable-query")
            conf_sec["enable-rcon"] = properties.getBoolean("NETWORK", "enable-rcon")
            conf_sec["rcon.password"] = properties.getString("NETWORK", "rcon.password")
            conf_sec["auto-save"] = properties.getBoolean("WORLD", "auto-save")
            conf_sec["force-resources"] = properties.getBoolean("SERVER_GENERAL", "force-resources")
            conf_sec["bug-report"] = properties.getBoolean("SERVER_GENERAL", "force-resources")
            conf_sec["xbox-auth"] = properties.getBoolean("AUTH", "bug-report")
            self.async_pool = 0
            logger.info("pocketfurnace.server.start")
        except ServerError as e:
            logger.error(e)
            pass

    @staticmethod
    def get_name() -> str:
        return 'pocket furnace'

    def get_data_path(self) -> str:
        return self.data_path

    def get_plugin_path(self) -> str:
        return self.plugin_path

    def get_max_players(self) -> int:
        return self.max_players

    def get_online_mode(self) -> bool:
        return self.get_online_mode()

    def requires_authentication(self) -> bool:
        return self.get_online_mode()

    def has_auto_save(self):
        return self.auto_save

    # ClassLoader - not needed
    def get_loader(self):
        return self.auto_loader

    def get_entity_metadata(self):
        return self.entity_metadata

    def get_player_metadata(self):
        return self.player_metadata

    def get_level_metadata(self):
        return self.level_metadata

    def get_updater(self):
        return self.updater

    def get_plugin_manager(self):
        return self.plugin_manager

    def get_crafting_manager(self):
        return self.crafting_manager

    def get_resource_pack_manager(self):
        return self.resource_manager

    def get_async_pool(self):
        return self.async_pool

    def get_tick(self) -> int:
        return self.tick_counter

    def get_tick_per_second(self) -> float:
        return round(self.current_tps, 2)

    def get_tick_per_second_average(self) -> float:
        return round((sum(self.use_average) / len(self.use_average)) * 100, 2)

    def get_command_map(self):
        return self.command_map

    def get_logged_in_players(self):
        return self.logged_in_players

    def get_online_players(self):
        return self.player_list

    def get_default_level(self):
        return self.level_default

    def get_name_bans(self):
        return self.ban_by_name

    def get_ip_bans(self):
        return self.ban_by_ip

    def get_whitelisted(self):
        return self.get_whitelisted()

    def get_ops(self):
        return self.operators

    def get_tick_sleeper(self):
        return self.tick_sleeper

    def get_language(self):
        return self.language

    def is_language_forced(self) -> bool:
        return self.force_language

    def get_network(self):
        return self.network()

    def get_memory_manager(self):
        return self.memory_manager

    def __sleep(self):
        raise ValueError("Cannot serialize Server instance")
