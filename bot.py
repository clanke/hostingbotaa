import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
from random import randint
import math
import datetime
from datetime import timedelta, timezone, tzinfo
import asyncio
import html
import time
import discord.utils
from discord.utils import get
import threading
from threading import Timer
import tracemalloc
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import os
import wikipedia

Bot = commands.Bot(command_prefix= '/')

@Bot.event
async def on_ready():
    print('Бот в онлайне')

Bot.remove_command('help')

@commands.command() 
async def inf(ctx, member: discord.Member):
    inm = discord.Embed(title= 'Ифнормация о человеке', color= 0x383a3d)
    inm.add_field(name= 'Никнейм: ', value= "{}".format(member.name))
    inm.add_field(name= 'Дата присоединения на сервер:', value= "{}".format(member.joined_at))
    inm.set_thumbnail(url= member.avatar_url)
    inm.add_field(name= 'Режим:', value= "{}".format(member.activities))
    inm.add_field(name= 'Роли:', value= "{}".format(member.roles))
    inm.set_footer(text= f'Вызвал команду {ctx.message.author.mention}')
    await ctx.send(embed= inm)

@Bot.command() 
@commands.has_any_role('Модераторы','Боярская дума', 'Администратор', 'Глава')
async def unmute(ctx, member: discord.Member, reason= None):
    unmute = discord.utils.get(ctx.guild.roles, id = 657650336718389258)
    if member is None:
        await ctx.send('Укажите пользователя которого нужно размутить')
    elif reason is None:
        await ctx.send('Укажите причину размута')
    else:
        await member.remove_roles(unmute)
        kg = discord.Embed(title= 'Произошол размут', color= 0x383a3d, description= f'{member} Был размучен по причине {reason}')
        kg.set_footer(text= f'Размутил пользователя {member.nick}', icon_url= f'{member.avatar_url}')
        await ctx.send(embed= kg)
        member.send(f'Вы были размучены по причине {reason}')

@Bot.command() 
@commands.has_any_role('Модераторы', 'Боярская дума', 'Администратор', 'Глава')
async def warn(ctx, member: discord.Member, reason= None):
    if member is None:
        await ctx.send('Укажите человека которому нужно сделать варн')
    elif reason is None:
        warned = discord.Embed(title= 'Предупреждение было сделано успешно!', color= 0x383a3d, description= f'{member} был предупреждён \n Прична: None')
        warned.set_footer(text= f'Вызвал бота {ctx.message.author.mention}')
        await ctx.send(embed= warned)
        await member.send(embed= discord.Embed(title= 'Вам было послано предупреждение!', color= 0x383a3d, description= f'Предупреждение было послано от: {ctx.message.author.mention} \n Причина предупреждения: None\n Если у вас появились вопросы напишите команду /complaint и упоминание того модератора который вас замутил'))
    else:
        warning = discord.Embed(title= 'Предупреждение было сделано успешно!', color= 0x383a3d, description= f'{member} был предупреждён \n Прична: {reason}')
        await ctx.send(embed= warning)
        await member.send(f'Вам было послано предупржденике от {ctx.message.author.mention} по причине {reason}')

@Bot.command() 
@commands.has_any_role('Модераторы', 'Смотрящие сервера', 'Руководитель', 'Боярская дума', 'Глава')
async def clear( ctx, amount = 250):
    await ctx.message.delete()
    await ctx.channel.purge(limit = amount)
    em = discord.Embed(description= f'было удаленно *{amount}* сообщений', color = 0x383a3d)
    await ctx.send(embed=em)
    await asyncio.sleep(3)
    await ctx.channel.purge(limit = 1)

