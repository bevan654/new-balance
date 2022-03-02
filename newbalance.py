import requests
import threading
from termcolor import *
import colorama
from datetime import datetime
from utility import *
import random
from discord_webhook import DiscordWebhook, DiscordEmbed


proxies = Data().loadProxies('proxies.txt')
colorama.init()




print('starting')
class Task:
    def __init__(self,pid):
        self.pid = pid
        self.stock = {}
        self.first_run = True
        self.LOG('Starting','blue',bypass=True)
        self.sendWebhook('deployed','deployed','https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=936&height=936','deployed')
        self.monitor()


    def sendWebhook(self,price,title,image,stock):
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/947719726778449950/yKP9G6xnq8DrjYrlttp3Txicug2zj92OYLkg_diNU55hGoPlUqHMi3I4I1i56HLEpFay')

        embed = DiscordEmbed(title=title, color=15158332,url=f'https://www.newbalance.com.au/pd/slot/{self.pid}.html?sku={self.pid}&endpoint=slot')

        embed.set_author(name='https://www.newbalance.com.au')


        embed.set_thumbnail(url=image)

        # set footer
        embed.set_footer(text='Powered By Genesis | New Balance V0.9.0', icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=936&height=936')

        embed.set_timestamp()

        # add fields to embed
        embed.add_embed_field(name='Notification Type', value=self.notification,inline=True)
        embed.add_embed_field(name='Price', value=price,inline=True)
        embed.add_embed_field(name='Stock',value=stock,inline=False)
        embed.add_embed_field(name='Links',value=f'**[Product Link](https://www.newbalance.com.au/pd/slot/{self.pid}.html?sku={self.pid}&endpoint=slot) | [Cart](https://www.newbalance.com.au/on/demandware.store/Sites-NBAU-Site/en_AU/Cart-Show) | [Login](https://www.newbalance.com.au/on/demandware.store/Sites-NBAU-Site/en_AU/Login-Show)**')

        # add embed object to webhook
        webhook.add_embed(embed)

        response = webhook.execute()


    def LOG(self,text,color,bypass=False):
        if(bypass):
            print(colored(f'[{datetime.now()}][{self.pid}] {text}',color))
            return
        if not self.first_run:
            print(colored(f'[{datetime.now()}][{self.pid}] {text}',color))

    def monitor(self):
        cycle = 0
        while True:
            cycle += 1

            if(cycle == 1 or cycle == 2 or cycle % 500 == 0):
                self.LOG("Checking",'blue',bypass=True)

            self.notification = None
            try:
                response = requests.get(f'https://www.newbalance.com.au/on/demandware.store/Sites-NBAU-Site/en_AU/Product-Variation?pid={self.pid}',proxies=random.choice(proxies))
            except Exception as e:
                print(e)
                self.LOG("Request Error",'red')
                continue

            if response.status_code == 200:
                newly_available = []
                response = response.json()
                for i in response['product']['variationAttributes'][1]['values']:

                    if(i['displayValue'] not in self.stock):

                        self.notification = 'New Sizes Added'

                        if i['selectable'] == True:
                            newly_available.append(i['displayValue'])
                        self.LOG('[NEW SIZE] '+i['displayValue'] + ' :: '+str(i['selectable']),'yellow')
                        self.stock[i['displayValue']] = i['selectable']
                    elif(self.stock[i['displayValue']] != i['selectable']):

                        self.notification = 'Sizes Restocked'

                        self.LOG('[VARIANT UPDATE] '+i['displayValue'] + ' :: '+ str(self.stock[i['displayValue']]) + ' -> ' + str(i['selectable']),'yellow')
                        self.stock[i['displayValue']] = i['selectable']
                        if(i['selectable'] == True):
                            newly_available.append(i['displayValue'])

                if len(newly_available) != 0 and not self.first_run:
                    desc = ''
                    price = response['product']['price']['sales']['formatted']
                    title = response['product']['images']['productDetail'][0]['alt']
                    image = response['product']['images']['productDetail'][0]['src']

                    for i in newly_available:
                        desc = desc + i + '\n'

                    self.sendWebhook(price,title,image,desc)




                self.first_run = False


            elif response.statsu_code == 403:
                self.LOG("Unauthorized Access",'red')
                continue
            else:
                self.LOG("Bad Response Status "+str(response.status_code),'red')
                continue
            
            



with open('pids.txt','r') as e:
    e = e.readlines()
    for i in e:
        i = i.replace('\n','')
        threading.Thread(target=Task,args=(i,)).start()
