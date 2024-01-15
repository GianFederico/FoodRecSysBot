import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import google.cloud.dialogflow_v2 as dialogflow
from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler
import constants as keys
from recommender_script import Recommendation, Recommendation_due
from expl_script import Spiegazione
import nest_asyncio
import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)


# Definizione degli stati di conversazione
GENDER, AGE, HT_LIFESTYLE_IMPORTANCE, HT_LIFESTYLE, CM, KG, COOK_EXP, MAX_COST_REC, TIME_COOK, GOALS, MOOD, PH_ACTIVITY, SLEEP,STRESS, DEPRESS, LOWNICKEL, VEGETERIAN, LACTOSEFREE,GLUTENFREE,LIGHT, DIABETES, PREGNANT, CATEGORY= range(23)
 
# Funzione di gestione del comando /start
async def start(update: Update, context):
    await update.message.reply_text('Great! I\'ll ask you some questions to get to know you better.\nWhat is you gender?')
    return GENDER

############################################################################################################
# Funzione di gestione della risposta sul sesso
async def gender(update: Update, context):
    user_gender = update.message.text.lower()
    # Controllo sulla validità del sesso
    if user_gender not in ['man', 'woman', 'unspecified']:
        await update.message.reply_text("You need to type 'man', 'woman' or 'unspecified' if you don't want to specify it.")
        return GENDER
    else:
        if user_gender == "man":
                context.user_data['gender'] = "m"
        elif user_gender == "woman":
                context.user_data['gender'] = "f"
        await update.message.reply_text('How old are you?')
        return AGE
   
