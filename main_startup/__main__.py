# Copyright (C) 2020-2021 by TeamTezer@Github, < https://github.com/TeamTezer >.
#
# This file is part of < https://github.com/TeamTezer/TezerUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamTezer/blob/master/LICENSE >
#
# All rights reserved.

import logging
import os
import platform

import pyrogram
from pyrogram import __version__
from bot_utils_files.Localization.engine import Engine
from database.localdb import check_lang
from main_startup import (
    Tezer,
    Tezer2,
    Tezer3,
    Tezer4,
    bot,
    Tezer_version,
    mongo_client,
)
from main_startup.core.startup_helpers import (
    load_plugin,
    load_xtra_mod,
    plugin_collecter,
    run_cmd,
    update_it
)

from .config_var import Config


async def mongo_check():
    """Check Mongo Client"""
    try:
        await mongo_client.server_info()
    except BaseException as e:
        logging.error("Something Isn't Right With Mongo! Please Check Your URL")
        logging.error(str(e))
        quit(1)


async def load_unofficial_modules():
    """Load Extra Plugins."""
    logging.info("Loading X-Tra Plugins!")
    await run_cmd(f'bash bot_utils_files/other_helpers/xtra_plugins.sh {Config.XTRA_PLUGINS_REPO}')
    xtra_mods = plugin_collecter("./xtraplugins/")
    for mods in xtra_mods:
        try:
            load_xtra_mod(mods)
        except Exception as e:
            logging.error(
                "[USER][XTRA-PLUGINS] - Failed To Load : " + f"{mods} - {str(e)}"
            )


async def fetch_plugins_from_channel():
    """Fetch Plugins From Channel"""
    try:
        async for message in Tezer.search_messages(
            Config.PLUGIN_CHANNEL, filter="document", query=".py"
        ):
            hmm = message.document.file_name
            if not os.path.exists(os.path.join("./plugins/", hmm)):
                await Tezer.download_media(message, file_name="./plugins/")
    except BaseException as e:
        logging.error(f"Failed! To Install Plugins From Plugin Channel Due To {e}!")
        return
    logging.info("All Plugins From Plugin Channel Loaded!")


async def run_bot():
    try:
        await update_it()
    except:
        pass
    """Run The Bot"""
    await mongo_check()
    if bot:
        await bot.start()
        bot.me = await bot.get_me()
        assistant_mods = plugin_collecter("./assistant/")
        for mods in assistant_mods:
            try:
                load_plugin(mods, assistant=True)
            except Exception as e:
                logging.error("[ASSISTANT] - Failed To Load : " + f"{mods} - {str(e)}")
    await Tezer.start()
    Tezer.me = await Tezer.get_me()
    Tezer.selected_lang = await check_lang()
    LangEngine = Engine()
    LangEngine.load_language()
    Tezer.has_a_bot = bool(bot)
    if Tezer2:
        await Tezer2.start()
        Tezer2.me = await Tezer2.get_me()
        Tezer2.has_a_bot = True if bot else False
    if Tezer3:
        await Tezer3.start()
        Tezer3.me = await Tezer3.get_me()
        Tezer3.has_a_bot = bool(bot)
    if Tezer4:
        await Tezer4.start()
        Tezer4.me = await Tezer4.get_me()
        Tezer4.has_a_bot = bool(bot)
    if Config.PLUGIN_CHANNEL:
        await fetch_plugins_from_channel()
    needed_mods = plugin_collecter("./plugins/")
    for nm in needed_mods:
        try:
            load_plugin(nm)
        except Exception as e:
            logging.error("[USER] - Failed To Load : " + f"{nm} - {str(e)}")
    if Config.LOAD_UNOFFICIAL_PLUGINS:
        await load_unofficial_modules()
    full_info = f"""Tezer Based On Pyrogram V{__version__}
Python Version : {platform.python_version()}
Tezer Version : {Tezer_version}
You Can Visit @TezerSupportOfficial For Updates And @TezerChat For Any Query / Help!
"""
    logging.info(full_info)
    await pyrogram.idle()


if __name__ == "__main__":
    Tezer.loop.run_until_complete(run_bot())