@Bot.command() 
@commands.has_any_role('Администратор', 'Боярская дума', 'Глава')
async def ban(ctx, member: discord.Member, reason= None):
    if not member.guild_permissions.administrator:
        await ctx.send('Недостаточно прав')
    elif member.guild_permissions.administrator:
        if member is None:
            await ctx.send('Нужно указать пользователя')
        elif member is ctx.message.author:
            await ctx.send('Себя банить нельзя')
        elif reason is None:
            ctx.guild.ban(member)
            wasban = discord.Embed(title= 'Произошол бан!', color= discord.Colour.red(), description= f'{member} был забанен \n Причина: None')
            wasban.set_footer(text= f'Если вы ошиблись, напишите команду </com>unban, вызвал бота {ctx.message.author.mention}', icon_url= member.avatar_url)
            await ctx.send(embed= wasban)
            member.send(f'Здраствуйте! Вы были забанены на сервере ****Jeff\'s Group**** \n Причина бана: None, если вы хотите разбан подайте пожалуйста на оппеляцию https://docs.google.com/forms/d/e/1FAIpQLSdcNZ2xe-lwm70w7JYOPfVWi-sn7gm9g4R6HHnbNHxp7hkG0A/viewform?usp=sf_link')
        else:
            ctx.guild.ban(member)
            wasban = discord.Embed(title= 'Произошол бан!', color= discord.Colour.red(), description= f'{member} был забанен \n Причина: {reason}')
            wasban.set_footer(text= f'Если вы ошиблись, напишите команду </com>unban, вызвал бота {ctx.message.author.mention}', icon_url= member.avatar_url)
            await ctx.send(embed= wasban)
            member.send(f'Здраствуйте! Вы были забанены на сервере ****Jeff\'s Group**** \n Причина бана {reason}, если вы хотите разбан пожалуйста подайте аппеляцию https://docs.google.com/forms/d/e/1FAIpQLSdcNZ2xe-lwm70w7JYOPfVWi-sn7gm9g4R6HHnbNHxp7hkG0A/viewform?usp=sf_link')
    else:
        await ctx.send('Произошла ошибка')

@Bot.command() 
@commands.has_any_role('Администратор', 'Боярская дума', 'Глава')
async def unban(ctx, member: discord.Member, reason= None):
    if not member.guild_permissions.administrator:
        await ctx.send('у вас недостаточно прав для разбана пользователя')
    elif member.guild_permissions.administrator:
        if member is None:
            await ctx.send('Укажите пользователя которого вам нужно разбанить')
        elif reason is None:
            ctx.guild.unban(member)
            ssss = discord.Embed(title= 'Произошол разбан', color= discord.Colour.blurple(), description= f'{member} был разбанен \n Причина разбана: None')
            ssss.set_footer(text= f'Вызвал бота {ctx.message.author.mention}', icon_url= member.avatar_url)
        else:
            ctx.guild.unban(member)
            ssss = discord.Embed(title= 'Произошол разбан', color= discord.Colour.blurple(), description= f'{member} был разбанен \n Причина разбана: {reason}')
            ssss.set_footer(text= f'Вызвал бота {ctx.message.author.mention}', icon_url= member.avatar_url)
    else:
        await ctx.send('Произошла ошибка, попробуйте снова прописать команду')

@Bot.command() 
@commands.has_any_role('Администратор', 'боярская дума', 'Глава')
async def kick(ctx, member: discord.Member, reason= None):
    if member is None:
        await ctx.send('Укажите пользователя которого вы хотите кикнуть')
    elif reason is None:
        await ctx.guild.kick(member)
        kicked = discord.Embed(title= 'Произошол кик', color= discord.Colour.blue(), description= f'{member} был кикнут с сервера \n причина кика: None')
        kicked.set_footer(text= 'Администрация')
        member.send('Здраствуйте! Вас кикнули с сервера ****Jeff\'s Group**** \n Причина кика: None')
    else:
        await ctx.guild.kick(member)
        kicked = discord.Embed(title= 'Произошол кик', color= discord.Colour.blue(), description= f'{member} был кикнут с сервера \n причина кика: {reason}')
        kicked.set_footer(text= 'Администрация')
        member.send(f'Здраствуйте! Вас кикнули с сервера ****Jeff\'s Group**** \n Причина кика: {reason}')

@Bot.command() 
async def orel(ctx):
    orh = ('Орёл', 'Решка')

    await ctx.send(f'Вам выпал {random.choice(orh)}')

@Bot.command() 
async def reshka(ctx):
    org = ('Орёл', 'Решка')

    await ctx.send(f'Вам выпал {random.choice(org)}')

