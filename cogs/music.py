import asyncio
import functools
import itertools
import math
import random
import traceback
import discord
from discord.ext.commands import bot
import youtube_dl
from async_timeout import timeout
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''

try:

    client_id = 'fb529738c6244f9fa269bdf28ec76881'
    client_secret = 'cca9008a801c4c93a8c94a3823ea10af'

    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    try:
        class VoiceError(Exception):
            pass


        class YTDLError(Exception):
            pass


        class YTDLSource(discord.PCMVolumeTransformer):
            YTDL_OPTIONS = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                'restrictfilenames': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'auto',
                'source_address': '0.0.0.0',
            }

            FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn',
            }

            ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

            def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
                super().__init__(source, volume)

                self.requester = ctx.author
                self.channel = ctx.channel
                self.data = data

                self.uploader = data.get('uploader')
                self.uploader_url = data.get('uploader_url')
                date = data.get('upload_date')
                self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
                self.title = data.get('title')
                self.thumbnail = data.get('thumbnail')
                self.description = data.get('description')
                self.duration = self.parse_duration(int(data.get('duration')))
                self.tags = data.get('tags')
                self.url = data.get('webpage_url')
                self.views = data.get('view_count')
                self.likes = data.get('like_count')
                self.dislikes = data.get('dislike_count')
                self.stream_url = data.get('url')

            def __str__(self):
                return '**{0.title}** by **{0.uploader}**'.format(self)

            @classmethod
            async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
                loop = loop or asyncio.get_event_loop()

                partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
                data = await loop.run_in_executor(None, partial)

                if data is None:
                    raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

                if 'entries' not in data:
                    process_info = data
                    webpage_url = process_info['webpage_url']

                else:
                    process_info = None
                    for entry in data['entries']:
                        urllist = list(data['entries'])
                        chklist = []
                        for x in urllist:
                            chklist.append(x.get('url'))
                        return chklist

                    if process_info is None:
                        raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

                    webpage_url = process_info['url']

                partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
                processed_info = await loop.run_in_executor(None, partial)

                if processed_info is None:
                    raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

                if 'entries' not in processed_info:
                    info = processed_info
                else:
                    info = None
                    while info is None:
                        try:
                            info = processed_info['entries'].pop(0)
                        except IndexError:
                            raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))
                return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

            @staticmethod
            def parse_duration(duration: int):
                minutes, seconds = divmod(duration, 60)
                hours, minutes = divmod(minutes, 60)
                days, hours = divmod(hours, 24)

                duration = []
                if days > 0:
                    duration.append('{} days'.format(days))
                if hours > 0:
                    duration.append('{} hours'.format(hours))
                if minutes > 0:
                    duration.append('{} minutes'.format(minutes))
                if seconds > 0:
                    duration.append('{} seconds'.format(seconds))

                return ', '.join(duration)


        class Song:
            __slots__ = ('source', 'requester')

            def __init__(self, source: YTDLSource):
                self.source = source
                self.requester = source.requester

            def create_embed(self):
                embed = (discord.Embed(title='Now playing',
                                    description='```css\n{0.source.title}\n```'.format(self),
                                    color=discord.Color.random())
                        .add_field(name='Duration', value=self.source.duration)
                        .add_field(name='Requested by', value=self.requester.mention)
                        .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                        .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                        .set_thumbnail(url=self.source.thumbnail))

                return embed


        class SongQueue(asyncio.Queue):
            def __getitem__(self, item):
                if isinstance(item, slice):
                    return list(itertools.islice(self._queue, item.start, item.stop, item.step))
                else:
                    return self._queue[item]

            def __iter__(self):
                return self._queue.__iter__()

            def __len__(self):
                return self.qsize()

            def clear(self):
                self._queue.clear()

            def shuffle(self):
                random.shuffle(self._queue)

            def remove(self, index: int):
                del self._queue[index]


        class VoiceState:
            def __init__(self, bot: commands.Bot, ctx: commands.Context):
                self.bot = bot
                self._ctx = ctx

                self.current = None
                self.voice = None
                self.next = asyncio.Event()
                self.songs = SongQueue()

                self._loop = False
                self._volume = 0.5
                self.skip_votes = set()

                self.audio_player = bot.loop.create_task(self.audio_player_task())

            def __del__(self):
                self.audio_player.cancel()

            @property
            def loop(self):
                return self._loop

            @loop.setter
            def loop(self, value: bool):
                self._loop = value

            @property
            def volume(self):
                return self._volume

            @volume.setter
            def volume(self, value: float):
                self._volume = value

            @property
            def is_playing(self):
                return self.voice and self.current

            async def audio_player_task(self):
                while True:
                    self.next.clear()

                    if not self.loop:
                        # Try to get the next song within 3 minutes.
                        # If no song will be added to the queue in time,
                        # the player will disconnect due to performance
                        # reasons.
                        try:
                            async with timeout(180):  # 3 minutes
                                self.current = await self.songs.get()
                        except asyncio.TimeoutError:
                            self.bot.loop.create_task(self.stop())
                            return

                    self.current.source.volume = self._volume
                    self.voice.play(self.current.source, after=self.play_next_song)
                    await self.current.source.channel.send(embed=self.current.create_embed())

                    await self.next.wait()

            def play_next_song(self, error=None):
                if error:
                    raise VoiceError(str(error))

                self.next.set()

            def skip(self):
                self.skip_votes.clear()

                if self.is_playing:
                    self.voice.stop()

            async def stop(self):
                self.songs.clear()

                if self.voice:
                    await self.voice.disconnect()
                    self.voice = None
    except:
        print(f"```{traceback.format_exc()}```")


    class Music(commands.Cog):
        try:
            def __init__(self, bot: commands.Bot):
                self.bot = bot
                self.voice_states = {}

            def get_voice_state(self, ctx: commands.Context):
                state = self.voice_states.get(ctx.guild.id)
                if not state:
                    state = VoiceState(self.bot, ctx)
                    self.voice_states[ctx.guild.id] = state

                return state

            def cog_unload(self):
                for state in self.voice_states.values():
                    self.bot.loop.create_task(state.stop())

            def cog_check(self, ctx: commands.Context):
                if not ctx.guild:
                    raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

                return True

            async def cog_before_invoke(self, ctx: commands.Context):
                ctx.voice_state = self.get_voice_state(ctx)

            async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
                await ctx.send('An error occurred: {}'.format(str(error)))

            @commands.command(name='join', invoke_without_subcommand=True)
            async def _join(self, ctx: commands.Context):
                """Joins a voice channel."""

                destination = ctx.author.voice.channel
                if ctx.voice_state.voice:
                    await ctx.voice_state.voice.move_to(destination)
                    return

                ctx.voice_state.voice = await destination.connect()

            @commands.command(name='leave', aliases=['disconnect'])
            async def _leave(self, ctx: commands.Context):
                """Clears the queue and leaves the voice channel."""

                if not ctx.voice_state.voice:
                    return await ctx.send('Not connected to any voice channel.')

                await ctx.voice_state.stop()
                del self.voice_states[ctx.guild.id]

        except:
            print(f"```{traceback.format_exc()}```")
            
        @commands.command()
        async def splaylist(self,ctx,arg):
            try:
                if not ctx.voice_state.voice:
                    await ctx.invoke(self._join)
                
                msg = await ctx.send("**Queueing Playlist** <a:loading:869964972594192414>")
                    
                def getTrackIDs(user, playlist_id):
                    ids = []
                    playlist = sp.user_playlist(user, playlist_id)
                    for item in playlist['tracks']['items']:
                        track = item['track']
                        ids.append(track['id'])
                    return ids

                url= f'{arg}'
                ids = getTrackIDs('aksljhd', url)

                def getTrackFeatures(id):
                    meta = sp.track(id)

                    # meta
                    name = meta['name']
                    artist = meta['album']['artists'][0]['name']

                    
                    track = f"{name} - {artist}"
                    return track
                
                # loop over track ids 
                tracks = []
                for i in range(len(ids)):
                    track = getTrackFeatures(ids[i])
                    tracks.append(track)

                for url in tracks:
                    try:
                        source = await YTDLSource.create_source(ctx, url, loop=self.bot.loop)
                    except:
                        continue
                    song = Song(source)
                    await ctx.voice_state.songs.put(song)

                embed = discord.Embed(title="Queued Playlist",description=f"```Ignore this idk how to get playlist names```", color=discord.Colour.random())
                embed.add_field(name='Requested By', value=ctx.author.mention)
                embed.add_field(name='URL', value=f"[Click]({arg})")
                embed.set_thumbnail(url='https://c.tenor.com/D_F--PvRH4wAAAAi/pepe-listening-to-music.gif')

                await msg.delete()
                await ctx.send(embed=embed)
            
            except:
                print(f"```{traceback.format_exc()}```")

        # @commands.command()
        # async def splay(self,ctx,arg):
        #     try:
        #         if not ctx.voice_state.voice:
        #             await ctx.invoke(self._join)
        #         search = sp.search(arg)
        #         track = search['track']
        #         id = track['id']
                
        #         print(search)
        #     except:
        #         print(f"```{traceback.format_exc()}```")

        @commands.command(name='now', aliases=['current', 'playing'])
        async def _now(self, ctx: commands.Context):
            """Displays the currently playing song."""

            await ctx.send(embed=ctx.voice_state.current.create_embed())

        @commands.command(name='clear')
        async def _clear(self, ctx: commands.Context):
        #Clears Queue
            ctx.voice_state.songs.clear()

            await ctx.send('**Cleared Queue**')

        @commands.command(name='skip')
        async def _skip(self, ctx: commands.Context):
            if not ctx.voice_state.is_playing:
                return await ctx.send('Not playing any music right now...')

            await ctx.message.add_reaction('⏭')
            try:
                ctx.voice_state.skip()
            except:
                await ctx.send(f"```{traceback.format_exc()}```")

        @commands.command(name='queue')
        async def _queue(self, ctx: commands.Context, *, page: int = 1):
            """Shows the player's queue.
            You can optionally specify the page to show. Each page contains 10 elements.
            """

            if len(ctx.voice_state.songs) == 0:
                return await ctx.send('Empty queue.')

            items_per_page = 10
            pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

            start = (page - 1) * items_per_page
            end = start + items_per_page

            queue = ''
            for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
                queue += '`{0}.` [{1.source.title}]({1.source.url})\n'.format(i + 1, song)

            chkvar = ctx.voice_state.current.source.title
            finalvar = f'[{chkvar}]({ctx.voice_state.current.source.url})'
            embed = (discord.Embed(title="__Queue__",description='\n__Now Playing:__\n{}\n\n__Up Next:__\n{}\n**{} Tracks Queued**'.format(finalvar, queue,len(ctx.voice_state.songs)), color=discord.Colour.random())
                    .set_footer(text='Viewing Page {}/{}'.format(page, pages)))
            embed.set_thumbnail(url='https://c.tenor.com/D_F--PvRH4wAAAAi/pepe-listening-to-music.gif')
            await ctx.send(embed=embed)

        @commands.command(name='shuffle')
        async def _shuffle(self, ctx: commands.Context):
            """Shuffles the queue."""

            if len(ctx.voice_state.songs) == 0:
                return await ctx.send('Empty queue.')

            ctx.voice_state.songs.shuffle()
            await ctx.message.add_reaction('✅')

        @commands.command(name='delete')
        async def _delete(self, ctx: commands.Context, index: int = None):
            """Removes a song from the queue at a given index."""

            if index == None:
                await ctx.send('Put the number of the song you want to delete from the queue')
                return

            if len(ctx.voice_state.songs) == 0:
                return await ctx.send('Empty queue.')

            ctx.voice_state.songs.remove(index - 1)
            await ctx.message.add_reaction('✅')

        @commands.command(name='play')
        async def _play(self, ctx: commands.Context, *, search: str):
            """Plays a song.
            If there are songs in the queue, this will be queued until the
            other songs finished playing.
            This command automatically searches from various sites if no URL is provided.
            A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
            """
            try:
                if not ctx.voice_state.voice:
                    await ctx.invoke(self._join)

                async with ctx.typing():
                    try:
                        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
                    except Exception as e:
                        await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
                    else:
                        list_check = isinstance(source, list)
                        if list_check:
                            msg = await ctx.send("**Queueing Playlist** <a:loading:869964972594192414>")

                            for url in source:
                                source = await YTDLSource.create_source(ctx, url, loop=self.bot.loop)
                                song = Song(source)
                                await ctx.voice_state.songs.put(song)

                            partial = youtube_dl.YoutubeDL().extract_info(search, download=False,process=False)
                            embed = discord.Embed(title="Queued Playlist",description=f"```{partial['title']}```", color=discord.Colour.random())
                            embed.add_field(name='Requested By', value=ctx.author.mention)
                            embed.add_field(name='Uploader', value=f"[{partial['uploader']}]({partial['uploader_url']})")
                            embed.add_field(name='URL', value=f"[Click]({partial['webpage_url']})")
                            embed.set_thumbnail(url='https://c.tenor.com/D_F--PvRH4wAAAAi/pepe-listening-to-music.gif')

                            await msg.delete()
                            await ctx.send(embed=embed)
                        
                        else:
                            song = Song(source)

                            await ctx.voice_state.songs.put(song)
                            await ctx.send('Queued {}'.format(str(source)))
            except:
                print(f"```{traceback.format_exc()}```")

        @_join.before_invoke
        @_play.before_invoke
        async def ensure_voice_state(self, ctx: commands.Context):
            if not ctx.author.voice or not ctx.author.voice.channel:
                raise commands.CommandError('You are not connected to any voice channel.')

            if ctx.voice_client:
                if ctx.voice_client.channel != ctx.author.voice.channel:
                    raise commands.CommandError('Bot is already in a voice channel.')

except:
    print(f"```{traceback.format_exc()}```")

def setup(client):
    client.add_cog(Music(client))