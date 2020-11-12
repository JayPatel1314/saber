from tg_bot import oko
import os
import time
from telethon import types
from telethon.tl import functions
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import ContentTooShortError
from youtube_dl.utils import DownloadError
from youtube_dl.utils import ExtractorError
from youtube_dl.utils import GeoRestrictedError
from youtube_dl.utils import MaxDownloadsReached
from youtube_dl.utils import PostProcessingError
from youtube_dl.utils import UnavailableVideoError
from youtube_dl.utils import XAttrMetadataError
from tg_bot.events import register
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError


@register(pattern="^/yt(audio|video) (.*)")
async def download_video(v_url):
    
    """ For .ytdl command, download media from YouTube and many other sites. """
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()
    lmao = await v_url.reply("`Preparing to download...`")
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "256",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    elif type == "video":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        await lmao.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await lmao.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await lmao.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await lmao.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await lmao.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await lmao.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await lmao.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await lmao.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await lmao.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await lmao.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await lmao.edit(
            f"`Preparing to upload song:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await tbot.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data["duration"]),
                    title=str(ytdl_data["title"]),
                    performer=str(ytdl_data["uploader"]),
                )
            ],
        )
        os.remove(f"{ytdl_data['id']}.mp3")
    elif video:
        await lmao.edit(
            f"`Preparing to upload video:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await tbot.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            caption=ytdl_data["title"],
        )
        os.remove(f"{ytdl_data['id']}.mp4")

from tg_bot import CMD_HELP
global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo=  file_help.replace("_", " ")

__help__ = """
 - /yt <text>: perform a youtube search
 - /ytaudio <link> or /ytvideo <link>: Downlods a video or audio from a youtube video to the bots local server
"""
__mod_name__ = "Yt"

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