@Bot.command() 
async def question(ctx):
    md = discord.utils.get(ctx.guild.roles, id = 582137956429594629)
    lmd = discord.utils.get(ctx.guild.roles, id = 582138135497015297)
    br = discord.utils.get(ctx.guild.roles, id = 671342845805854740)
    admin = discord.utils.get(ctx.guild.roles, id = 582137698756591639)
    voproc = discord.utils.get(ctx.guild.roles, id = 701357441605959713)

    number = ('Вопрос38839275928', 'Вопрос9734783279853', 'Вопрос0390910948', 'Вопрос848298923', 'Вопрос7879231948', 'Вопрос0649609069')

    overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
    ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
    md: discord.PermissionOverwrite(read_messages=True),
    lmd: discord.PermissionOverwrite(read_messages=True),
    br: discord.PermissionOverwrite(read_messages=True),
    admin: discord.PermissionOverwrite(read_messages=True),
}

    await ctx.channel.purge(limit= 1)
    ctx.guild.get_role(voproc)
    await ctx.guild.create_text_channel(name= f'{random.choice(number)}', overwrites= overwrites, category= None)
    channel1 = discord.utils.get(ctx.guild.channels, id=637294602919084042)
    await channel1.send(f'@here, у {ctx.message.author.mention} есть вопросы, пожалуйста ответьте на них')

@Bot.command() 
@commands.has_any_role('Модератор', 'Администратор', 'Боярская дума', 'Глава')
async def clouse_channel(ctx):
    await ctx.channel.delete()

@Bot.command() 
async def AFK(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name= 'AFK')
    await member.add_roles(role)
    await ctx.send(f'{ctx.message.author.mention} ушёл в `AFK`')

@Bot.command() 
async def UN_AFK(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name= 'AFK')
    await member.remove_roles(role)
    await ctx.send(f'{ctx.message.author.mention} пришёл из `AFK`')

@Bot.command() 
@commands.has_any_role('Руководитель', 'Боярская дума', 'Глава')
async def create_role(ctx, name: str= None):

    color = (0xFF1818, 0x71FF18, 0x18FF96, 0x00FFFF)

    if name is None:
        await ctx.send('напишите названия роли')
    else:
        await ctx.guild.create_role(name= name, reason= None, colour= f'{random.choice(color)}', permissions= None, hoist= None, mentionable= None)
        await ctx.send(f'Роль {name} была создана')

@Bot.command() 
async def recall(ctx, member: discord.Member, *, text: str = None):
    if member is None:
        await ctx.channel.purge(limit= 1)
        await ctx.send('Нужно указать себя а не другого')
    elif member is not ctx.message.author:
        await ctx.channel.purge(limit= 1)
        await ctx.send('Укажите себя как автора отзыва')
    elif text is None:
        await ctx.channel.purge(limit= 1)
        await ctx.send("Введите ваше предложение по серверу")
    elif member and text is None:
        await ctx.channel.purge(limit= 1)
        await('Введите пожалуйста себя и свой отзыв')
    else:
        await ctx.channel.purge(limit= 1)
        await ctx.send("Спасибо за ваш отзыв, оно отправлено в <#685525817086050358>")
        channel1 = discord.utils.get(ctx.guild.channels, id = 685525817086050358)
        recal = discord.Embed(color= 0xFF1818, title= "Отзыв", description= f'{text}')
        recal.set_footer(text= f"Отзыв написал {member.nick}", icon_url= "{}".format(member.avatar_url))
        await channel1.send(embed= recal)

@Bot.command() 
async def offer(ctx, member: discord.Member, *, text: str = None):
    if member is None:
        await ctx.channel.purge(limit= 1)
        await ctx.send('Нужно указать себя а не другого')
    elif member is not ctx.message.author:
        await ctx.channel.purge(limit= 1)
        await ctx.send('Укажите себя как автора предложение')
    elif text is None:
        await ctx.channel.purge(limit= 1)
        await ctx.send("Введите ваше предложение по серверу")
    elif member and text is None:
        await ctx.channel.purge(limit= 1)
        await('Введите пожалуйста себя и своё предложение')
    else:
        await ctx.channel.purge(limit= 1)
        await ctx.send("Спасибо за ваше предложение, оно отправлено в <#685525817086050358>")
        channel1 = discord.utils.get(ctx.guild.channels, id = 685525817086050358)
        offer = discord.Embed(color= 0xFF1818, description= f'{text}')
        offer.set_footer(text= f'Предложение от {member.nick}', icon_url= f'{member.avatar_url}')
        await channel1.send(embed= offer)

