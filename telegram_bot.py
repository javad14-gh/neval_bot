from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ContextTypes,ApplicationBuilder,CommandHandler,ConversationHandler,filters,MessageHandler
from bs4 import BeautifulSoup
import requests
import json




headers = {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00 Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1'}
token = '5921068963:AAH1KQkVg0YyajEq4c5dBRSPhfXfM3cpZpo'
menu = [['/matn','/getPic'],['/nerkh','/gheymat_lir'],['/send_message_channel']]
markup_menu = ReplyKeyboardMarkup(menu,one_time_keyboard=True)
markup_edame = ReplyKeyboardMarkup([['/YES','/NO']],one_time_keyboard=True)
menuKey , getpickey , matnKey , resume , calculate , lir = range(6)

def getImage(siteUrl):
    response = requests.get(siteUrl, headers=headers,)
    parser = BeautifulSoup(response.text, 'html.parser')
    return parser

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="%s joon amdei beterekunim??????" % update.message.from_user['first_name'],reply_markup=markup_menu)
    return menuKey

async def eslah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text = 'lotfan matn ra vared konid')
    return matnKey

async def get_pic(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text='lotfan link mahsul ra vared namaeed')
    return getpickey

async def eslahe_matn(update:Update,context:ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    matn = matn.replace('ي','ی')
    matn = matn.replace('ك','ک')
    matn = matn.replace('¥', u'\u200c')
    await context.bot.send_message(chat_id=update.effective_chat.id,text = matn)
    return menuKey
   
async def get_image_zara(update: Update,context: ContextTypes.DEFAULT_TYPE):
    try:    
        link = update.message.text
        parser = getImage(link)
        all_ = parser.find_all('source', attrs={'srcset' : True})
        elements = [x['srcset'].split()[0] for x in all_]
        for x in elements:
            image = requests.get(x,headers=headers)
            await context.bot.send_photo(chat_id=update.effective_chat.id,photo=image.content)
        await context.bot.send_message(chat_id=update.effective_chat.id,text='hameye axa ersal shod bazam dar khedmatam' )
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,text='link eshtebahe lotfan dobare link ro bede')
    finally:
        await context.bot.send_message(chat_id=update.effective_chat.id,text='mikhay edame bedi?',reply_markup=markup_edame)
        return resume
    
async def get_image_mango(update: Update,context: ContextTypes.DEFAULT_TYPE):
    try:    
        link = update.message.text
        parser = getImage(link)
        all_ = parser.find_all('script')
        elements = []
        for x in all_:
            y = x.string
            if y is None:
                continue
            elif 'dataLayerV2Json' in y:
                elements.append(y)
        javab = elements[0].split(';')[0]
        n = javab.find('{')
        jj = json.loads(javab[n:])
        dict_jj = jj['ecommerce']['detail']['products'][0]['photos']
        for x in dict_jj.values():
            image = requests.get(x,headers=headers)
            await context.bot.send_photo(chat_id=update.effective_chat.id,photo=image.content)
        await context.bot.send_message(chat_id=update.effective_chat.id,text='hameye axa ersal shod bazam dar khedmatam')
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,text='link eshtebahe lotfan dobare link ro bede')
    finally:
        await context.bot.send_message(chat_id=update.effective_chat.id,text='mikhay edame bedi?',reply_markup=markup_edame)
        return resume

async def get_image_adidas(update: Update,context: ContextTypes.DEFAULT_TYPE):
    try:    
        link = update.message.text
        parser = getImage(link)
        all_ = parser.find_all('div',attrs={'class': 'content___3m-ue'})
        for x in all_:
            img_tag = x.find('img')
            image_links = img_tag['srcset']
            image = requests.get(image_links.split()[-2],headers=headers)
            await context.bot.send_photo(chat_id=update.effective_chat.id,photo=image.content)
        await context.bot.send_message(chat_id=update.effective_chat.id,text='hameye axa ersal shod bazam dar khedmatam')
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,text='link eshtebahe lotfan dobare link ro bede')
    finally:
        await context.bot.send_message(chat_id=update.effective_chat.id,text='mikhay edame bedi?',reply_markup=markup_edame)
        return resume

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text='mersi ke az man estefade kardi\nharvaght khasti \'/start\' ro bezani man dar khedmatam')
    await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAAEG7JljouhYWc9TdXnDJbS29Hqpz0wBpAACDgADr8ZRGrdbgux-ASf3LAQ')

    return ConversationHandler.END

async def Error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id,text=f'dastor ya linki ke behem midi eshtebahe\ndasture vared shode:{t}')
    return getpickey

async def get_price_data(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text='lotfan nerkhe mahsul ro behem bede')
    return calculate

async def chanel_messege(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=-1001255095528,text='salam salam')
    return menuKey

async def set_lir(update:Update,context:ContextTypes.DEFAULT_TYPE):
    global lir_price
    lir_price = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id,text=f'gheymate lir be {lir_price} taghir kard\nbe menuye asli bar gashtid',reply_markup=markup_menu)
    return menuKey

async def calculate_price(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        price = update.message.text
        price = int(price)
        if price <= 100:
            sud = 0.4
        elif price <= 500:
            sud = 0.35
        elif price <= 1000:
            sud = 0.3
        elif price <= 2000:
            sud = 0.25
        else:
            sud = 0.2
        n = (price + (price*sud)) * int(lir_price)
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'gheymat nahayi mahsul: {n:,} tooman\nin gheymat ba lir {lir_price} mohasebe shode')
    except NameError:
        await context.bot.send_message(chat_id=update.effective_chat.id,text='geymat lir tarif nashode')
    finally:
        await context.bot.send_message(chat_id=update.effective_chat.id,text='be menuye asli bargashtim',reply_markup=markup_menu)
        return menuKey

async def get_lir(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text='lotfan gheymat lir ro be man begu')
    return lir

def main():
    application = ApplicationBuilder().token(token).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            menuKey: [CommandHandler('matn', eslah),
                    CommandHandler('getPic', get_pic),
                    CommandHandler('nerkh',get_price_data),
                    CommandHandler('gheymat_lir',get_lir),
                    CommandHandler('send_message_channel',chanel_messege)],
            getpickey: [MessageHandler(filters.Regex('^http.*zara\.com.*'),get_image_zara),
                MessageHandler(filters.Regex('^http.*mango\.com.*'),get_image_mango),
                MessageHandler(filters.Regex('^http.*adidas\.com.*'),get_image_adidas),
                MessageHandler(filters.Regex(filters.TEXT & ~(filters.COMMAND)),Error)],
            matnKey: [MessageHandler(filters.TEXT & ~(filters.COMMAND), eslahe_matn)],
            resume: [CommandHandler('YES',get_pic),CommandHandler('NO',cancel)],
            calculate:[MessageHandler(filters.TEXT & ~(filters.COMMAND),calculate_price)],
            lir: [MessageHandler(filters.TEXT & ~(filters.COMMAND),set_lir)],
                },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    # start_handler = CommandHandler('start', start)
    # start_handler = CommandHandler('zara',zara)
    # application.add_handler(start_handler)
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()