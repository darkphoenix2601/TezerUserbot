# Copyright (C) 2020-2021 by TeamTezer@Github, < https://github.com/TeamTezer >.
#
# This file is part of < https://github.com/TeamTezer/TezerUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamTezer/blob/master/LICENSE >
#
# All rights reserved.

from database import db_x

bot = db_x["BOT_USERS"]


async def add_user(user_id):
    await bot.insert_one({"user_id": user_id})


async def check_user(user_id):
    Lol = await bot.find_one({"user_id": user_id})
    return bool(Lol)


async def get_all_users():
    return [s async for s in bot.find()]
