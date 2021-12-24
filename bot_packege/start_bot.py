import json
import math
import os
import sqlite3
import discord
from discord.ext import commands
import string
import random
from math import *
import webbrowser as wb

import to_json
import my_qr

bool_start = True
staus = ''

# Реализация меню консоли для управления ботом
while bool_start:
    print('Настройки бота Proj_Bot')
    print('1)Включить бота')
    print('2)Обновить список запрещенных слов')
    print('3)Установить статус Proj_Bot')
    print('4)Завершить работу')
    choice = int(input('Ваш выбор:'))
    if choice == 1:
        break
    elif choice == 2:
        to_json.create_json()
    elif choice == 3:
        print()
        staus = input('Статус:')
        print()
        print('Статус...........ОК')
        print()
    elif choice == 4:
        exit()
    else:
        print()
        print('Простите, такого пункта нет в меню!')
        print()
# Добавил префикс на команды и разрешения для раьоты на сервере
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command('help')
#Создал декоратор для проверки события старта бота
@bot.event
# Далее создаю асинхронную функцию (по документациии сказано, что нужно все делать через них)
async def on_ready():

    my_base = sqlite3.connect('bot.db')
    await bot.change_presence( status= discord.Status.online, activity= discord.Game(staus))
    print()
    print('Включение бота прошло успешно!')

    if my_base:
        print('Подключение к базе данных...........ОК')
        my_base.close()

@bot.event
# асинхронный метод фиксирующий в общий чат присоединение новых пользователей сервера
async def on_member_join(member):
    await member.send('Приветствую! Я бот Proj_Bot, и просмотр команд начинается с команды !инфо \n Хочу предупредить,что на этом сервере не допустимо использование ненормативной лексики!' )
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member}, здорово, что вы уже с нами! (в лс оправил сообщение по этому серверу)')
@bot.event
# асинхронный метод обработка ошибок, конкретнее: запросы от пользователей на не существующие команды
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.author.mention}, такой команды нет!!!')
@bot.event
# асинхронный метод фиксирующий в общий чат уход пользователей с сервера
async def on_member_remove(member):
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member}, нам будет тебя не хватать!')

@bot.command()
# асинхронный метод реализующий первую тестовую команду в этом проекте
async def test(ctx):
    await ctx.send('Тест команды прошел успешно!')
