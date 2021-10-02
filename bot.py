import os 

from telegram.ext import Updater , CommandHandler,CallbackQueryHandler , InlineQueryHandler ,MessageHandler , Filters


from telegram import InlineKeyboardMarkup , InlineKeyboardButton

from googlesearch import search
import difflib


	
def repo(update, context):

    update.message.reply_text('Acá encontraras el Código del Bot con el que podrás elaborar uno propio.\n\nhttps://github.com/Luamcho/google-telegram-bot')	
	
		    			
def start(update, context):
    name=update.effective_user.first_name
    update.message.reply_text(
        text=f'Hola {name} Para hacer una Búsqueda en Google puedes poner el comando /buscar . ',
        reply_markup=InlineKeyboardMarkup([                          
            [InlineKeyboardButton(text='⚜️ Desarrollador ⚜️', url='https://t.me/Luamcho')],
	    [InlineKeyboardButton(text='🔰 Repo 🔰', url='https://github.com/Luamcho/google-telegram-bot')],	
        ])
    )


   
#Comando que inicia Start

def buscar(Update,context):
	
	name=Update.effective_user.first_name		
	
	
	Update.message.reply_text(text=
	f"<b>👋Hola {name}:\n\n"
	"🔍Escribe lo que quieres buscar "
	"</b>", 
	parse_mode="html")


def messagehandler(Update,context):
	
	text=Update.message.text
	
	'''
	GUARDAR DATOS EN CACHE
	'''
	context.user_data['text']=text
	
	boton1=InlineKeyboardButton(text=
	"Si ✅" ,callback_data="call_yes")
	
	
	boton2=InlineKeyboardButton(text=
	"No ❌" ,callback_data="call_no")
		
	
	
	
	Update.message.reply_text(text=
	"<b>🤔¿Estás seguro de que quieres buscar esto?"
	f"\n<u>👉{text}</u></b>",
	parse_mode="html",
	reply_markup=
	InlineKeyboardMarkup([
	[boton1 , boton2]
	]))
	
def callback_no(Update,context):
	
	query=Update.callback_query
	
	query.answer()
	
	query.edit_message_text(text=
	"<b>📝reescribe lo que"
	" deceas buscar</b>",
	parse_mode="html"
	)

def callback_yes(Update,context):
	
	consulta=context.user_data.get('text','not found')
	
	
	query=Update.callback_query
	
	query.answer()
	
	query.edit_message_text(text=
	"<b>🧐 buscando ..."
	"</b>",
	parse_mode="html")
	

	
	results = search(consulta, 
	stop = 10 )
	
	result=[]
	n = 1
	for i in results:
		x = i
		i = i.replace("/" , " ")
		i = i.replace(".html","")
		y = i.split()
		sitio=y[1]
		
		txtf=difflib.get_close_matches(consulta,
		possibilities=y,
		n=1,cutoff=0.4)
		
		txtf="".join(txtf)
		
		
		
		title=txtf.replace("-"," ")
		
		
		if str(sitio).__contains__(title) and "www.youtube.com" not in sitio :
			t=y[-1]
			title=t.replace("-", " ")
			result.append(
		f"#{n} Sitio: <code>{sitio}</code>"
		f'\n👉<a href="{x}">{title}</a>')			
		
		
		
		elif title != "" and "?" not in title:
			result.append(
		f"#{n} Sitio: <code>{sitio}</code>"
		f'\n👉<a href="{x}">{title}</a>')
		
		elif str(i).__contains__("www.youtube.com"):
			result.append(
		f"#{n} Sitio: <code>{sitio}</code>"
		f'\n👉<a href="{x}">View on Youtube</a>')				
		
			
		
		
		
		else:
			result.append(
		f"#{n} Sitio: <code>{sitio}</code>"
		f'\n👉<a href="{x}">LINK</a>')		
		
		
		n += 1
		
		
	
	r="\n".join(result)
	
	query.edit_message_text(text=
	"<b>📄Resultados: "
	f"<u>{consulta}</u>\n\n{r}"
	"</b>",
	parse_mode="html",
	disable_web_page_preview=
	True)
	

	



if __name__ == '__main__':

	updater = Updater(token=os.environ ['TOKEN'], use_context=True)
	
	update = Updater
	dp = updater.dispatcher
	
	
	dp.add_handler(CommandHandler('repo', repo))
	
	dp.add_handler(CommandHandler('start', start))

	dp.add_handler(CommandHandler('buscar', buscar))
	
	dp.add_handler(CallbackQueryHandler(pattern="call_yes" , callback=callback_yes))
	
	dp.add_handler(CallbackQueryHandler(pattern="call_no",callback=callback_no))		
	
	
	dp.add_handler(MessageHandler(Filters.text , messagehandler))	
	
		
	updater.start_polling()
	print("Corriendo...")
	updater.idle()
	