@Bot.command() 
async def quote(ctx, member: discord.Member, *, text: str = None):
    if member is None:
        await ctx.send(f'Нужно указать себя а не другого {ctx.message.author.mention}')
    elif member is not ctx.message.author:
        await ctx.send(f'Укажите себя как автора предложение {ctx.message.author.mention}')
    elif text is None:
        await ctx.channel.purge(limit= 1)
        await ctx.send('Цитата была выложена в чат <#648896334606368770>')
        channel1 = discord.utils.get(ctx.guild.channels, id = 648896334606368770)
        qoutes = discord.Embed(color= 0x383a3d)
        qoutes.set_footer(text= f"Цитата от {member.nick}", icon_url= "{}".format(member.avatar_url))
        for a in ctx.message.attachments:
            if a.filename.endswith(('.jpg', '.png', '.mp3')):
                qoutes.set_image(url= a.proxy_url)
        await channel1.send(embed= qoutes)
    else:
        await ctx.channel.purge(limit= 1)
        await ctx.send('Цитата была выложена в чат <#648896334606368770>')
        channel1 = discord.utils.get(ctx.guild.channels, id = 648896334606368770)
        qoutes = discord.Embed(color= 0x383a3d, description= f'{text}')
        qoutes.set_footer(text= f"Цитата от {member.nick}", icon_url= "{}".format(member.avatar_url))
        for a in ctx.message.attachments:
            if a.filename.endswith(('.jpg', '.png', '.mp3')):
                qoutes.set_image(url= a.proxy_url)
        await channel1.send(embed= qoutes)

@Bot.command() 
async def help(ctx):
    helf = discord.Embed(title= "Навигатор по боту", color= 0x71FF18)
    helf.add_field(name= "Команды для модерации", value= "/mute - мутит пользователя \n /unmute - размучивает пользователя \n /kick - кикает пользователя со сервера \n /ban - банит пользователя с сервера \n /clear - очищает сервер от сообщений \n /warn - предупреждает пользователя", inline= False)
    helf.add_field(name= "Докладные команды", value= "/complaint - подача жалобы на модератора \n /recall - отзыв серверу \n /offer - предложение по улучшению сервера \n /quote - создание цитатов \n /question - для вопросов по серверу", inline= False)
    helf.add_field(name= "Игровые команды", value= "/reshka - выбераете решку \n /orel - выбераете орёл \n /knb - камень, ножницы, бумага", inline= False)
    helf.add_field(name= "Другие команды", value= "/inf - информация об человеке \n /AFK - команда афк \n /create_private_voice - создания своего войса", inline= False)
    await ctx.send(embed= helf)

@Bot.command() 
@commands.has_role("Игрок")
async def create_private_voice(ctx, member: discord.Member, sites: int = None, *, name = None):

    Category = discord.utils.get(ctx.guild.categories, id = 582134983385153536)
    AFk = discord.utils.get(ctx.guild.voice_channels, id = 582132826711916555)

    overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(use_voice_activation= False),
    ctx.guild.default_role: discord.PermissionOverwrite(manage_channels= False),
    ctx.guild.me: discord.PermissionOverwrite(use_voice_activation= True),
    ctx.guild.me: discord.PermissionOverwrite(manage_channels= True)
}

    if name is None:
        await ctx.send('Пожалуйста напишите название войса')
    elif sites is None:
        private_voice = await ctx.guild.create_voice_channel(name = name, overwrites= overwrites, category = Category, reason = None)
        await ctx.send('Ваш личный войс был создан')
        await asyncio.sleep(18000)
        await ctx.guild.delete(private_voice)
        if member.guild.afk_timeout:
            await asyncio.sleep(600)
            await member.move_to(AFk)
            await ctx.guild.delete(private_voice)
            await member.send('Вы были переведны в AFK а ваш личный войс был удалён')
        elif member.send(f'/create_private_voice {name}') and member.send(f'/create_private_voice {name}'):
            await ctx.channel.purge(limit = 1)
            await ctx.send('Можно создать только один приват войс')
    else:
        private_voice = await ctx.guild.create_voice_channel(name = name, user_limit = sites, overwrites= overwrites, category = Category, reason = None)
        await ctx.send('Ваш личный войс был создан')
        await asyncio.sleep(18000)
        await ctx.guild.delete(private_voice)
        if member.guild.afk_timeout:
            await asyncio.sleep(600)
            await member.move_to(AFk)
            await ctx.guild.delete(private_voice)
            await member.send('Вы были переведны в AFK а ваш личный войс был удалён')
        elif member.send(f'/create_private_voice {name}') and member.send(f'/create_private_voice {name}'):
            await ctx.channel.purge(limit = 1)
            await ctx.send('Можно создать только один приват войс')