############################################################################################################
# Funzione di gestione della risposta sull'età
async def age(update: Update, context):
    user_age = update.message.text
    if 0 < int(user_age) < 19:
        user_age='U20'
    elif 20 <= int(user_age) < 29:
        user_age='U30'
    elif 30 <= int(user_age) < 39:
        user_age='U40'
    elif 40 <= int(user_age) < 49:
        user_age='U50'
    elif 50 <= int(user_age) < 59:
        user_age='U60'
    elif int(user_age) >= 60:
        user_age='O60'
    # Controllo sulla validità dell'età
    if user_age not in ['U20','U30', 'U40','U50','U60','O60']:
        await update.message.reply_text('Sorry I did not get your age, can you insert it again? (only the number is good)')
        return AGE
    else:
        if context.user_data['gender']=="f":
            keyboard = [['Yes','No']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text('Are you pregnant?',reply_markup=reply_markup)
        else:
            await update.message.reply_text('How tall are you? (cm)')
            return CM
        # keyboard = [['Molto importante', 'Importante','Poco importante'], ['Non importante','Assolutamente non importante']]
        # reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        # await update.message.reply_text('Quanto è importante per te avere uno stile di vita salutare?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)
        return PREGNANT

############################################################################################################
# Funzione di gestione della risposta sull'essere incinta
async def pregnant(update: Update, context):
    user_pregnant= update.message.text.lower()
    if context.user_data['gender']=='f':
        if user_pregnant not in ['yes','no']:
            await update.message.reply_text("Gentilmente rispondimi con uno dei miei suggerimenti.")
            return PREGNANT
        else:
            if user_pregnant == "yes":
                context.user_data['pregnant'] = 1
            if user_pregnant == "no" :
                context.user_data['pregnant'] = 0
    else: context.user_data['pregnant'] = 0
    await update.message.reply_text('How tall are you? (cm)')
    return CM

############################################################################################################
# Funzione di gestione della risposta sull'altezza
async def height(update: Update, context):
    user_height = update.message.text

    # Controllo sulla validità dell'altezza
    if not user_height.isdigit() or int(user_height) < 90 or int(user_height) > 230:
        await update.message.reply_text('Insert an height between 100cm and 230cm')
        return CM
    else:
        context.user_data['height'] = int(user_height)
        await update.message.reply_text('What is your weight? (kg)')
        return KG
    
############################################################################################################
# Funzione di gestione della risposta sul peso
async def weight(update: Update, context):
    user_weight = update.message.text
    # Controllo sulla validità del peso
    if not user_weight.isdigit() or int(user_weight) < 30 or int(user_weight) > 150:
        await update.message.reply_text('You must insert a number, round it up to the nearest integer. ')
        return KG
    else:
        user_bmi = float(int(user_weight)*10000/(context.user_data['height']*context.user_data['height']))
        if user_bmi < 18:
            context.user_data['weight'] = "under"
        elif 18 <= user_bmi < 25:
            context.user_data['weight'] = "normal"
        elif user_bmi >= 25:
            context.user_data['weight'] = "over"
        #print(user_bmi)
        # keyboard = [['Molto facile', 'Facile','Media'],['Difficile','Molto difficile']]
        # reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        # await update.message.reply_text('Come dovrebbe essere la preparazione di un piatto fatto da te?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)
        # return COOK_EXP
        keyboard = [['Lose','Maintain', 'Gain']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('What are your goals regarding your weight?',reply_markup=reply_markup)
        return GOALS

############################################################################################################
# Funzione di gestione della risposta sull'obiettivo
async def goals(update: Update, context):
    user_goals = update.message.text.lower()
    # Controllo sulla validità dell'obiettivo
    if user_goals not in ['lose','gain','maintain']:
        await update.message.reply_text("Please select or type one of the options.")
        return GOALS
    else:
        if user_goals == "lose":
            context.user_data['goals'] = -1
        if user_goals == "gain":
            context.user_data['goals'] = 1
        if user_goals == "maintain":
            context.user_data['goals'] = 0
        # keyboard = [['Bene', 'Neutro'],['Male']]
        # reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        # await update.message.reply_text('Come ti senti attualmente?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)
        # return MOOD
        keyboard = [['A lot (>2)', 'Just enough (1-2)', 'Not so much (<1)']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('How much physical activity do you practice weekly?',reply_markup=reply_markup)
        return PH_ACTIVITY
    
############################################################################################################
# Funzione di gestione della risposta sull'attività fisica
async def ph_activity(update: Update, context):
    user_ph_activity = update.message.text.lower()
    # Controllo sulla validità del mood
    if user_ph_activity not in ['a lot (>2)', 'just enough (1-2)', 'not so much (<1)']:
        await update.message.reply_text("Devi inserire una tra le opzioni da me suggerite.")
        return PH_ACTIVITY
    else:
        if user_ph_activity == "a lot (>2)":
            context.user_data['ph_activity'] = "high"
        if user_ph_activity == "just enough (1-2)":
            context.user_data['ph_activity'] = "normal"
        if user_ph_activity == "not so much (<1)":
            context.user_data['ph_activity'] = "low"       
        
        keyboard = [['Yes','No']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Are you LACTOSE intolerant?',reply_markup=reply_markup)
        return LACTOSEFREE

############################################################################################################
# Funzione di gestione della risposta sull'essere vegetariani
async def vegetarian(update: Update, context):
    user_vegetarian= update.message.text.lower()
    if user_vegetarian not in ['yes','no']:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return VEGETERIAN
    else:
        if user_vegetarian == "yes" :
            context.user_data['vegetarian'] = 1
        if user_vegetarian == "no" :
            context.user_data['vegetarian'] = 0
        keyboard = [['First courses','Second courses', 'Desserts']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Ok, we are done! Which type of recipes do you want me to suggest?', reply_markup=reply_markup)
        return CATEGORY

############################################################################################################
# Funzione di gestione della risposta sull'intolleranza al lattosio
async def lactosefree(update: Update, context):
    user_lactosefree= update.message.text.lower()
    if user_lactosefree not in ['yes','no']:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return LACTOSEFREE
    else:
        if user_lactosefree == "yes":
            context.user_data['lactosefree'] = 1
        if user_lactosefree == "no" :
            context.user_data['lactosefree'] = 0
        keyboard = [['Yes','No']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Are you GLUTEN intolerant?',reply_markup=reply_markup)
        return GLUTENFREE

############################################################################################################
# Funzione di gestione della risposta sull'intolleranza al glutine
async def glutenfree(update: Update, context):
    user_glutenfree= update.message.text.lower()
    if user_glutenfree not in ['yes','no']:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return GLUTENFREE
    else:
        if user_glutenfree == "yes" :
            context.user_data['glutenfree'] = 1
        if user_glutenfree == "no" :
            context.user_data['glutenfree'] = 0
        keyboard = [['Yes','No']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Are you DIABETIC?',reply_markup=reply_markup)
        return DIABETES

############################################################################################################
# Funzione di gestione della risposta sull'essere diabetici
async def diabetes(update: Update, context):
    user_diabetes= update.message.text.lower()
    if user_diabetes not in ['yes','no']:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return DIABETES
    else:
        if user_diabetes == "yes":
            context.user_data['diabetes'] = 1
        if user_diabetes == "no" :
            context.user_data['diabetes'] = 0
        keyboard = [['Yes','No']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Are you vegetarian?', reply_markup=reply_markup)
        return VEGETERIAN

############################################################################################################
# Funzione di gestione della risposta sulla scelta dei piatti da suggerire
async def category(update: Update, context):
    user_category= update.message.text.lower()
    if user_category not in ['first courses','second course', 'desserts']:
        await update.message.reply_text("Please type one between 'First courses','Second courses' or 'Desserts'")
        return CATEGORY
    else:
        context.user_data['category'] = user_category
        reply_markup = ReplyKeyboardRemove()
        await update.message.reply_text('Thank you for your time, now you can ask me something to eat!',reply_markup=reply_markup)
        return ConversationHandler.END 




###########_domande non obbligatorie_#######################################################################
############################################################################################################
# Funzione di gestione della risposta sull'importanza di uno stile di vita healthy
async def ht_lifestyle_importance(update: Update, context):
    user_lifestyle_importance = update.message.text.lower()

    # Controllo sulla validità dell'importanza di uno stile di vita healthy
    if user_lifestyle_importance not in ['molto importante', 'importante', 'non importante', 'poco importante', 'assolutamente non importante']:
        await update.message.reply_text("Devi inserire una tra le opzioni da me suggerite.")
        return HT_LIFESTYLE_IMPORTANCE
    else:
        if user_lifestyle_importance=="molto importante":
            context.user_data['ht_lifestyle_importance'] = 5
        elif user_lifestyle_importance=="importante":
            context.user_data['ht_lifestyle_importance'] = 4
        elif user_lifestyle_importance=="poco importante":
            context.user_data['ht_lifestyle_importance'] = 3
        elif user_lifestyle_importance=="non importante":
            context.user_data['ht_lifestyle_importance'] = 2
        elif user_lifestyle_importance=="assolutamente non importante":
            context.user_data['ht_lifestyle_importance'] = 1
        keyboard = [['Molto salutare', 'Salutare','Poco salutare'], ['Non salutare','Assolutamente non salutare']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Tu invece come consideri il tuo stile di vita?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)
        return HT_LIFESTYLE

#############################################################################################################
# Funzione di gestione della risposta sull'healthy lifestyle
async def ht_lifestyle(update: Update, context):
    user_lifestyle = update.message.text.lower()
    # Controllo sulla validità dell'healthy lifestyle
    if user_lifestyle not in ['molto salutare', 'salutare', 'non salutare', 'poco salutare', 'assolutamente non salutare']:
        await update.message.reply_text("Gentilmente rispondimi con uno dei miei suggerimenti.")
        return HT_LIFESTYLE
    else:
        if user_lifestyle=="molto salutare":
            context.user_data['ht_lifestyle'] = 5
        elif user_lifestyle=="salutare":
            context.user_data['ht_lifestyle'] = 4
        elif user_lifestyle=="poco salutare":
            context.user_data['ht_lifestyle'] = 3
        elif user_lifestyle=="non salutare":
            context.user_data['ht_lifestyle'] = 2
        elif user_lifestyle=="assolutamente non salutare":
            context.user_data['ht_lifestyle'] = 1
        reply_markup = ReplyKeyboardRemove()
        await update.message.reply_text('Sapresti dirmi la tua altezza in cm?', reply_markup=reply_markup)
        return CM

############################################################################################################
# Funzione di gestione della risposta sull'esperienza di cucina
async def cook_exp(update: Update, context):
    user_cook_exp = update.message.text.lower()
    # Controllo sulla validità dell'esperienza di cucina
    if user_cook_exp not in ['molto facile','facile','media','difficile', 'molto difficile']:
        await update.message.reply_text("Gentilmente rispondimi con uno dei miei suggerimenti.")
        return COOK_EXP
    else:
        if user_cook_exp == "molto facile":
            context.user_data['cook_exp'] = 1
        elif user_cook_exp == "facile":
            context.user_data['cook_exp'] = 2
        elif user_cook_exp == "media":
            context.user_data['cook_exp'] = 3
        elif user_cook_exp == "difficile":
            context.user_data['cook_exp'] = 4
        elif user_cook_exp == "molto difficile":
            context.user_data['cook_exp'] = 5
            
        keyboard = [['Molto basso', 'Basso'],['Medio','Elevato', 'Non importante']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Quanto potrebbe essere il tuo budget per preparare una ricetta?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)
        return MAX_COST_REC

############################################################################################################
# Funzione di gestione della risposta sul costo massimo di una ricetta
async def max_cost_rec(update: Update, context):
    user_max_cost_rec = update.message.text.lower()
    # Controllo sulla validità del costo massimo di una ricetta
    if user_max_cost_rec not in ['molto basso','basso','medio','elevato', 'non importante']:
        await update.message.reply_text("Devi inserire una tra le opzioni da me suggerite.")
        return MAX_COST_REC
    else:
        if user_max_cost_rec == "molto basso":
            context.user_data['max_cost_rec'] = 1
        elif user_max_cost_rec == "basso":
            context.user_data['max_cost_rec'] = 2
        elif user_max_cost_rec == "medio":
            context.user_data['max_cost_rec'] = 3
        elif user_max_cost_rec == "elevato":
            context.user_data['max_cost_rec'] = 4
        elif user_max_cost_rec == "non importante":
            context.user_data['max_cost_rec'] = 5

        reply_markup = ReplyKeyboardRemove()
        await update.message.reply_text('Quanto è in media il tuo tempo disponibile per cucinare espresso in minuti?\n(Puoi inserire un numero da 0 a 200) ', reply_markup=reply_markup)
        return TIME_COOK
    
############################################################################################################
# Funzione di gestione della risposta sul tempo di cucina
async def time_cook(update: Update, context):
    user_time_cook = update.message.text.lower()

    # Controllo sulla validità del tempo di cucina
    if not user_time_cook.isdigit() or int(user_time_cook) < 0 or int(user_time_cook) > 200:
        await update.message.reply_text('Devi inserire un numero intero indicativo per la mia domanda.')
        return TIME_COOK
    else:
        context.user_data['time_cook'] = int(user_time_cook)
        keyboard = [['Perderne', 'Acquisirne'],['Nessuno']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Qual è il tuo obiettivo in termini di peso?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)
        return GOALS

############################################################################################################
# Funzione di gestione della risposta sul mood
async def mood(update: Update, context):
    user_mood = update.message.text.lower()
    # Controllo sulla validità del mood
    if user_mood not in ['bene','neutro','male']:
        await update.message.reply_text("Gentilmente rispondimi con uno dei miei suggerimenti.")
        return MOOD
    else:
        if user_mood=="bene":
            context.user_data['mood'] = "good"
        elif user_mood=="male":
            context.user_data['mood'] = "bad"
        else:
            context.user_data['mood'] = "neutral"
        keyboard = [['Tanta', 'Media'],['Poca']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Quanta attività fisica fai in una settimana?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)
        return PH_ACTIVITY

############################################################################################################
# Funzione di gestione della risposta sul sonno
async def sleep(update: Update, context):
    user_sleep = update.message.text.lower()
    # Controllo sulla validità del sonno
    if user_sleep not in ['8-','8+']:
        await update.message.reply_text("Gentilmente rispondimi con uno dei miei suggerimenti.")
        return SLEEP
    else:
        if user_sleep == "8-":
            context.user_data['sleep'] = "low"
        if user_sleep == "8+":
            context.user_data['sleep'] = "good"
        keyboard = [['Si', 'No']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Ti senti stressato in questo periodo?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)
        return STRESS
    
############################################################################################################
# Funzione di gestione della risposta sullo stress
async def stress(update: Update, context):
    user_stress = update.message.text.lower()
    # Controllo sulla validità dello stress
    if user_stress not in ['sì','no', 'si']:
        await update.message.reply_text("Devi inserire una tra le opzioni da me suggerite.")
        return STRESS
    else:
        if user_stress == "si" or "sì":
            context.user_data['stress'] = 1
        if user_stress == "no" :
            context.user_data['stress'] = 0
        keyboard = [['Si', 'No']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Ti senti depresso in questo periodo?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)

        return DEPRESS

############################################################################################################
# Funzione di gestione della risposta sulla depressione
async def depress(update: Update, context):
    user_depress = update.message.text.lower()
    if user_depress not in ['sì','no', 'si']:
        await update.message.reply_text("Gentilmente rispondimi con uno dei miei suggerimenti.")
        return DEPRESS
    else:
        if user_depress == "si" or "Si" or "Sì" or "sì":
            context.user_data['depress'] = 1
        if user_depress == "no" :
            context.user_data['depress'] = 0
        keyboard = [['Si','No']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Grazie! Ancora poche domande ed abbiamo terminato. Hai bisogno di ricette con basso Nickel?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)
        return LOWNICKEL
    
############################################################################################################
# Funzione di gestione della risposta sul nickel basso
async def nickel(update: Update, context):
    user_nickel= update.message.text.lower()
    # Controllo sulla validità dello stress
    if user_nickel not in ['sì','no', 'si']:
        await update.message.reply_text("Devi inserire una tra le opzioni da me suggerite.")
        return LOWNICKEL
    else:
        if user_nickel == "si" or "Si" or "Sì" or "sì":
            context.user_data['nickel'] = 1
        if user_nickel == "no" :
            context.user_data['nickel'] = 0
        keyboard = [['Si','No']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Sei vegetariano?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)
        return VEGETERIAN

############################################################################################################
# Funzione di gestione della risposta sui pochi grassi
async def light(update: Update, context):
    user_light= update.message.text.lower()
    if user_light not in ['sì','no', 'si']:
        await update.message.reply_text("Gentilmente rispondimi con uno dei miei suggerimenti.")
        return LIGHT
    else:
        if user_light == "si" or "sì":
            context.user_data['light'] = 1
        if user_light == "no" :
            context.user_data['light'] = 0
        keyboard = [['Si','No']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text('Sei diabetico/a?\n(Hai a disposizione dei pulsanti per rispondere alla mia domanda)',reply_markup=reply_markup)
        return DIABETES

############################################################################################################
############################################################################################################
    



#UTILS
def error(update, context):
    logging.error(f"Update {update}   caused error {context.error}")
     
async def aiuto (update: Update, context):
    await update.message.reply_text("Sono FoodRecSysBot, il bot che ti aiuta a scegliere cosa mangiare!\nPuoi chiedere di suggerirti un piatto che in base alle tue caratteristiche andrà benissimo per te!\nPuoi avere dei consigli su questo piatto, se va bene per te, se è attinente a ciascuna delle informazioni che mi hai dato! Infatti, puoi domandarmi:\nuna spiegazione/descrizione generale del piatto;\nse è adatto ai tuoi obiettivi;\nse è adatto alle tue restrizioni;\nse è attinente al tuo stile di vita;\nse è adatto alla tua età;\nse il suo costo è attinente con la tua disponibilità;\nse il suo tempo di cottura è attinente con il tuo tempo a disposizione;\nquali sono i suoi benefici e quali sono i suoi rischi;\ne perfino se è coerente con la tua esperienza di cucina!\nDopo di che potrai chiedermi di suggerirti anche un altro piatto, e posso confrontarti le caratteristiche dei due piatti rispetto a tutte le caratteristiche di essi.\nInoltre se hai bisogno di cambiare i tuoi dati, premi questo tasto /start per iniziare di nuovo.")

async def unknown(update: Update, context):
   await update.message.reply_text("Mi dispiace, non ho capito. Puoi ripetere la tua risposta?")
   return GENDER

# Funzione per inviare il messaggio a Dialogflow e restituire la risposta
def dialogflow_mode(update, context):
    # Id del progetto Dialogflow
    DIALOGFLOW_PROJECT_ID = 'foodrecsys-kbji'
    # Credenziali del progetto Dialogflow
    DIALOGFLOW_CREDENTIALS = 'foodrecsys-kbji-b7a61301de6a.json'
    # Recupera l'ID dell'utente e imposta la lingua del messaggio
    session_id = update.effective_user.id
    language_code = 'it'
    # Crea il client di sessione di Dialogflow
    session_client = dialogflow.SessionsClient.from_service_account_file(DIALOGFLOW_CREDENTIALS)
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
    # Invia il messaggio a Dialogflow
    Text = update.message.text.strip()
    if not Text:
        return
    text_input = dialogflow.types.TextInput(text=Text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    print(session, query_input)
    with session_client as client:
        response = client.detect_intent(session=session, query_input=query_input)

    # Invia la risposta di Dialogflow all'utente
    intent = response.query_result.intent.display_name
    if intent == 'Introduction':
        print("intent introduction")
    if intent == 'Suggerimento del cibo':
        Recommendation.suggerimento(update, context)
    if intent == 'Controllo del piatto':
        Spiegazione.controllo_piatto(update, context)
    if intent == 'Popolarità_un_piatto':
        Spiegazione.spiegazione_popolarita(update, context)
    if intent == 'Spiegazione del cibo':
        Spiegazione.spiegazione_piatto(update, context)
    if intent == 'Spiegazione del cibo, Abilità di cucina':
        Spiegazione.spiegazione_skill_cucina(update, context)           
    if intent == 'Spiegazione del cibo, Obiettivi':
        Spiegazione.spiegazione_obiettivo(update, context)
    if intent == 'Spiegazione del cibo, Benefici di salute':
        Spiegazione.spiegazione_benefici_salute(update, context)
    if intent == 'Spiegazione del cibo, Rischi di Salute':
        Spiegazione.spiegazione_rischi_salute(update, context)
    if intent == 'Spiegazione del cibo, Costo':
        Spiegazione.spiegazione_costo(update, context)
    if intent == 'Spiegazione del cibo, Età':
        Spiegazione.spiegazione_eta(update, context)
    if intent == 'Spiegazione del cibo, Restrizioni':
        Spiegazione.spiegazione_restrizioni(update, context)
    if intent == 'Spiegazione del cibo, Stile di vita':
        Spiegazione.spiegazione_lifestyle(update, context)
    if intent == 'Spiegazione del cibo, Tempo':
        Spiegazione.spiegazione_tempo(update, context)
    if intent == 'Altro suggerimento del piatto':
        Recommendation_due.altro_suggerimento(update, context)
    if intent == 'Controllo del piatto due piatti':
        Spiegazione.controllo_piatto_due_piatti(update, context)
    if intent == 'Popolarità_due_piatti':
        Spiegazione.spiegazione_popolarita_due_piatti(update, context)
    if intent == 'Spiegazione del cibo due piatti':
        Spiegazione.spiegazione_piatto_due_piatti(update, context)
    if intent == 'Spiegazione del cibo - Abilità di cucina due ricette':
        Spiegazione.spiegazione_skill_cucina_due_piatti(update, context)           
    if intent == 'Spiegazione del cibo, Obiettivi_due_ricette':
        Spiegazione.spiegazione_obiettivi_due_piatti(update, context)
    if intent == 'Spiegazione del cibo, Benefici di salute due piatti':
        Spiegazione.spiegazione_benefici_salute_due_piatti(update, context)
    if intent == 'Spiegazione del cibo, Rischi di Salute due piatti':
        Spiegazione.spiegazione_rischi_salute_due_piatti(update, context)
    if intent == 'Spiegazione del cibo, Costo due piatti':
        Spiegazione.spiegazione_costo_due_piatti(update, context)
    if intent == 'Spiegazione del cibo, Età due piatti':
        Spiegazione.spiegazione_eta_due_piatti(update, context)
    if intent == 'Spiegazione del cibo, Restrizioni due ricette':
        Spiegazione.spiegazione_restrizioni_due_piatti(update, context)
    if intent == 'Spiegazione del cibo, Stile di vita due piatti':
        Spiegazione.spiegazione_lifestyle_due_piatti(update, context)
    if intent == 'Spiegazione del cibo, Tempo due piatti':
        Spiegazione.spiegazione_tempo_due_piatti(update, context)
    confidence = response.query_result.intent_detection_confidence
    print("Intent:", intent)
    print("Confidence:", confidence)
    return update.message.reply_text(response.query_result.fulfillment_text)

async def main():
    nest_asyncio.apply()
    # Inizializzazione del logger
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    # Definizione dei comandi e dei gestori di messaggi
    application = Application.builder().token(keys.API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create', start)],
        states={
            GENDER: [MessageHandler(filters.TEXT, gender)],
            AGE: [MessageHandler(filters.TEXT, age)],
            PREGNANT:[MessageHandler(filters.TEXT, pregnant)],
            CM:[MessageHandler(filters.TEXT, height)],
            KG:[MessageHandler(filters.TEXT, weight)],
            GOALS:[MessageHandler(filters.TEXT, goals)],
            PH_ACTIVITY:[MessageHandler(filters.TEXT, ph_activity)],
            LACTOSEFREE:[MessageHandler(filters.TEXT, lactosefree)],
            GLUTENFREE:[MessageHandler(filters.TEXT, glutenfree)],
            DIABETES:[MessageHandler(filters.TEXT, diabetes)],
            VEGETERIAN:[MessageHandler(filters.TEXT, vegetarian)],
            CATEGORY:[MessageHandler(filters.TEXT, category)]
            #HT_LIFESTYLE_IMPORTANCE:[MessageHandler(filters.TEXT, ht_lifestyle_importance)],
            #HT_LIFESTYLE:[MessageHandler(filters.TEXT,ht_lifestyle )],
            #COOK_EXP:[MessageHandler(filters.TEXT, cook_exp)],
            #MAX_COST_REC:[MessageHandler(filters.TEXT, max_cost_rec)],
            #TIME_COOK:[MessageHandler(filters.TEXT, time_cook)],
            #MOOD:[MessageHandler(filters.TEXT, mood)],
            #SLEEP:[MessageHandler(filters.TEXT, sleep)],
            #STRESS:[MessageHandler(filters.TEXT, stress)],
            #DEPRESS:[MessageHandler(filters.TEXT, depress)],
            #LOWNICKEL:[MessageHandler(filters.TEXT, nickel)],
            #LIGHT:[MessageHandler(filters.TEXT, light)],
        },
            fallbacks=[MessageHandler(filters.TEXT, unknown)]   
    )
    application.add_handler(conv_handler)
    # application.add_handler(CommandHandler('help',aiuto))
    # application.add_handler(CommandHandler('aiuto',aiuto))
    # application.add_handler(CommandHandler('info',aiuto))

    # Aggiunta del CommandHandler per il cambio modalità
    application.add_handler(MessageHandler(filters.TEXT, dialogflow_mode))

    # Aggiunta dell'ErrorHandler
    application.add_error_handler(error)

    logging.info("Bot avviato")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
     asyncio.run(main())
