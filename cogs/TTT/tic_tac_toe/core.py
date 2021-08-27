import asyncio
import itertools
import discord
import random
import json
from cogs.TTT.tic_tac_toe.config import CONFIG
from enum import Enum
from discord.ext import tasks
import traceback
from discord.ext.commands.errors import EmojiNotFound


class Move(Enum):
    empty = "empty"
    x = "x"
    o = "o"


class TicTacToe:
    def __init__(self, ctx, users,amount, *, config=None):
        self.ctx = ctx
        self.bot = ctx.bot
        self.users = users
        self._board = [Move.empty for _ in range(9)]
        random.shuffle(users)
        self._moves = {users[0]: Move.x, users[1]: Move.o}
        self._cycle_users = itertools.cycle(users)
        self._turn_of = next(self._cycle_users)
        self.message = None
        self.winner = None
        self._config = config or {}
        self.refactor_config()
        self.remaining_moves()

        self.amount = amount
        self.player1 = ctx.author
        self.player2 = users[1]
        if self.player2 == ctx.author:
            self.player2 = users[0]

    @property
    def emoji_board(self):
        return [self.config[move.value] for move in self._board]

    def refactor_config(self):
        self.config = {}
        _config = self._config.copy()
        for slot in CONFIG._slots:
            try:
                value = _config.pop(slot)
            except KeyError:
                value = getattr(CONFIG, slot)

            if isinstance(value, int):
                emoji = self.bot.get_emoji(value)
                if emoji is None:
                    raise EmojiNotFound(value)
            elif isinstance(value, str):
                emoji = value
            else:
                raise RuntimeError(
                    "Emoji must either be a discord snowflake or a unicode character."
                )

            self.config[slot] = emoji

        if len(_config) > 0:
            raise RuntimeError("Invalid configuration values.")

    def remaining_moves(self):
        self._remaining_moves = {}
        for idx, slot in enumerate(CONFIG._slots[3:]):
            key = str(self.config[slot])
            self._remaining_moves[key] = idx

    def board_to_embed(self):
        embed = discord.Embed(
            title=f":x::o::x: Tic Tac Toe :x::o::x:", 
            description = f"{self.users[0].mention} vs {self.users[1].mention}",
            color=0x00ffff,
        )
        board = self.emoji_board
        messages = []
        if len(self._remaining_moves) == 0 and self.winner is None:
            messages.append("It's a Draw!\n")
            self.stop()
            
        elif self.winner is None and len(self._remaining_moves) > 0:
            messages.append(
                f"{self._turn_of.mention}'s Turn **({self._moves[self._turn_of].value.upper()})**\n"
            )
        elif self.winner is not None:
            messages.append(f"{self.winner.mention} Wins!\n")

        # This statement creates board
        messages.append(
            "\n".join(
                "\u200b".join(board[i] for i in range(j, j + 3)) for j in range(0, 9, 3)
            ),
        )

        embed.description = "\n".join(messages)
        return embed

    @tasks.loop()
    async def runner(self):
        check = (
            lambda payload: payload.user_id == self._turn_of.id
            and str(payload.emoji) in self._remaining_moves
            and payload.message_id == self.message.id
        )
        try:
            payload = await self.bot.wait_for(
                "raw_reaction_add", check=check, timeout=30
            )
            emoji = str(payload.emoji)
        except asyncio.TimeoutError:
            self.stop()
            await self.ctx.reply(f"{self._turn_of.mention} didn't select fast enough.")
        else:
            await self.run_move(self._turn_of, emoji)

    def stop(self):
        self.runner.stop()

    def determine_winner(self):
        rows = []
        board = self._board

        # Horizontal _
        for i in range(0, 9, 3):
            rows.append(board[i : i + 3])

        # Verticle |
        for i in range(3):
            rows.append(board[i::3])

        # \ Diagonal
        rows.append(board[::4])

        # / Diagonal
        rows.append(board[2:-1:2])
        for row in rows:
            if row.count(row[0]) == len(row) and row[0] != Move.empty:
                self.stop()
                return self._turn_of

    async def run_move(self, member, emoji):
        move = self._remaining_moves.pop(emoji)
        self._board[move] = self._moves[member]
        self.winner = self.determine_winner()
        if self.winner == self.users[0]:
            self.loser = self.users[1]
        else:
            self.loser = self.users[0]
        self._turn_of = next(self._cycle_users)
        embed = self.board_to_embed()
        await self.message.edit(embed=embed)
        if self.winner is None:
            await self.message.clear_reaction(emoji)
        else:
            await self.message.clear_reactions()

    @runner.error
    async def error(self, e):
        traceback.print_exc()

    async def send_initial_message(self):
        embed = self.board_to_embed()
        self.message = await self.ctx.send(embed=embed)

    async def apply_reactions(self):
        for move in list(self.config.values())[3:]:
            await self.message.add_reaction(move)

    async def start(self):
        await self.send_initial_message()
        await self.apply_reactions()
        self.runner.start()

    