@Bot.command() 
@commands.has_any_role('Модератор', 'Боярская дума', 'Администратор', 'Глава')
async def voice_mute(ctx, member: discord.Member, *, reason = None):
    if member is None:
        await ctx.send('Укажите пользователя которого нужно замутить')
    elif reason is None:
        ctx.guild.get_role(718162438293553253)
        await ctx.send(f'{member} был заглушён в войсе по неизвестной причине')
        await member.send(f'Здраствуйте, вас замутил модератор {ctx.message.author.mention} по неизвестной причине, вы можете подать жалобу написав команду `/complaint @user (модератора)`')
    else:
        ctx.guild.get_role(718162438293553253)
        await ctx.send(f'{member} был заглушён в войсе по причине {reason}')
        await member.send(f'Здраствуйте, вас замутил модератор {ctx.message.author.mention} по причине {reason}, если не согласны с причиной мута, вы можете подать жалобу написав команду `/complaint @user (модератора)`')

@Bot.command() 
@commands.has_any_role('Модератор', 'Боярская дума', 'Администратор', 'Глава')
async def voice_unmute(ctx, member: discord.Member, *, reason = None):
    if member is None:
        await ctx.send('Укажите пользователя которого нужно замутить')
    elif reason is None:
        ctx.guild.remove_role(718162438293553253)
        await ctx.send(f'{member} был разглушён в войсе по неизвестной причине')
        await member.send(f'Здраствуйте, вас размутил модератор {ctx.message.author.mention} по неизвестной причине')
    else:
        ctx.guild.remove_role(718162438293553253)
        await ctx.send(f'{member} был разглушён в войсе по причине {reason}')
        await member.send(f'Здраствуйте, вас рамзутил модератор {ctx.message.author.mention} по причине {reason}')

@Bot.command()
@commands.has_any_role('Боярская дума', 'Администратор', 'Глава')
async def warning(ctx, member: discord.Member, *, numberwarn = None):
    if member is None:
        await ctx.send('Упомяните пользователя которого предупредить о бане')
    elif numberwarn is None:
        await ctx.send('пожалуйста введите стадий предупреждений, их всего 3')
    else:
        if numberwarn == '1 предупреждение':
            await ctx.send('Хорошо, отправляю пользователю первое предупреждение')
            await member.send('Здраствуйте! Вы получили первое предурпеждение от сервера ****Jeff\'s Group****, осталось два предупреждения до бана')
        elif numberwarn == '2 предупреждение':
            await ctx.send('Хорошо, отправляю пользователю второе предупреждение')
            await member.send('Здраствуйте! Вы получили второе предурпеждение от сервера ****Jeff\'s Group****, осталось одно предупреждения до бана')
        elif numberwarn == '1 предупреждение':
            await ctx.guild.ban()
            await ctx.send('Третье предупреждение, пользователь был забанен на сервере')
            await member.send('Вы получили третье предупреждение и бан, удачи вам дальше, только уже без нас... \n для разбана подавайте на аппеляцию https://docs.google.com/forms/d/e/1FAIpQLSdcNZ2xe-lwm70w7JYOPfVWi-sn7gm9g4R6HHnbNHxp7hkG0A/viewform?usp=sf_link')
        else:
            await ctx.send('Не несите бред')

