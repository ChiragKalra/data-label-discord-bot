import csv
import os

import discord

root = 'C:/Users/bruhascended/PycharmProjects/SMS/pruned_db/'

token = open('token', 'r').read()
data = list(csv.reader(open(root + 'human.csv', encoding='utf8')))
same = list(csv.reader(open(root + 'same.csv', encoding='utf8')))

distinct = []

for twins in same:
    distinct.append(int(twins[0]))

bot_state = False


async def display_message(message):
    global bot_state
    index = int(open('pos', 'r').read())
    if index < len(distinct):
        to_send = 'sms number #{1}\nSender: {0[1]};\n{0[2]}'.format(data[distinct[index] + 1], index)
    else:
        bot_state = False
        to_send = 'All of data set is labelled!\n'\
                  '------------END------------'
    await message.channel.send(to_send)


class MyClient(discord.Client):
    async def on_ready(self):
        print('Login Successful as '+self.user.name+' - '+str(self.user.id))

    @staticmethod
    async def on_member_join(member):
        pass

    async def on_message(self, message):
        _content = message.clean_content.lower()
        global bot_state

        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        # text
        elif _content.find('sms start') > -1:
            bot_state = True
            await message.channel.send('1 for personal\n2 for transaction\n3 for advertisement\n'
                                       '4 for spam/fraud\n5 for not clear\n'
                                       '------------------START----------------')
            await display_message(message)

        elif _content.isdigit() and int(_content) in range(1, 6) and bot_state:
            index = int(open('pos', 'r').read())
            open('pos', 'w').write(str(index + 1))
            open("labels.csv", "a").write('\n{0},{1}'.format(distinct[index], message.clean_content))
            await display_message(message)

        elif _content == 'undo' and bot_state:
            await message.channel.send("Undoing last label")

            # remove last label from file
            index = int(open('pos', 'r').read())
            open('pos', 'w').write(str(index - 1))

            with open('labels.csv', "r+") as file:
                file.seek(0, os.SEEK_END)
                pos = file.tell()
                while pos >= 0 and file.read(1) != '\n':
                    pos -= 1
                    file.seek(pos, os.SEEK_SET)
                if pos >= 0:
                    file.seek(pos-1, os.SEEK_SET)
                    file.truncate()

            await display_message(message)

        elif _content.find('sms end') > -1:
            bot_state = False
            await message.channel.send("sms bot has ended\n"
                                       '-------------------END-----------------\n')

        elif _content.find('sms') > -1:
            await message.channel.send("\"SMS start\" to start labeling")


client = MyClient()
client.run(token)