@bot.command()
# асинхронный метод реализующий команду !инфо , отображающую информацию по всем командам
async def инфо(ctx):
        emb = discord.Embed(title='Помощь', colour=discord.Colour.green(),)
        emb.set_image(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSdEETL50Glbryer5Ut_e0wbP-XPex_AIThQ&usqp=CAU')
        emb.add_field(name='!test', value='тестовая команда')
        emb.add_field(name='!qr<ссылка>', value='позволяет получить qr код из ссылки')
        emb.add_field(name='!статус', value='узнать кол-во нарушений')
        emb.add_field(name='!волк', value='вызвать рандомную цитату волка')
        emb.add_field(name='!yandex<запрос>', value='воспользоваться поисковиком')
        emb.add_field(name='!очистка <кол-во сообщений>', value='удаление сообщений из чата (только для админов)')
        emb.add_field(name='!выгнать <ник>', value='исключает пользователя сервера (только для админов)')
        emb.add_field(name='!забанить <ник> ', value='банит пользователя на сервере (только для админов)')
        emb.add_field(name='!разбанить <ник>', value='снмает бан с пользователя (только для админов)')
        emb.add_field(name='!стоп ', value='отключает бота')
        emb.add_field(name='!заглушить <ник>', value='Отключает возможность писать в чате(только для админов)')
        emb.add_field(name='!разглушить <ник>', value='Убирает отключение чата(только для админов)')
        emb.set_footer(text='Было зарошено:  {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed = emb)
@bot.command()
# асинхронный метод реализующий команду !калькулятор, позволяющий пользователям проводить простые математические команды
# силами сервера бота
async def калькулятор(ctx, a:int, arg, b:int = 1):
    if arg == '+':
        await ctx.send(f'Результат: {a+b}')
    elif arg == '-':
        await ctx.send(f'Результат: {a-b}')
    elif arg == '*':
        await ctx.send(f'Результат: {a*b}')
    elif (arg == '/') and (b != 0):
        await ctx.send(f'Результат: {a/b}')
    elif (arg == '^'):
        await ctx.send(f'Результат: {a ** b}')
    elif (arg == '^') and (b != 0):
        await ctx.send(f'Результат: {a ** b}')
    elif (arg == '!') and (b != 0):
        await ctx.send(f'Результат: {math.factorial(a)}')


@bot.command()
@commands.has_permissions(administrator = True)
# асинхронный метод реализующий команду !yandex, открытие браузера происходит на машине с запущеным ботом
# предусмотрена только для оператора сервера (человек, имеющий полный доступ к файлам бота и его консоли)
async def yandex(ctx ,*, arg_1 = None):
    if arg_1 != None:
        request = arg_1
        await wb.open('https://yandex.ru/search/?text=' + request)
    else:
        wb.open('https://yandex.ru/')
@bot.command()
# асинхронный метод реализующий команду !qr, вызов воспомагательного метода (в отдельном файле my_qr)
async def qr(ctx, *, arg):
    my_qr.make_qr(arg)
    await ctx.send('Ваш qr-код', file=discord.File('my_qr.png'))

@bot.command()
async def статус(ctx):
    # асинхронный метод реализующий команду проверки на кол-во нарушений по базе данных
    # метод устанавливает соединение с бд, далее проверяет создана ли таблица нарушителей, если не создана создает
    # отправляет изменения в бд, плсле чего отправляет поисковый запрос, по запрасившему эту команду
    # если не находит записи, то рапартует , что нарушений нет, иначе сообщаяет о кол-ве нарушений
    # после закрывает соединение с бд
    my_base = sqlite3.connect('bot.db')
    my_cur = my_base.cursor()
    my_base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(ctx.message.guild.name))
    my_base.commit()
    warning = my_cur.execute('SELECT * FROM {} WHERE userid == ?'.format(ctx.message.guild.name)
                          , (ctx.message.author.id,)).fetchone()
    my_base.close()
    if warning == None:
        await ctx.send(f'{ctx.message.author.mention}, у вас нет предупреждений!!!')
    else:
        await ctx.send(f'{ctx.message.author.mention}, у вас {warning[1]} предупреждений!!!')
@bot.command()
@commands.has_permissions(administrator = True)
# асинхронный метод реализующий команду удаления сообщений из чата
# декоратор @commands.has_permissions(administrator = True) - дает право использовать эту команду только администраторами
async def очистка(ctx, amount=10):
    await ctx.channel.purge(limit=amount)
@bot.command()
@commands.has_permissions(administrator = True)
# асинхронный метод реализующий команду исключения с сервера пользователя (Важно, что он может вернуться сам, по моим мыслям может служить предупредительной мерой)
#с помощью Embed из дискорд api, получилось организовать вывод красивой таблички
async def выгнать(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='Наказание', colour=discord.Colour.red())
    await ctx.channel.purge(limit=1)
    await member.kick(reason = reason)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Отключение от сервера', value='Отключен пользователь: {}'.format(member.mention))
    emb.set_footer(text='Был отключен администратором:  {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)
@bot.command()
@commands.has_permissions(administrator = True)
# асинхронный метод реализующий команду аварийной остановки бота
# бд отключаю на всякий случай, если в новых обновлениях буду забывать на месте закрывать после использования
async def стоп(ctx):
    my_base = sqlite3.connect('bot.db')
    await ctx.send('Proj_Bot отключен!!!')
    my_base.close()
    await exit()

@bot.command()
@commands.has_permissions(administrator = True)
# асинхронный метод реализующий бан пользователей
# Embed опять выручил с красивой табличкой, с информацией по бану
async def забанить(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='Наказание', colour=discord.Colour.red())
    await member.ban(reason = reason)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Бан пользователя',value='Забанен пользователь: {}'.format(member.mention))
    emb.set_footer( text = 'Был забанен администратором:  {}'.format(ctx.author.name),icon_url=ctx.author.avatar_url)
    await ctx.send(embed = emb)
@bot.command()
@commands.has_permissions(administrator = True)
# асинхронный метод реализующий снятие бана с пользователей
async def разбанить(ctx, * , member):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Амнистия', colour=discord.Colour.green())
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        await  ctx.guild.unban(user)
        emb.add_field(name='Снятие бана', value='Амнистирован пользователь: {}'.format(member.mention))
        emb.set_footer(text='Амнистия объявлена администратором:  {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
        return
@bot.command()
@commands.has_permissions(administrator = True)
# асинхронный метод реализующий запрет пользователю на отправку сообщений
# перед примененим на сервере следует создать роль 'mute' и в настройках настроить все ограничения
# вызов этой команды назначает пользователю эту роль с онраничениями
async def заглушить(ctx,member: discord.Member):
    emb = discord.Embed(title='Наказание', colour=discord.Colour.red())
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')
    await member.add_roles(mute_role)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Ограничение сообщений', value='Пользователь заглушен: {}'.format(member.mention))
    emb.set_footer(text='Ограничение было выдано администратором:  {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)
@bot.command()
@commands.has_permissions(administrator = True)
# асинхронный метод реализующий снятие ограничения по сообщениям из метода выше
# у пользователя исключается роль 'mute'
# после чего выводится табличка с амнистией
async def разглушить(ctx,member: discord.Member):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Амнистия', colour=discord.Colour.green())
    mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')
    await member.remove_roles(mute_role)
    emb.add_field(name='Снятие ограничений чата', value='Амнистирован пользователь: {}'.format(member.mention))
    emb.set_footer(text='Амнистия объявлена администратором:  {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)
    await ctx.send(f'У {member.mention}, ограничение чатов отключено!')
@bot.command()
# асинхронный метод, создающий список с ссылками на картинки 'Цитаты великого волка'
# далее с помощью рандома выберается случайная ссылка на картину и картинка по этой ссылки выводится в чат
async def волк(ctx):
    imgs = [
        "https://eus-www.sway-cdn.com/s/J4E1975xk51EEm7q/images/-vn04jEW8velPq?quality=2048&allowAnimation=true",
        "https://citatko.com/wp-content/uploads/2020/12/8-1.jpg",
        "https://avatars.mds.yandex.net/get-zen_doc/3614701/pub_5f16a392743dd36e9bb41ff5_5f16a49c6286b935475d5b93/scale_1200",
        "https://pbs.twimg.com/media/EB3PGvFWkAAnLiX.jpg",
        "https://pbs.twimg.com/media/FCIRNUSWEAE3Zpk.jpg:large",
        "https://www.meme-arsenal.com/memes/7e256296d5657c5973762ddcb112d3b9.jpg",
        "https://i.ytimg.com/vi/9Pbtql83sSM/maxresdefault.jpg",
        "https://dm-st.ru/wp-content/uploads/2019/07/post_5d33994d24a32.jpeg",
        ''
    ]
    embed = discord.Embed(color = 0xff9900, title = 'Цитата великого волка') # Создание Embed'a
    embed.set_image(url=random.choice(imgs)) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed
@bot.event
# асинхронный метод, прослушивающий сообщения всех пользователей, и сверяющий их с списком запрещеных слов из json (с запрещеными словами)
# string.punctuation использовал для проверки, на вставляния знаков препинания в слова, чтоб пресеч обход мат фильтра
# далее работаю с бд, создаю бд если не создана, после прогоняю по таблице пользователя,
# по столбцу count (кол-во нарушений),ориентируюсь по дабавлению записи в бд или обновлению ее ячейки на + 1 единицу
# максимальное кол-во нарушений на 24.12.2021 составляет 3 нарушения, после чего происходит бан пользователя
async def on_message(message):
    my_base = sqlite3.connect('bot.db')
    my_cur = my_base.cursor()
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
        message.content.split(' ')}.intersection(set(json.load(open('black_list.json')))) != set():
        await message.channel.send(f'{message.author.mention}, тут так нельзя говорить!!!')
        await message.delete()

        name = message.guild.name

        my_base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(name))
        my_base.commit()

        warning = my_cur.execute('SELECT * FROM {} WHERE userid == ?'.format(name), (message.author.id,)).fetchone()
        my_base.close()

        if warning == None:
            my_base = sqlite3.connect('bot.db')
            my_cur = my_base.cursor()
            my_cur.execute('INSERT INTO  {}  VALUES(?, ?)'.format(name), (message.author.id, 1)).fetchone()
            my_base.commit()
            await message.channel.send(f'{message.author.mention}, у вас первое предупреждение! (После 3 предупреждения будет приняты меры!)')
        elif warning[1] == 1:
            my_base = sqlite3.connect('bot.db')
            my_cur = my_base.cursor()
            my_cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name), (2, message.author.id))
            my_base.commit()
            my_base.close()
            await message.channel.send(f'{message.author.mention}, в полку ваших предупреждений прибыло! (После 3 предупреждения будет приняты меры!)')

        elif warning[1] == 2:
            my_base = sqlite3.connect('bot.db')
            my_cur = my_base.cursor()
            my_cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name), (3, message.author.id))
            my_base.commit()
            my_base.close()
            await message.channel.send(f'{message.author.mention}, Забанен за использование недопустимых слов!')
            await message.author.ban(reason='Недопустимые выражения')
    await bot.process_commands(message)

@очистка.error
# асинхронный метод, осуществляющий обработку ошибок по командам
# ошибка commands.MissingPermissions - появляется при недоси=таточном кол-ве прав у пользователя, который вызывает эту команду
# ошибка commands.MissingRequiredArgument - появляется, когда в методе вызова команды не нашелся аргумент
async def очистка_error(ctx,error):
    if isinstance( error , commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, у вас недостаточно прав для использования этой команды !!!')


@выгнать.error
async def выгнать_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, у вас недостаточно прав для использования этой команды !!!')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, Пользователь для отключения не выбран !!!')
@стоп.error
async def стоп_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, у вас недостаточно прав для использования этой команды !!!')

@забанить.error
async def забанить_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, у вас недостаточно прав для использования этой команды !!!')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, Пользователь для бана не выбран !!!')
@разбанить.error
async def разбанить_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name},у вас недостаточно прав для использования этой команды !!! ')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, Пользователь для амнистии не выбран !!!')
@qr.error
async def qr_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, Вы не ввели сслыку или сообщение !!!')


bot.run(os.getenv('TOKEN'))