@Bot.command()
@commands.has_any_role('Модератор', 'Боярская дума', 'Администратор', 'Глава')
async def mute(ctx, member: discord.Member, time: int = None, *, reason = None):
    role = discord.utils.get(ctx.guild.roles, id = 657650336718389258)
    if member == None:
        await ctx.send('Упомяните пользователя которого нужно замутить')
    elif time is None:
        muted = (discord.Embed(title = "Произошёл мут!", color = 0x383a3d, description = f'{member} был замучен по причине {reason}, время мута None'))
        muted.set_footer(text= f'Замутил пользователя {ctx.message.author.mention}')
        await ctx.send(embed= muted)
        await member.send(f'Здраствуйте! Вас замутили по причине {reason}, время мута None')
        await member.add_roles(role)
    elif reason is None:
        muted1 = (discord.Embed(title = "Произошёл мут!", color = 0x383a3d, description = f'{member} был замучен по причине None, время мута {time} секунд'))
        muted1.set_footer(text= f'Замутил пользователя {ctx.message.author.mention}')
        await ctx.send(embed= muted1)
        await member.send(f'Здраствуйте! Вас замутили по причине None, время мута {time} секунд')
        await member.add_roles(role)
        await asyncio.sleep(time)
        await member.remove_roles(role)
        emb = discord.Embed(title= 'Размут!', color = 0x383a3d, description= f'{member} был размучен из за исхода времени')
        await ctx.send(embed= emb)
        await member.send('Здраствйте снова! Вы были размучены, время мута вышло')
    else:
        muted1 = (discord.Embed(title = "Произошёл мут!", color = 0x383a3d, description = f'{member} был замучен по причине {reason}, время мута {time} секунд'))
        muted1.set_footer(text= f'Замутил пользователя {ctx.message.author.mention}')
        await ctx.send(embed= muted1)
        await member.send(f'Здраствуйте! Вас замутили по причине {reason}, время мута {time} секунд')
        await member.add_roles(role)
        await asyncio.sleep(time)
        await member.remove_roles(role)
        emb = discord.Embed(title= 'Размут', color = 0x383a3d, description= f'{member} был размучен из за исхода времени')
        await ctx.send(embed= emb)
        await member.send('Здраствйте снова! Вы были размучены, время мута вышло')

@Bot.command
@commands.has_any_role('Боярская дума', 'Администратор', 'Глава', 'Главный по розыгрышам')
async def giveaway(ctx, member: discord.Member, name: str = None, users: int = None, timer: int = None):
    if member == None:
        await ctx.send('Укажите себя как автора этого розыгрыша')
    elif users is None:
        await ctx.send('Укажите кол-во пользователей которые должны попасть в победители')
    elif name is None:
        await ctx.send('Напишите название рулетки')
    else:
        giveawayy = discord.Embed(title= f'Розыгрыш: {name}', color = 0x383a3d, description = f'Число пользователей: {users} \n Время розыгрыша: {timer}')
        await ctx.send(embed = giveawayy)
        await ctx.message.add_reaction('🎉')
        await asyncio.sleep(timer)
        await ctx.guild.edit(giveawayy, description = f'Победители хз кто!')

@Bot.event
async def on_message_delete(message):
    channelDelete = discord.utils.get(message.guild.channels, id = 602144054591094794)
    DeleteMessage = discord.Embed(title= 'Сообщение было удалено', color = 0x383a3d)
    DeleteMessage.add_field(name= 'Удалённое сообщение:', value = f'{message.content}')
    DeleteMessage.add_field(name= 'Автор удалённого сообщения:', value = f'{message.author}')
    DeleteMessage.add_field(name= 'В категории и в чате:', value = f'{message.channel}')
    DeleteMessage.set_footer(text= 'ID сообщения: {}, id пользователя: {}'.format(message.id, message.author.mention))
    for a in message.attachments:
        if a.filename.endswith(('.jpg', '.jpeg', '.png')):
            DeleteMessage.set_image(url = a.proxy_url)
    await channelDelete.send(embed = DeleteMessage)

@Bot.command()
async def knb(ctx, move: str = None):
    solutions = ["`ножницы`", "`камень`", "`бумага`"]
    winner = "**НИЧЬЯ**"
    p1 = solutions.index(f"`{move.lower()}`")
    p2 = randint(0, 2)
    if p1 == 0 and p2 == 1 or p1 == 1 and p2 == 2 or p1 == 2 and p2 == 0:
        winner = f"{ctx.message.author.mention} ты **Проиграл**"
    elif p1 == 1 and p2 == 0 or p1 == 2 and p2 == 1 or p1 == 0 and p2 == 2:
        winner = f"{ctx.message.author.mention} ты **Выиграл**"
    await ctx.send(    
        f"{ctx.message.author.mention} **=>** {solutions[p1]}\n"
        f"{Bot.user.mention} **=>** {solutions[p2]}\n"
        f"{winner}")

