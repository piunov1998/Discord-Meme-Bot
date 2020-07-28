import discord, json, os
from discord.ext import commands

with open('Data.json', encoding = 'utf-8') as dataFile:
    data = json.load(dataFile)
    token = data['token']
    prefix = tuple(data['prefix'])[0]
    client = commands.Bot(command_prefix = tuple(data['prefix']))
meme_list = {}
meme_folder = './img/'
with open('quotes.json', encoding='utf-8') as q:
    quotes = json.load(q)
print(f'Quotes library loaded. ({len(quotes)} qoutes)')

def create():
    meme_list.clear()
    for filename in os.listdir(meme_folder):
        name = os.path.splitext(filename)[0]
        meme_list[name] = meme_folder + filename

@client.event
async def on_ready():
    print('Ready.')

@client.command(brief = 'Shows meme list')
async def memes(ctx):
    create()
    string = ''
    i = 0
    for name in meme_list.keys():
        i += 1
        string += f'{i}. {name}\n'
    await ctx.message.channel.send(f'```{string}```')

@client.command(brief = 'Saves ur meme')
async def save(ctx, *name):
    meme_name = ''
    for word in name:
        meme_name += f'{word} '
    meme_name = meme_name[:-1]
    original_name = ctx.message.attachments[0].filename
    original_path = os.path.join(meme_folder, original_name)
    await ctx.message.attachments[0].save(original_path)
    
    meme_ext = os.path.splitext(original_name)[1]
    os.rename(original_path, os.path.join(meme_folder, meme_name + meme_ext))
    create()
    await ctx.message.channel.send(f'```Meme saved as {meme_name}```')

@client.command(brief = 'Saves ur quote')
async def savequote(ctx, quote_name, author, *quote_words):
    text = ''
    for word in quote_words:
        text += f'{word} '
    text = text[:-1]
    quote = {
        'author' : author,
        'text' : text
    }
    quotes[quote_name] = quote
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes, f, sort_keys=True, indent=2)
    string = f'```Quote has been saved:\nName: {quote_name}\nAuthor: {author}```'
    await ctx.message.channel.send(string)

@client.command(brief = 'Shows chosen meme')
async def meme(ctx, *meme):
    meme_name = ''
    for word in meme:
        meme_name += f'{word} '
    meme_name = meme_name[:-1]
    picture_path = meme_list[meme_name]
    with open(picture_path, 'rb') as picture:
        file = discord.File(picture)
        await ctx.message.channel.send(file = file)

@client.command(brief = 'Shows chosen quote')
async def quote(ctx, *id):
    quote_id = ''
    for word in id:
        quote_id += f'{word} '
    quote_id = quote_id[:-1]
    quote = quotes[quote_id]
    text = quote['text']
    author = quote['author']
    string = f'{text}\n©{author}'
    await ctx.message.channel.send(f'**{string}**')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'**{ctx.message.content}** command not found. Use {prefix}help')

create()
print(f'Memes library loaded. ({len(meme_list)} memes)')
client.run(token)