@Bot.command()
async def support(ctx):
    setting = discord.Embed(color= 0x383a3d)
    setting.set_author(name= 'Служба поддержки и запросы')
    setting.add_field(name= 'ᅠ', value= 'Здраствуйте! Вы находитесь на стадий подачи верефикаций/заявки/запросов', inline= False)
    setting.add_field(name= 'ᅠ', value= 'Мы должны знать какой категорий относится ваш запрос: \n `верефикация`, `жалоба на модератора` или `другое`', inline= False)
    setting.add_field(name= 'ᅠ', value= '****Описание:****', inline= False)
    setting.add_field(name = 'ᅠ', value= '****/ верификация:**** Вы подайте заявку для удаления с себя роли рертенанта и получить после верефикаций роль игрок \n ****/ жалоба на модератора:**** вы можете подать жалобу, если человек плохо работает и т.п. \n ****/ другое:**** все, что не подходит под вышеуказанные категории.')
    setting.add_field(name= 'ᅠ', value= '****В какую категорию вы собираетесь подать?****', inline= False)
    await ctx.send(embed= setting)

@Bot.command(aliases= ['верификация'])
async def ᅠ(ctx):

    await ctx.send('Хорошо, чтоб пройти верефикацию нужно написать заявку, напишите команду `/BidVerify @user текст [в тексте отвечаете на вопросы: Зачем модерация на сервере? Для чего нужна верефикация? Почему важны правила на сервере?]` Хочу предупредить, после написаний текста он будет пошлен сразу администраций и проверить или отредактировать уже нельзя')

@Bot.command()
async def BidVerify(ctx, member: discord.Member, *, description = None):
    verify_channel = discord.utils.get(ctx.guild.channels, id = 637294602919084042)

    if Bot.get_command('верификация') == False:
        pass
    else:
        await ctx.send(embed = discord.Embed(color = 0x383a3d, description = f'Ваш текст был отправлен: \n \n Подача заявки на верефикацию от {member} \n \n Текст: {description}'))
        await verify_channel.send(embed = discord.Embed(color = 0x383a3d, description = f'Подача заявки на верефикацию от {member} \n \n {description}'))
        await ctx.send('Заявка была отправлена, ждите в течений 10-15 минут вам придёт письмо')

@Bot.command()
@commands.has_any_role('Модератор', 'Боярская дума', 'Администратор', 'Глава')
async def ver(ctx, member: discord.Member, *, decision = None, session = None):

    verify = discord.utils.get(ctx.guild.roles, id = 603831732327809045)
    not_verify = discord.utils.get(ctx.guild.roles, id = 722432542107500586)
    bid_verifr = Bot.get_command('bid_verify')

    if member is None:
            await ctx.send('Упомяните пользователя или же возьмите айди')
    elif decision is None:
            await ctx.send('Укажите этапы, их всего три: `accepted` - заявка хорошая и вы её принимаете и человек верефицирован, `prohibition` - заявка плохая и она не принята, `draw` - заявка не совсем хорошая и не совсем плохая, предлагаете снова переписать анкету')
    else:
        if decision == 'accepted':
                await member.remove_roles(not_verify)
                await member.add_roles(verify)
                await ctx.send('Человек прошёл верефикацию')
                await member.send('Вы были верефицированы')
        elif decision == 'prohibition':
                await ctx.send('Заявка была отклонена')
                await member.send('Ваша заявка на верефикацию была отклонена')
        elif decision == 'draw' and session == None:
                await ctx.send('Напишите о заявке что нужно добавить а что убрать')
        else:
            await ctx.send('Ваш ответ о вашей заявке отправлен')
            await member.send(embed= discord.Embed(title = 'о вашей заявке', color = 0x383a3d, description = f'Ответ от администратора: {session} \n \n Прошу вас взять ваш текст и отредактировать его: \n \n  ****{bid_verifr.title}**** \n {bid_verifr.description}'))

@Bot.command(aliases = ['жалоба на модератора'])
async def ᅠᅠ(ctx):

    await ctx.send('Хорошо, чтобы написать жалобы напишите `/mod_complaint @user [упомяните модератора] text [сама жалоба на модератора]`. Хочу предупредить, после написаний текста он будет пошлен сразу администраций и проверить или отредактировать уже нельзя')

@Bot.command()
async def mod_complaint(ctx, member: discord.Member, *, text = None):


    md_chat = discord.utils.get(ctx.guild.channels, id = 637294602919084042)

    if Bot.get_command('модерация') == False:
        pass
    elif member is None:
        await ctx.send('Упомяните модератора на которого нужно подать вам жалобу')
    elif text is None:
        await ctx.send('Напишите саму жалобу')
    else:
        emb= discord.Embed(title = f'Жалоба на мд {member}', color = 0x383a3d, description = f'{text}')
        emb.set_footer(text= f'Жалоба от {ctx.message.author} | id пользователя = {ctx.message.author.mention}')
        await md_chat.send(embed= emb)
        await ctx.send('Ваша жалоба была подана')

@Bot.command()
@commands.has_any_role('Модератор', 'Боярская дума', 'Администратор', 'Глава')
async def answer_mod_complaint(ctx, member: discord.Member, *, session = None):
    if member is None:
        await ctx.send('Укажите пользователя который подал жалобу')
    else:
        if session is None:
            await ctx.send('Выберите этапы, их си во лишь 3, `accepted` - жалоба принята, `False` - жалоба не принята, `None_Mod` - такого модератора нет')
        elif session == 'accepted':
            await ctx.send('Жалоба принята')
            await member.send('Ваша жалоба была принята, спасибо что рассказали нам что он делал')
        elif session == 'False':
            await ctx.send('Жалоба отменена')
            await member.send('Ваша жалоба была отклонена')
        elif session == 'None_Mod':
            await ctx.send('Хорошо предупрежу, что нет такого модератора')
            await member.send('Жалоба была отменена, нету такого модератора которого вы упомянули')

@Bot.command(aliases = ['другое'])
async def ᅠᅠᅠ(ctx):
    await ctx.send('Хорошо, напишите команду `/other @user [упомяните себя] text [свою просьбу]`. Хочу предупредить, после написаний текста он будет пошлен сразу администраций и проверить или отредактировать уже нельзя')

@Bot.command()
async def other(ctx, member: discord.Member, *, text = None):

    ot_chat = discord.utils.get(ctx.guild.channels, id = 637294602919084042)

    if member is None:
        await ctx.send('Упомяните себя')
    elif text is None:
        await ctx.send('Напишите свою просьбу')
    else:
        emb = discord.Embed(color = 0x383a3d, description = f'{text}')
        emb.set_footer(text = f'Просьба от {member}', icon_url= f'{member.avatar_url}')
        await ot_chat.send(embed = emb)
        await ctx.send('Ваша просьба отправлена')

@Bot.command()
@commands.has_any_role('Модератор', 'Боярская дума', 'Администратор', 'Глава')
async def answer_other(ctx, member: discord.Member, *, answer = None):
    if member is None:
        await ctx.send('Упомяните пользователя')
    elif answer is None:
        await ctx.send('Напишите ответ')
    else:
        await ctx.send('Ответ отправлен')
        await member.send(color= 0x383a3d, title = f'{member} пришёл ответ на вашу просьбу', description = f'{answer}')

@Bot.event
async def on_member_join(member):
    rertenant = discord.utils.get(member.guild.roles, id = 722432542107500586)

    await member.add_roles(rertenant)
    await member.send('Добро пожаловать на сервер ****Jeff\'s Group****')

@Bot.command()
async def s_wikipedia(ctx, *, wkipedia = None):
    if wkipedia == None:
        await ctx.send('Напишите о чём вы хотите узнать')
    else:
        wikipedia.set_lang('ru')
        pang = wikipedia.page(wkipedia)
        summm = wikipedia.summary(wkipedia)
        emb = discord.Embed(
            title = pang.title,
            description = summm,
            color = 0x383a3d
        )
        await ctx.send(embed= emb)

token = os.environ.get('BOT_TOKEN')
