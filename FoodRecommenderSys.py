import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import google.cloud.dialogflow_v2 as dialogflow
from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler
import constants as keys
from recommender_script import Recommendation, Recommendation_due, Recommendation_tre, SpecificRec
from expl_script import Spiegazione
import nest_asyncio
import asyncio
import random
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Definizione degli stati di conversazione
(
    GENDER,
    AGE,
    HT_LIFESTYLE_IMPORTANCE,
    HT_LIFESTYLE,
    CM,
    KG,
    COOK_EXP,
    MAX_COST_REC,
    TIME_COOK,
    GOALS,
    MOOD,
    PH_ACTIVITY,
    SLEEP,
    STRESS,
    DEPRESS,
    LOWNICKEL,
    VEGETERIAN,
    LACTOSEFREE,
    GLUTENFREE,
    LIGHT,
    DIABETES,
    PREGNANT,
    CATEGORY,
    ATTRIBUTE,
    TO_CHOICES,

    PRE_FIRST_COURSE_HEALTINESS,
    PRE_SECOND_COURSE_HEALTINESS,
    PRE_DESSERT_HEALTINESS,

    PRE_FIRST_COURSE_SUSTAINABILITY,
    PRE_SECOND_COURSE_SUSTAINABILITY,
    PRE_DESSERT_SUSTAINABILITY,

    POST_FIRST_COURSE_HEALTINESS,
    POST_SECOND_COURSE_HEALTINESS,
    POST_DESSERT_HEALTINESS,

    POST_FIRST_COURSE_SUSTAINABILITY,
    POST_SECOND_COURSE_SUSTAINABILITY,
    POST_DESSERT_SUSTAINABILITY,
    HEALTHINESS_LEVEL,
    HEALTHINESS_INTEREST,
    SUSTAINABILITY_LEVEL,
    SUSTAINABILITY_INTEREST
) = range(41) #range(25)


# Funzione di gestione del comando /start
async def start(update: Update, context):
    await update.message.reply_text(
        "Great! I'll ask you some questions to get to know you better.\nWhat is you gender?"
    )
    return GENDER


############################################################################################################
# Funzione di gestione della risposta sul sesso
async def gender(update: Update, context):
    user_gender = update.message.text.lower()
    # Controllo sulla validità del sesso
    if user_gender not in ["man", "woman", "unspecified"]:
        await update.message.reply_text(
            "You need to type 'man', 'woman' or 'unspecified' if you don't want to specify it."
        )
        return GENDER
    else:
        if user_gender == "man":
            context.user_data["gender"] = "m"
            context.user_data["pregnant"] = 0
        elif user_gender == "woman":
            context.user_data["gender"] = "f"
        elif user_gender == "unspecified":
            context.user_data[
                "gender"
            ] = "u"  # TODO CHECK WHAT LETTER CORRESPONDS TO UNSPECIFIED
        await update.message.reply_text("How old are you?")
        return AGE


############################################################################################################
# Funzione di gestione della risposta sull'età
async def age(update: Update, context):
    user_age = update.message.text
    if 0 < int(user_age) and int(user_age) <= 19:
        user_age = "U20"
        context.user_data["age"] = "U20"
    elif 20 <= int(user_age) and int(user_age) <= 29:
        user_age = "U30"
        context.user_data["age"] = "U30"
    elif 30 <= int(user_age) and int(user_age) <= 39:
        user_age = "U40"
        context.user_data["age"] = "U40"
    elif 40 <= int(user_age) and int(user_age) <= 49:
        user_age = "U50"
        context.user_data["age"] = "U50"
    elif 50 <= int(user_age) and int(user_age) <= 59:
        user_age = "U60"
        context.user_data["age"] = "U60"
    elif int(user_age) >= 60:
        user_age = "O60"
        context.user_data["age"] = "O60"
    # Controllo sulla validità dell'età
    if user_age not in ["U20", "U30", "U40", "U50", "U60", "O60"]:
        await update.message.reply_text(
            "Sorry I did not get your age, can you insert it again? (only the number is good)"
        )
        return AGE
    else:
        if context.user_data["gender"] == "f" or context.user_data["gender"] == "u":
            keyboard = [["Yes", "No"]]
            reply_markup = ReplyKeyboardMarkup(
                keyboard, one_time_keyboard=True, resize_keyboard=True
            )
            await update.message.reply_text(
                "Are you pregnant?", reply_markup=reply_markup
            )
        else:
            await update.message.reply_text("How tall are you? (cm)")
            return CM
        # keyboard = [['Molto importante', 'Importante','Poco importante'], ['Non importante','Assolutamente non importante']]
        # reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        # await update.message.reply_text('Quanto è importante per te avere uno stile di vita salutare?\n(Hai a disposizione dei pulsanti per rispoe alla mia domanda)',reply_markup=reply_markup)
        return PREGNANT


############################################################################################################
# Funzione di gestione della risposta sull'essere incinta
async def pregnant(update: Update, context):
    user_pregnant = update.message.text.lower()
    if context.user_data["gender"] == "f" or context.user_data["gender"] == "u":
        if user_pregnant not in ["yes", "no"]:
            await update.message.reply_text(
                "Sorry i did not get that, can you repeat it?"
            )
            return PREGNANT
        else:
            if user_pregnant == "yes":
                context.user_data["pregnant"] = 1
            if user_pregnant == "no":
                context.user_data["pregnant"] = 0
    await update.message.reply_text("How tall are you? (cm)")
    return CM


############################################################################################################
# Funzione di gestione della risposta sull'altezza
async def height(update: Update, context):
    user_height = update.message.text

    # Controllo sulla validità dell'altezza
    if not user_height.isdigit() or int(user_height) < 90 or int(user_height) > 230:
        await update.message.reply_text("Insert an height between 100 and 230 centimeters")
        return CM
    else:
        context.user_data["height"] = int(user_height)
        await update.message.reply_text("What is your weight? (kg)")
        return KG


############################################################################################################
# Funzione di gestione della risposta sul peso
async def weight(update: Update, context):
    user_weight = update.message.text
    # Controllo sulla validità del peso
    if not user_weight.isdigit() or int(user_weight) < 25 or int(user_weight) > 190:
        await update.message.reply_text(
            "You must insert a valid number in between 25 and 190, round it up to the nearest integer. "
        )
        return KG
    else:
        user_bmi = float(
            int(user_weight)
            * 10000
            / (context.user_data["height"] * context.user_data["height"])
        )
        if user_bmi < 18:
            context.user_data["weight"] = "under"
        elif 18 <= user_bmi < 25:
            context.user_data["weight"] = "normal"
        elif user_bmi >= 25:
            context.user_data["weight"] = "over"
        # print(user_bmi)
        # keyboard = [['Molto facile', 'Facile','Media'],['Difficile','Molto difficile']]
        # reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        # await update.message.reply_text('Come dovrebbe essere la preparazione di un piatto fatto da te?\n(Hai a disposizione dei pulsanti per rispoe alla mia domanda)',reply_markup=reply_markup)
        # return COOK_EXP
        keyboard = [["Lose", "Maintain", "Gain"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            "What are your goals regarding your weight?", reply_markup=reply_markup
        )
        return GOALS


############################################################################################################
# Funzione di gestione della risposta sull'obiettivo
async def goals(update: Update, context):
    user_goals = update.message.text.lower()
    # Controllo sulla validità dell'obiettivo
    if user_goals not in ["lose", "gain", "maintain"]:
        await update.message.reply_text("Please select or type one of the options.")
        return GOALS
    else:
        if user_goals == "lose":
            context.user_data["goals"] = -1
        if user_goals == "gain":
            context.user_data["goals"] = 1
        if user_goals == "maintain":
            context.user_data["goals"] = 0
        # keyboard = [['Bene', 'Neutro'],['Male']]
        # reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        # await update.message.reply_text('Come ti senti attualmente?\n(Hai a disposizione dei pulsanti per rispoe alla mia domanda)',reply_markup=reply_markup)
        # return MOOD
        keyboard = [["A lot (>2)", "Just enough (1-2)", "Not so much (<1)"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            "How much physical activity do you practice weekly?",
            reply_markup=reply_markup,
        )
        return PH_ACTIVITY


############################################################################################################
# Funzione di gestione della risposta sull'attività fisica
async def ph_activity(update: Update, context):
    user_ph_activity = update.message.text.lower()
    # Controllo sulla validità del mood
    if user_ph_activity not in ["a lot (>2)", "just enough (1-2)", "not so much (<1)"]:
        await update.message.reply_text(
            "Devi inserire una tra le opzioni da me suggerite."
        )
        return PH_ACTIVITY
    else:
        if user_ph_activity == "a lot (>2)":
            context.user_data["ph_activity"] = "high"
        if user_ph_activity == "just enough (1-2)":
            context.user_data["ph_activity"] = "normal"
        if user_ph_activity == "not so much (<1)":
            context.user_data["ph_activity"] = "low"

        keyboard = [["Yes", "No"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            "Are you LACTOSE intolerant?", reply_markup=reply_markup
        )
        return LACTOSEFREE


############################################################################################################
# Funzione di gestione della risposta sull'intolleranza al lattosio
async def lactosefree(update: Update, context):
    user_lactosefree = update.message.text.lower()
    if user_lactosefree not in ["yes", "no"]:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return LACTOSEFREE
    else:
        if user_lactosefree == "yes":
            context.user_data["lactosefree"] = 1
        if user_lactosefree == "no":
            context.user_data["lactosefree"] = 0
        keyboard = [["Yes", "No"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            "Are you GLUTEN intolerant?", reply_markup=reply_markup
        )
        return GLUTENFREE


############################################################################################################
# Funzione di gestione della risposta sull'intolleranza al glutine
async def glutenfree(update: Update, context):
    user_glutenfree = update.message.text.lower()
    if user_glutenfree not in ["yes", "no"]:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return GLUTENFREE
    else:
        if user_glutenfree == "yes":
            context.user_data["glutenfree"] = 1
        if user_glutenfree == "no":
            context.user_data["glutenfree"] = 0
        keyboard = [["Yes", "No"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text("Are you DIABETIC?", reply_markup=reply_markup)
        return DIABETES


############################################################################################################
# Funzione di gestione della risposta sull'essere diabetici
async def diabetes(update: Update, context):
    user_diabetes = update.message.text.lower()
    if user_diabetes not in ["yes", "no"]:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return DIABETES
    else:
        if user_diabetes == "yes":
            context.user_data["diabetes"] = 1
        if user_diabetes == "no":
            context.user_data["diabetes"] = 0
        keyboard = [["Yes", "No"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            "Are you VEGETARIAN?", reply_markup=reply_markup
        )
        return VEGETERIAN



############################################################################################################
# Funzione di gestione della risposta sull'essere vegetariani
async def vegetarian(update: Update, context):
    user_vegetarian = update.message.text.lower()
    if user_vegetarian not in ["yes", "no"]:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return VEGETERIAN
    else:
        if user_vegetarian == "yes":
            context.user_data["vegetarian"] = 1
        if user_vegetarian == "no":
            context.user_data["vegetarian"] = 0

        context.user_data["category"] = "first courses"# default values for parameters that are not mandatory
        context.user_data["ht_lifestyle_importance"] = 5 #assume users want to improve their lifestyle
        context.user_data["ht_lifestyle"] = 3
        context.user_data["cook_exp"] = 3
        context.user_data["max_cost_rec"] = 3
        context.user_data["time_cook"] = 0
        context.user_data["mood"] = "neutral"
        context.user_data["sleep"] = "good"
        context.user_data["stress"] = 0
        context.user_data["depress"] = 0
        context.user_data["nickel"] = 0
        context.user_data["light"] = 0

        keyboard = [["Low", "Moderate", "High"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            "How would you define your *knowledge* about the HEALTHINESS of the recipes?", reply_markup=reply_markup, parse_mode='Markdown'
        )
        return HEALTHINESS_LEVEL

async def healthiness_level(update: Update, context):
    user_HT_LEVEL = update.message.text.lower()
    if user_HT_LEVEL not in ["low", "moderate", "high"]:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return HEALTHINESS_LEVEL
    else:
        if user_HT_LEVEL == "low":
            context.user_data["ht_level"] = "low ht knowledge"
        if user_HT_LEVEL == "moderate":
            context.user_data["ht_level"] = "moderate ht knowledge"
        if user_HT_LEVEL == "high":
            context.user_data["ht_level"] = "high ht knowledge"


        keyboard = [["Low", "Moderate", "High"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            "How much *interest* do you have in the HEALTHINESS of the recipes?", reply_markup=reply_markup, parse_mode='Markdown'
        )
        return HEALTHINESS_INTEREST
    
async def healthiness_interest(update: Update, context):
    user_HT_INTEREST = update.message.text.lower()
    if user_HT_INTEREST not in ["low", "moderate", "high"]:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return HEALTHINESS_INTEREST
    else:
        if user_HT_INTEREST == "low":
            context.user_data["ht_interest"] = "low ht interest"
        if user_HT_INTEREST == "moderate":
            context.user_data["ht_interest"] = "moderate ht interest"
        if user_HT_INTEREST == "high":
            context.user_data["ht_interest"] = "high ht interest"


        keyboard = [["Low", "Moderate", "High"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            "How would you define your *knowledge* about the SUSTAINABILITY of the recipes?", reply_markup=reply_markup, parse_mode='Markdown'
        )
        return SUSTAINABILITY_LEVEL

async def sustainability_level(update: Update, context):
    user_sus_level = update.message.text.lower()
    if user_sus_level not in ["low", "moderate", "high"]:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return SUSTAINABILITY_LEVEL
    else:
        if user_sus_level == "low":
            context.user_data["sus_level"] = "low sus knowledge"
        if user_sus_level == "moderate":
            context.user_data["sus_level"] = "moderate sus knowledge"
        if user_sus_level == "high":
            context.user_data["sus_level"] = "high sus knowledge"


        keyboard = [["Low", "Moderate", "High"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            "How much *interest* do you have in the SUSTAINABILITY of the recipes?", reply_markup=reply_markup, parse_mode='Markdown'
        )
        return SUSTAINABILITY_INTEREST
    

async def sustainability_interest(update: Update, context):
    user_sus_interest = update.message.text.lower()
    if user_sus_interest not in ["low", "moderate", "high"]:
        await update.message.reply_text("Sorry I did not get that, can you repeat it?")
        return SUSTAINABILITY_INTEREST
    else:
        if user_sus_interest == "low":
            context.user_data["sus_interest"] = "low sus interest"
        if user_sus_interest == "moderate":
            context.user_data["sus_interest"] = "moderate sus interest"
        if user_sus_interest == "high":
            context.user_data["sus_interest"] = "high sus interest"


        keyboard = [["Low", "Moderate", "High"]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            "Ok, you have just created your profile.\nThank you for your time! \nI've assumed some other values for you (averaging our users), if you want to check your profile out click here: /modify.\n\nOr you can /get_suggestions and I will provide 3 dishes for you:\n- A first-course\n- A second-course\n- A dessert."
        )
        return ConversationHandler.END

# UTILS
def error(update, context):
    logging.error(f"Update {update}   caused error {context.error}")


async def aiuto(update: Update, context):
    await update.message.reply_text(
        "Sono FoodRecSysBot, il bot che ti aiuta a scegliere cosa mangiare!\nPuoi chiedere di suggerirti un piatto che in base alle tue caratteristiche andrà benissimo per te!\nPuoi avere dei consigli su questo piatto, se va bene per te, se è attinente a ciascuna delle informazioni che mi hai dato! Infatti, puoi domandarmi:\nuna spiegazione/descrizione generale del piatto;\nse è adatto ai tuoi obiettivi;\nse è adatto alle tue restrizioni;\nse è attinente al tuo stile di vita;\nse è adatto alla tua età;\nse il suo costo è attinente con la tua disponibilità;\nse il suo tempo di cottura è attinente con il tuo tempo a disposizione;\nquali sono i suoi benefici e quali sono i suoi rischi;\ne perfino se è coerente con la tua esperienza di cucina!\nDopo di che potrai chiedermi di suggerirti anche un altro piatto, e posso confrontarti le caratteristiche dei due piatti rispetto a tutte le caratteristiche di essi.\nInoltre se hai bisogno di cambiare i tuoi dati, premi questo tasto /start per iniziare di nuovo."
    )


async def unknown(update: Update, context):
    await update.message.reply_text(
        "Sorry I did not get that, can you repeat it please?"
    )
    return


async def modify_profile(update: Update, context):
    if "gender" not in context.user_data:
        await update.message.reply_text(
            "You have *not* created your profile yet. \nTry /create first.", parse_mode='Markdown'
        )
        return
    else:
        profile_message = (
            "Ok! This is your current profile.\n"
            "       1 means TRUE.\n"
            "       0 means FALSE.\n"
            "       X/5 it's a scale where 1 is lowest and 5 highest.\n\n"
            f" •  *Category*:  {context.user_data['category']}\n"
            f" •  *Low Nickel*:  {context.user_data['nickel']}\n"
            f" •  *Vegetarian*:  {context.user_data['vegetarian']}\n"
            f" •  *Lactose Free*:  {context.user_data['lactosefree']}\n"
            f" •  *Gluten Free*:  {context.user_data['glutenfree']}\n"
            # f" • Light: {context.user_data['light']}\n"
            f" •  *Diabetic*:  {context.user_data['diabetes']}\n"
            f" •  *Pregnant*:  {context.user_data['pregnant']}\n"
            f" •  *User Skill*:  {context.user_data['cook_exp']}/5\n"
            f" •  *User Lifestyle*:  {context.user_data['ht_lifestyle']}/5\n"
            f" •  *Goal*:  {context.user_data['goals']}\n"
            f" •  *User Budget*:  {context.user_data['max_cost_rec']}/5\n"
            f" •  *User Time*:  {context.user_data['time_cook']}\n"
            f" •  *Weight*: {context.user_data['weight']}\n"
            f" •  *Age*:  {context.user_data['age']}\n"
            f" •  *Sex*:  {context.user_data['gender']}\n"
            f" •  *Activity*:  {context.user_data['ph_activity']}\n"
            f" •  *Stress*:  {context.user_data['stress']}\n"
            f" •  *Sleep*:  {context.user_data['sleep']}\n\n"
            f" •  *Healthiness Knowledge*:  {context.user_data['ht_level']}\n"
            f" •  *Healthiness Interest*:  {context.user_data['ht_interest']}\n"
            f" •  *Sustainability Knowledge*:  {context.user_data['sus_level']}\n"
            f" •  *Sustainability Interest*:  {context.user_data['sus_interest']}\n\n"
            "What would you like to modify?\n"
            "Please type in the attribute you want to modify or '*none*' if you changed your mind:"
            # f"Depression: {context.user_data['depress']}\n"
            # f"Mood: {context.user_data['mood']}"
        )
        await update.message.reply_text(profile_message, parse_mode='Markdown')
    return ATTRIBUTE


async def choose_attribute(update: Update, context):
    attribute = update.message.text.lower()

    attribute_options = {
        "category": ("Your choices are: First courses, Second courses, and Desserts. Please select one:",
                     [["First courses", "Second courses", "Desserts"]]),
        "low nickel": ("Your choices are: I want low nickel suggestions or I do NOT want low nickel suggestions. Please select one:",
                       [["I want low nickel suggestions", "I do NOT want low nickel suggestions"]]),
        "vegetarian": ("Your choices are: I am vegetarian or I am NOT vegetarian. Please select one:",
                        [["I am vegetarian", "I am NOT vegetarian"]]),
        "lactose free": ("Your choices are: I am lactose intolerant or I am NOT lactose intolerant. Please select one:",
                          [["I am lactose intolerant", "I am NOT lactose intolerant"]]),
        "gluten free": ("Your choices are: I am gluten intolerant or I am NOT gluten intolerant. Please select one:",
                          [["I am gluten intolerant", "I am NOT gluten intolerant"]]),
        "diabetic": ("Your choices are: I am diabetic or I am NOT diabetic. Please select one:",
                      [["I am diabetic", "I am NOT diabetic"]]),
        "pregnant": ("Your choices are: I am pregnant or I am NOT pregnant. Please select one:",
                       [["I am pregnant", "I am NOT pregnant"]]),
        "user skill": ("Your choices are: Very low-skilled, Low-skilled, Medium-skilled, High-skilled, Very High-skilled. Please select one:",
                         [["Very low-skilled", "Low-skilled", "Medium-skilled", "High-skilled", "Very High-skilled"]]),
        "user lifestyle": ("Your choices are: Very Unhealty-lifestyle, Unhealty-lifestyle, Normal-lifestyle, Healty-lifestyle, Very Healty-lifestyle. Please select one:",
                             [["Very Unhealty-lifestyle", "Unhealty-lifestyle", "Normal-lifestyle", "Healty-lifestyle", "Very Healty-lifestyle"]]),
        "goal": ("Your choices are: Lose, Maintain, and Gain. Please select one:",
                    [["Lose", "Maintain", "Gain"]]),
        "user budget": ("Your choices are: Very low-cost, Low-cost, Medium-cost, High-cost, Very High-cost. Please select one:",
                            [["Very low-cost", "Low-cost", "Medium-cost", "High-cost", "Very High-cost"]]),
        "user time": ("Your choices are: -30 minutes, 30-60 minutes, 60-90 minutes, 90-120 minutes, 120+ minutes. Please select one:",
                          [["-30", "30-60", "60-90", "90-120", "120+"]]),
        "weight": ("Your choices are: Under-weight, Normal-weight, and Over-weight. Please select one:",
                      [["Under", "Normal", "Over"]]),
        "age": ("Your choices are: Under20, Under30, Under40, Under50, Under60, Over60. Please select one:",
                   [["U20", "U30", "U40", "U50", "U60", "O60"]]),
        "sex": ("Your choices are: Male, Female, and Unspecified. Please select one:",
                  [["Male", "Female", "Unspecified"]]),
        "activity": ("Your choices are: Low-activity, Normal-activity, and High-activity. Please select one:",
                          [["Low-activity", "Normal-activity", "High-activity"]]),
        "stress": ("Your choices are: I am stressed or I am NOT stressed. Please select one:",
                      [["I am stressed", "I am NOT stressed"]]),
        "sleep": ("Your choices are: 8+ daily hours of sleep (good) or 8- daily hours of sleep (bad). Please select one:",
                    [["8+", "8-"]]),
        "healthiness knowledge": ("Your choices are: Low Knowledge, Moderate Knowledge or High Knowledge. Please select one:",
                    [["Low Ht Knowledge", "Moderate Ht Knowledge", "High Ht Knowledge"]]),
        "healthiness interest": ("Your choices are: Low Interest, Moderate Interest or High Interest. Please select one:",
                    [["Low Ht Interest", "Moderate Ht Interest", "High Ht Interest"]]),
        "sustainability knowledge": ("Your choices are: Low, Moderate or High. Please select one:",
                    [["Low Sus Knowledge", "Moderate Sus Knowledge", "High Sus Knowledge"]]),
        "sustainability interest": ("Your choices are: Low Interest, Moderate Interest or High Interest. Please select one:",
                    [["Low Sus Interest", "Moderate Sus Interest", "High Sus Interest"]]),
    }

    if attribute in attribute_options:
        message, options = attribute_options[attribute]
        reply_markup = ReplyKeyboardMarkup(options, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(message, reply_markup=reply_markup)
        return TO_CHOICES
    elif attribute == "none":
        await update.message.reply_text("You changed your mind, that's ok. Try to /get_suggestions")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Sorry, I did not get that. Can you repeat it please?")


async def change_attribute_value(update: Update, context):
    value = update.message.text.lower()

    if value == "low ht knowledge":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Healthiness Knowledge'\nfrom:  {context.user_data['ht_level']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ht_level"] = value
        return ConversationHandler.END

    if value == "moderate ht knowledge":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Healthiness Knowledge'\nfrom:  {context.user_data['ht_level']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ht_level"] = value
        return ConversationHandler.END

    if value == "high ht knowledge":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Healthiness Knowledge'\nfrom:  {context.user_data['ht_level']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ht_level"] = value
        return ConversationHandler.END
    
    if value == "low ht interest":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Healthiness Interest'\nfrom:  {context.user_data['ht_level']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ht_interest"] = value
        return ConversationHandler.END
    
    if value == "moderate ht interest":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Healthiness Interest'\nfrom:  {context.user_data['ht_interest']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ht_interest"] = value
        return ConversationHandler.END
    
    if value == "high ht interest":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Healthiness Interest'\nfrom:  {context.user_data['ht_interest']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ht_interest"] = value
        return ConversationHandler.END
    
    if value == "low sus knowledge":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Category'\nfrom:  {context.user_data['sus_level']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["sus_level"] = value
        return ConversationHandler.END
    
    if value == "moderate sus knowledge":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Category'\nfrom:  {context.user_data['sus_level']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["sus_level"] = value
        return ConversationHandler.END
    
    if value == "high sus knowledge":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Category'\nfrom:  {context.user_data['sus_level']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["sus_level"] = value
        return ConversationHandler.END
    
    if value == "low sus interest":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Category'\nfrom:  {context.user_data['sus_interest']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["sus_interest"] = value
        return ConversationHandler.END
    
    if value == "moderate sus interest":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Category'\nfrom:  {context.user_data['sus_interest']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["sus_interest"] = value
        return ConversationHandler.END
    
    if value == "high sus interest":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Category'\nfrom:  {context.user_data['sus_interest']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["sus_interest"] = value
        return ConversationHandler.END
    












    if value == "first courses":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Category'\nfrom:  {context.user_data['category']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["category"] = value
        return ConversationHandler.END

    elif value == "second courses":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Category'\nfrom:  {context.user_data['category']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["category"] = value
        return ConversationHandler.END

    elif value == "desserts":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successefully changed attribute 'Category'\nfrom:  {context.user_data['category']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["category"] = value
        return ConversationHandler.END

    elif value == "i do not want low nickel suggestions":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Low Nickel'\nfrom:  {context.user_data['nickel']} -> 0.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["nickel"] = 0
        return ConversationHandler.END

    elif value == "i am vegetarian":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Vegetarian'\nfrom:  {context.user_data['vegetarian']} -> 1.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["vegetarian"] = 1
        return ConversationHandler.END

    elif value == "i am not vegetarian":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Vegetarian'\nfrom:  {context.user_data['vegetarian']} -> 0.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["vegetarian"] = 0
        return ConversationHandler.END

    elif value == "i am lactose intolerant":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Lactose-Free'\nfrom:  {context.user_data['lactosefree']} -> 1.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["lactosefree"] = 1
        return ConversationHandler.END

    elif value == "i am not lactose intolerant":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Lactose-Free'\nfrom:  {context.user_data['lactosefree']} -> 0.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["lactosefree"] = 0
        return ConversationHandler.END

    elif value == "i am gluten intolerant":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Gluten-Free'\nfrom:  {context.user_data['glutenfree']} -> 1.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["glutenfree"] = 1
        return ConversationHandler.END

    elif value == "i am not gluten intolerant":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Gluten-Free'\nfrom:  {context.user_data['glutenfree']} -> 0.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["glutenfree"] = 0
        return ConversationHandler.END

    elif value == "i am diabetic":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Diabetes'\nfrom:  {context.user_data['diabetes']} -> 1.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["diabetes"] = 1
        return ConversationHandler.END

    elif value == "i am not diabetic":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Diabetes'\nfrom:  {context.user_data['diabetes']} -> 0.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["diabetes"] = 0
        return ConversationHandler.END

    elif value == "i am pregnant":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Pregnant'\nfrom:  {context.user_data['pregnant']} -> 1.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["pregnant"] = 1
        return ConversationHandler.END

    elif value == "i am not pregnant":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Pregnant'\nfrom:  {context.user_data['pregnant']} -> 0.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["pregnant"] = 0
        return ConversationHandler.END

    elif value == "very low-skilled":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Skill'\nfrom:  {context.user_data['cook_exp']} -> 1.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["cook_exp"] = 1
        return ConversationHandler.END

    elif value == "low-skilled":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Skill'\nfrom:  {context.user_data['cook_exp']} -> 2.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["cook_exp"] = 2
        return ConversationHandler.END

    elif value == "medium-skilled":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Skill'\nfrom:  {context.user_data['cook_exp']} -> 3.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["cook_exp"] = 3
        return ConversationHandler.END

    elif value == "high-skilled":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Skill'\nfrom:  {context.user_data['cook_exp']} -> 4.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["cook_exp"] = 4
        return ConversationHandler.END

    elif value == "very high-skilled":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Skill'\nfrom:  {context.user_data['cook_exp']} -> 5.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["cook_exp"] = 5
        return ConversationHandler.END

    elif value == "very unhealty-lifestyle":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Lifestyle'\nfrom:  {context.user_data['ht_lifestyle']} -> 1.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ht_lifestyle"] = 1
        return ConversationHandler.END

    elif value == "unhealty-lifestyle":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Lifestyle'\nfrom:  {context.user_data['ht_lifestyle']} -> 2.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ht_lifestyle"] = 2
        return ConversationHandler.END

    elif value == "normal-lifestyle":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Lifestyle'\nfrom:  {context.user_data['ht_lifestyle']} -> 3.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ht_lifestyle"] = 3
        return ConversationHandler.END

    elif value == "healty-lifestyle":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Lifestyle'\nfrom:  {context.user_data['ht_lifestyle']} -> 4.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ht_lifestyle"] = 4
        return ConversationHandler.END

    elif value == "very healty-lifestyle":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Lifestyle'\nfrom:  {context.user_data['ht_lifestyle']} -> 5.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ht_lifestyle"] = 5
        return ConversationHandler.END

    elif value == "lose":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Goal'\nfrom:  {context.user_data['goal']} -> -1.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["goal"] = -1
        return ConversationHandler.END

    elif value == "maintain":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Goal'\nfrom:  {context.user_data['goal']} -> 0.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["goal"] = 0
        return ConversationHandler.END

    elif value == "gain":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Goal'\nfrom:  {context.user_data['goals']} -> 1.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["goal"] = 1
        return ConversationHandler.END

    elif value == "very low-cost":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Budget'\nfrom:  {context.user_data['max_cost_rec']} -> 1.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["max_cost_rec"] = 1
        return ConversationHandler.END

    elif value == "low-cost":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Budget'\nfrom:  {context.user_data['max_cost_rec']} -> 2.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["max_cost_rec"] = 2
        return ConversationHandler.END

    elif value == "medium-cost":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Budget'\nfrom:  {context.user_data['max_cost_rec']} -> 3.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["max_cost_rec"] = 3
        return ConversationHandler.END

    elif value == "high-cost":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Budget'\nfrom:  {context.user_data['max_cost_rec']} -> 4.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["max_cost_rec"] = 4
        return ConversationHandler.END

    elif value == "very high-cost":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Budget'\nfrom:  {context.user_data['max_cost_rec']} -> 5.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["max_cost_rec"] = 5
        return ConversationHandler.END

    elif value == "-30":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Time'\nfrom:  {context.user_data['time_cook']} -> 20.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["time_cook"] = 20
        return ConversationHandler.END

    elif value == "30-60":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Time'\nfrom:  {context.time_cook['usertime']} -> 30.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["time_cook"] = 30
        return ConversationHandler.END

    elif value == "60-90":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Time'\nfrom:  {context.user_data['time_cook']} -> 75.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["time_cook"] = 75
        return ConversationHandler.END

    elif value == "90-120":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Time'\nfrom:  {context.user_data['time_cook']} -> 105.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["time_cook"] = 90
        return ConversationHandler.END

    elif value == "120+":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'User Time'\nfrom:  {context.user_data['time_cook']} -> 135.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["time_cook"] = 120
        return ConversationHandler.END

    elif value == "under":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Weight'\nfrom:  {context.user_data['weight']} -> Under-weight.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["weight"] = "under"
        return ConversationHandler.END

    elif value == "normal":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Weight'\nfrom:  {context.user_data['weight']} -> Normal-weight.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["weight"] = "normal"
        return ConversationHandler.END

    elif value == "over":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Weight'\nfrom:  {context.user_data['weight']} -> Over-weight.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["weight"] = "over"
        return ConversationHandler.END

    elif value == "u20":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Age'\nfrom:  {context.user_data['age']} -> U20.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["age"] = "U20"
        return ConversationHandler.END

    elif value == "u30":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Age'\nfrom:  {context.user_data['age']} -> U30.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["age"] = "U30"
        return ConversationHandler.END

    elif value == "u40":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Age'\nfrom:  {context.user_data['age']} -> U40.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["age"] = "U40"
        return ConversationHandler.END

    elif value == "u50":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Age'\nfrom:  {context.user_data['age']} -> U50.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["age"] = "U50"
        return ConversationHandler.END

    elif value == "u60":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Age'\nfrom:  {context.user_data['age']} -> U60.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["age"] = "U60"
        return ConversationHandler.END

    elif value == "o60":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Age'\nfrom:  {context.user_data['age']} -> O60.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["age"] = "O60"
        return ConversationHandler.END

    elif value == "male":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Gender'\nfrom:  {context.user_data['gender']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["gender"] = "m"
        return ConversationHandler.END

    elif value == "female":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Gender'\nfrom:  {context.user_data['gender']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["gender"] = "f"
        return ConversationHandler.END

    elif value == "unspecified":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Gender'\nfrom:  {context.user_data['gender']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["gender"] = "u"
        return ConversationHandler.END

    elif value == "low-activity":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Activity'\nfrom:  {context.user_data['ph_activity']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ph_activity"] = "low"
        return ConversationHandler.END

    elif value == "normal-activity":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Activity'\nfrom:  {context.user_data['ph_activity']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ph_activity"] = "normal"
        return ConversationHandler.END

    elif value == "high-activity":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Activity'\nfrom:  {context.user_data['ph_activity']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["ph_activity"] = "high"
        return ConversationHandler.END

    elif value == "i am stressed":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Stress'\nfrom:  {context.user_data['stress']} -> 1.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["stress"] = 1
        return ConversationHandler.END

    elif value == "i am not stressed":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Stress'\nfrom:  {context.user_data['stress']} -> 0.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["stress"] = 0
        return ConversationHandler.END

    elif value == "8+ daily hours of sleep":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Sleep'\nfrom:  {context.user_data['sleep']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["sleep"] = "good"
        return ConversationHandler.END

    elif value == "8- daily hours of sleep":
        print(f"debug - value selected -> ({value})")
        await update.message.reply_text(
            f"You successfully changed attribute 'Sleep'\nfrom:  {context.user_data['sleep']} -> {value}.\n\nYou can now /modify something else, or /get_suggestions"
        )
        context.user_data["sleep"] = "bad"
        return ConversationHandler.END

    else:
        await update.message.reply_text(
            "Sorry, I did not get that. Can you repeat it, please?"
        )


# Thesis functions
async def healthiness_initialiation(update, context):
    if "gender" not in context.user_data:
        await update.message.reply_text(
            "You have *not* created your profile yet. \nTry /create first.",
            parse_mode="Markdown",
        )
        return
    else:
        await Recommendation.suggerimento(update, context)
        keyboard = [
            ["Unhealthy", "Somewhat Unhealthy"],
            ["Moderately Healthy"],
            ["Healthy", "Very Healthy"],
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(
            "How healthy do you think this recipe is?", reply_markup=reply_markup
        )
        return PRE_FIRST_COURSE_HEALTINESS


async def first_suggestion_healthiness_explanation(update, context):
    first_suggestion_unconditioned = update.message.text.lower()
    name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(
            name
            + ","
            + str(user_id)
            + ","
            + str(context.user_data["nickel"])
            + ","
            + str(context.user_data["vegetarian"])
            + ","
            + str(context.user_data["lactosefree"])
            + ","
            + str(context.user_data["glutenfree"])
            + ","
            + str(context.user_data["ht_lifestyle"])
            + ","
            + str(context.user_data["diabetes"])
            + ","
            + str(context.user_data["pregnant"])
            + ","
            + str(context.user_data["cook_exp"])
            + ","
            + str(context.user_data["goals"])
            + ","
            + str(context.user_data["max_cost_rec"])
            + ","
            + str(context.user_data["time_cook"])
            + ","
            + str(context.user_data["weight"])
            + ","
            + str(context.user_data["age"])
            + ","
            + str(context.user_data["gender"])
            + ","
            + str(context.user_data["ph_activity"])
            + ","
            + str(context.user_data["stress"])
            + ","
            + str(context.user_data["sleep"])
            + ","
            + str(context.user_data["ht_level"])
            + ","
            + str(context.user_data["ht_interest"])
            + ","
            + str(context.user_data["sus_level"])
            + ","
            + str(context.user_data["sus_interest"])
            + ","
            + Recommendation.img_url
            + ","
            + first_suggestion_unconditioned
            + ","
        )
    await update.message.reply_text(
        "Great, I will now prompt you with one of my explanations:"
    )

    random_number = random.randint(1, 4)
    if random_number == 1:
        await Spiegazione.spiegazione_obiettivo(update, context)
        expl_type = "goals"
    elif random_number == 2:
        await Spiegazione.spiegazione_benefici_salute(update, context)
        expl_type = "health-benefits"
    elif random_number == 3:
        await Spiegazione.spiegazione_rischi_salute(update, context)
        expl_type = "health-risks"
    elif random_number == 4:
        await Spiegazione.spiegazione_macros(update, context)
        expl_type = "macros"

    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(expl_type + ",")

    keyboard = [
        ["Unhealthy", "Somewhat Unhealthy"],
        ["Moderately Healthy"],
        ["Healthy", "Very Healthy"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        "How healthy do you think this recipe is now?", reply_markup=reply_markup
    )
    return POST_FIRST_COURSE_HEALTINESS


async def second_suggestion(update, context):
    first_suggestion_conditioned = update.message.text.lower()
    await update.message.reply_text("Great, now a second course:")
    context.user_data["category"] = "second courses"
    await Recommendation.suggerimento(update, context)

    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(first_suggestion_conditioned + "," + Recommendation.img_url + ",")

    keyboard = [
        ["Unhealthy", "Somewhat Unhealthy"],
        ["Moderately Healthy"],
        ["Healthy", "Very Healthy"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        "How healthy do you think this recipe is?", reply_markup=reply_markup
    )
    return PRE_SECOND_COURSE_HEALTINESS


async def second_suggestion_healthiness_explanation(update, context):
    second_suggestion_unconditioned = update.message.text.lower()
    random_number = random.randint(1, 4)
    if random_number == 1:
        await Spiegazione.spiegazione_obiettivo(update, context)
        expl_type = "goals"
    elif random_number == 2:
        await Spiegazione.spiegazione_benefici_salute(update, context)
        expl_type = "health-benefits"
    elif random_number == 3:
        await Spiegazione.spiegazione_rischi_salute(update, context)
        expl_type = "health-risks"
    elif random_number == 4:
        await Spiegazione.spiegazione_macros(update, context)
        expl_type = "macros"

    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(second_suggestion_unconditioned + "," + expl_type + ",")
    await update.message.reply_text(
        "Wonderful, I'll now provide you with one of my explanations:"
    )

    keyboard = [
        ["Unhealthy", "Somewhat Unhealthy"],
        ["Moderately Healthy"],
        ["Healthy", "Very Healthy"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        "How healthy do you think this recipe is now?", reply_markup=reply_markup
    )
    return POST_SECOND_COURSE_HEALTINESS


async def third_suggestion(update, context):
    second_suggestion_conditioned = update.message.text.lower()
    await update.message.reply_text("Great, now a dessert:")
    context.user_data["category"] = "desserts"
    await Recommendation.suggerimento(update, context)

    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(second_suggestion_conditioned + "," + Recommendation.img_url + ",")

    keyboard = [
        ["Unhealthy", "Somewhat Unhealthy"],
        ["Moderately Healthy"],
        ["Healthy", "Very Healthy"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        "How healthy do you think this recipe is?", reply_markup=reply_markup
    )
    return PRE_DESSERT_HEALTINESS


async def third_suggestion_healthiness_explanation(update, context):
    third_suggestion_unconditioned = update.message.text.lower()
    await update.message.reply_text(
        "Excellent, I'll proceed to present you with one of my explanations:"
    )

    random_number = random.randint(1, 4)
    if random_number == 1:
        await Spiegazione.spiegazione_obiettivo(update, context)
        expl_type = "goals"
    elif random_number == 2:
        await Spiegazione.spiegazione_benefici_salute(update, context)
        expl_type = "health-benefits"
    elif random_number == 3:
        await Spiegazione.spiegazione_rischi_salute(update, context)
        expl_type = "health-risks"
    elif random_number == 4:
        await Spiegazione.spiegazione_macros(update, context)
        expl_type = "macros"

    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(third_suggestion_unconditioned + "," + expl_type + ",")

    keyboard = [
        ["Unhealthy", "Somewhat Unhealthy"],
        ["Moderately Healthy"],
        ["Healthy", "Very Healthy"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        "How healthy do you think this recipe is now?", reply_markup=reply_markup
    )
    return POST_DESSERT_HEALTINESS


async def fourth_suggestion(update, context):
    third_suggestion_conditioned = update.message.text.lower()
    await update.message.reply_text(
        "Good job! Now let's talk about the sustainability:"
    )
    context.user_data["category"] = "first courses"
    await Recommendation_due.altro_suggerimento2(update, context)

    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(third_suggestion_conditioned + "," + Recommendation_due.img_url + ",")

    keyboard = [
        ["Unsustainable", "Somewhat Unsustainable"],
        ["Moderately Sustainable"],
        ["Sustainable", "Very Sustainable"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        "How sustainable do you think this recipe is?", reply_markup=reply_markup
    )
    return PRE_FIRST_COURSE_SUSTAINABILITY


async def fourth_suggestion_sustainability_explanation(update, context):
    fourth_suggestion_unconditioned = update.message.text.lower()
    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(fourth_suggestion_unconditioned + ",")
    await update.message.reply_text(
        "Fantastic, I'll now offer you one of my explanations:"
    )
    random_number = random.randint(1, 2)
    if random_number == 1:
        await Spiegazione.spiegazione_sustainability_alternativa(update, context)
        expl_type = "ingredients"
    elif random_number == 2:
        await Spiegazione.spiegazione_sustainability(update, context)
        expl_type = "description"

    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(fourth_suggestion_unconditioned + "," + expl_type + ",")

    keyboard = [
        ["Unsustainable", "Somewhat Unsustainable"],
        ["Moderately Sustainable"],
        ["Sustainable", "Very Sustainable"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        "How sustainable do you think this recipe is now?", reply_markup=reply_markup
    )
    return POST_FIRST_COURSE_SUSTAINABILITY


async def fifth_suggestion(update, context):
    fourth_suggestion_conditioned = update.message.text.lower()
    await update.message.reply_text("Great, now a second course:")
    context.user_data["category"] = "second courses"
    await Recommendation_due.altro_suggerimento2(update, context)
    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(
            fourth_suggestion_conditioned + "," + Recommendation_due.img_url + ","
        )
    keyboard = [
        ["Unsustainable", "Somewhat Unsustainable"],
        ["Moderately Sustainable"],
        ["Sustainable", "Very Sustainable"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        "How sustainable do you think this recipe is?", reply_markup=reply_markup
    )
    return PRE_SECOND_COURSE_SUSTAINABILITY


async def fifth_suggestion_sustainability_explanation(update, context):
    fifth_suggestion_unconditioned = update.message.text.lower()
    await update.message.reply_text(
        "Terrific, I'll now deliver one of my explanations to you:"
    )
    random_number = random.randint(1, 2)
    if random_number == 1:
        await Spiegazione.spiegazione_sustainability(update, context)
        expl_type = "sustainability"
    elif random_number == 2:
        await Spiegazione.spiegazione_sustainability_alternativa(update, context)
        expl_type = "ingredients"

    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(fifth_suggestion_unconditioned + "," + expl_type + ",")
    keyboard = [
        ["Unsustainable", "Somewhat Unsustainable"],
        ["Moderately Sustainable"],
        ["Sustainable", "Very Sustainable"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        "How sustainable do you think this recipe is now?", reply_markup=reply_markup
    )
    return POST_SECOND_COURSE_SUSTAINABILITY


async def sixth_suggestion(update, context):
    fifth_suggestion_conditioned = update.message.text.lower()
    await update.message.reply_text("Great, now a dessert:")
    context.user_data["category"] = "desserts"
    await Recommendation_due.altro_suggerimento2(update, context)

    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(
            fifth_suggestion_conditioned + "," + Recommendation_due.img_url + ","
        )

    keyboard = [
        ["Unsustainable", "Somewhat Unsustainable"],
        ["Moderately Sustainable"],
        ["Sustainable", "Very Sustainable"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        "How sustainable do you think this recipe is?", reply_markup=reply_markup
    )
    return PRE_DESSERT_SUSTAINABILITY


async def sixth_suggestion_sustainability_explanation(update, context):
    sixth_suggestion_unconditioned = update.message.text.lower()

    await update.message.reply_text(
        "Perfect, I'll now provide you with one of my explanations:"
    )
    random_number = random.randint(1, 2)
    if random_number == 1:
        await Spiegazione.spiegazione_sustainability(update, context)
        expl_type = "sustainability"
    elif random_number == 2:
        await Spiegazione.spiegazione_sustainability_alternativa(update, context)
        expl_type = "ingredients"

    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(sixth_suggestion_unconditioned + "," + expl_type + ",")
    keyboard = [
        ["Unsustainable", "Somewhat Unsustainable"],
        ["Moderately Sustainable"],
        ["Sustainable", "Very Sustainable"],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        "How sustainable do you think this recipe is now?", reply_markup=reply_markup
    )
    return POST_DESSERT_SUSTAINABILITY


async def end_of_experiment(update, context):
    user_id = str(update.message.from_user.id)
    sixth_suggestion_conditioned = update.message.text.lower()
    with open("replies.csv", "a", encoding="utf-8") as file:
        file.write(sixth_suggestion_conditioned + "\n")

    if hasattr(SpecificRec, 'img_url'):
        del SpecificRec.img_url 
    if hasattr(Recommendation_tre, 'img_url'):
        del Recommendation_tre.img_url 
    if hasattr(Recommendation_due, 'img_url'):
        del Recommendation_due.img_url 
    if hasattr(Recommendation, 'img_url'):
        del Recommendation.img_url 
    if context.user_data["category"]:
        del context.user_data["category"] 
    if context.user_data["nickel"]:
        del context.user_data["nickel"] 
    if context.user_data["vegetarian"]:
        del context.user_data["vegetarian"] 
    if context.user_data["lactosefree"]:
        del context.user_data["lactosefree"] 
    if context.user_data["glutenfree"]:
        del context.user_data["glutenfree"] 
    if context.user_data["diabetes"]:
        del context.user_data["diabetes"] 
    if context.user_data["pregnant"]:
        del context.user_data["pregnant"] 
    if context.user_data["cook_exp"]:
        del context.user_data["cook_exp"] 
    if context.user_data["ht_lifestyle"]:
        del context.user_data["ht_lifestyle"] 
    if context.user_data["goals"]:
        del context.user_data["goals"] 
    if context.user_data["max_cost_rec"]:
        del context.user_data["max_cost_rec"] 
    if context.user_data["time_cook"]:
        del context.user_data["time_cook"] 
    if context.user_data["weight"]:
        del context.user_data["weight"] 
    if context.user_data["age"]:
       del context.user_data["age"] 
    if context.user_data["gender"]:
        del context.user_data["gender"] 
    if context.user_data["ph_activity"]:
        del context.user_data["ph_activity"] 
    if context.user_data["stress"]:
        del context.user_data["stress"] 
    if context.user_data["sleep"]:
        del context.user_data["sleep"]

    await update.message.reply_text(f"Session completed.\n\nThank you so much for your time, we are now done.\nPlease click your ID to copy it: `{user_id}` \nyou will need this for the final questionnaire.\n\nTo proceed please follow this link: https://forms.gle/z9EzKyioQ5xvDdtR8", parse_mode='Markdown')
    return ConversationHandler.END


#########################################################################################################################à
# Funzione per inviare il messaggio a Dialogflow e restituire la risposta
async def dialogflow_mode(update: Update, context):
    # Id del progetto Dialogflow
    DIALOGFLOW_PROJECT_ID = "thesis-9rwt"
    # Credenziali del progetto Dialogflow
    DIALOGFLOW_CREDENTIALS = "thesis-9rwt-c09b3317288e.json"
    # Recupera l'ID dell'utente e imposta la lingua del messaggio
    session_id = update.effective_user.id
    language_code = "it"
    # Crea il client di sessione di Dialogflow
    session_client = dialogflow.SessionsClient.from_service_account_file(
        DIALOGFLOW_CREDENTIALS
    )
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
    confidence = response.query_result.intent_detection_confidence
    
    if intent == "Suggestion":
        await Recommendation.suggerimento(update, context)
    if intent == "Change suggestion 1":
        await Recommendation_due.altro_suggerimento2(update, context)
    if intent == "Change suggestion 2":
        await Recommendation_tre.altro_suggerimento3(update, context)
    if intent == "Explanation smart":
       await Spiegazione.smart_explanation(update, context)
    if intent == "Explanation check":
       await Spiegazione.controllo_piatto(update, context)
    if intent == "Explanation popularity":
       await Spiegazione.spiegazione_popolarita(update, context)
    if intent == "Explanation meal":
        await Spiegazione.spiegazione_piatto(update, context)
    if intent == "Explanation skill":
        await Spiegazione.spiegazione_skill_cucina(update, context)
    if intent == "Explanation goals":
        await Spiegazione.spiegazione_obiettivo(update, context)
    if intent == "Explanation health-benefit":
        await Spiegazione.spiegazione_benefici_salute(update, context)
    if intent == "Explanation health-risk":
        await Spiegazione.spiegazione_rischi_salute(update, context)
    if intent == "Explanation cost":
        await Spiegazione.spiegazione_costo(update, context)
    if intent == "Explanation age":
        await Spiegazione.spiegazione_eta(update, context)
    if intent == "Explanation restriction":
        await Spiegazione.spiegazione_restrizioni(update, context)
    if intent == "Explanation lifestyle":
        await Spiegazione.spiegazione_lifestyle(update, context)
    if intent == "Explanation time":
        await Spiegazione.spiegazione_tempo(update, context)
    if intent == "Explanation macros":
        await Spiegazione.spiegazione_macros(update, context)
    if intent == "Explanation sustainability":
        await Spiegazione.spiegazione_sustainability(update, context)
    if intent == "Explanation seasonability":
        await Spiegazione.spiegazione_seasonability(update, context)


    if intent == "Comparison smart":
       await Spiegazione.smartExplanation_due_piatti(update, context)
    if intent == "Comparison two meals":
       await Spiegazione.controllo_piatto_due_piatti(update, context)
    if intent == "Comparison popularity":
        await Spiegazione.spiegazione_popolarita_due_piatti(update, context)
    if intent == "Comparison meal checks":
        await Spiegazione.spiegazione_piatto_due_piatti(update, context)
    if intent == "Comparison skill":
        await Spiegazione.spiegazione_skill_cucina_due_piatti(update, context)
    if intent == "Comparison goal":
        await Spiegazione.spiegazione_obiettivi_due_piatti(update, context)
    if intent == "Comparison health-benefit":
        await Spiegazione.spiegazione_benefici_salute_due_piatti(update, context)
    if intent == "Comparison health-risk":
        await Spiegazione.spiegazione_rischi_salute_due_piatti(update, context)
    if intent == "Comparison cost":
        await Spiegazione.spiegazione_costo_due_piatti(update, context)
    if intent == "Comparison age":
        await Spiegazione.spiegazione_eta_due_piatti(update, context)
    if intent == "Comparison restriction":
        await Spiegazione.spiegazione_restrizioni_due_piatti(update, context)
    if intent == "Comparison lifestyle":
        await Spiegazione.spiegazione_lifestyle_due_piatti(update, context)
    if intent == "Comparison time":
        await Spiegazione.spiegazione_tempo_due_piatti(update, context)
    if intent == "Comparison macros":
        await Spiegazione.spiegazione_macros_due_piatti(update, context)
    if intent == "Comparison sustainability":
        await Spiegazione.spiegazione_sustainability_due_piatti(update, context)
    if intent == "Comparison seasonability":
        await Spiegazione.spiegazione_seasonability_due_piatti(update, context)

    if intent == "Specific suggestion":
        print("here")
        IngredientName=response.query_result.parameters.get("IngredientName")
        print("Specific suggestion variable:", IngredientName)
        await SpecificRec.specific_sugg(update, context, IngredientName)


    confidence = response.query_result.intent_detection_confidence
    print("Intent:", intent)
    print("Confidence:", confidence)
    if response.query_result.fulfillment_text:
        return await update.message.reply_text(response.query_result.fulfillment_text)
    else:
        return

async def clear_session(update: Update, context):
    if hasattr(SpecificRec, 'img_url'):
        del SpecificRec.img_url 
    if hasattr(Recommendation_tre, 'img_url'):
        del Recommendation_tre.img_url 
    if hasattr(Recommendation_due, 'img_url'):
        del Recommendation_due.img_url 
    if hasattr(Recommendation, 'img_url'):
        del Recommendation.img_url 
    if context.user_data["category"]:
        del context.user_data["category"] 
    if context.user_data["nickel"]:
        del context.user_data["nickel"] 
    if context.user_data["vegetarian"]:
        del context.user_data["vegetarian"] 
    if context.user_data["lactosefree"]:
        del context.user_data["lactosefree"] 
    if context.user_data["glutenfree"]:
        del context.user_data["glutenfree"] 
    if context.user_data["diabetes"]:
        del context.user_data["diabetes"] 
    if context.user_data["pregnant"]:
        del context.user_data["pregnant"] 
    if context.user_data["cook_exp"]:
        del context.user_data["cook_exp"] 
    if context.user_data["ht_lifestyle"]:
        del context.user_data["ht_lifestyle"] 
    if context.user_data["goals"]:
        del context.user_data["goals"] 
    if context.user_data["max_cost_rec"]:
        del context.user_data["max_cost_rec"] 
    if context.user_data["time_cook"]:
        del context.user_data["time_cook"] 
    if context.user_data["weight"]:
        del context.user_data["weight"] 
    if context.user_data["age"]:
       del context.user_data["age"] 
    if context.user_data["gender"]:
        del context.user_data["gender"] 
    if context.user_data["ph_activity"]:
        del context.user_data["ph_activity"] 
    if context.user_data["stress"]:
        del context.user_data["stress"] 
    if context.user_data["sleep"]:
        del context.user_data["sleep"]

    await update.message.reply_text("Session cleared!", parse_mode='Markdown') 
    return 

async def main():
    nest_asyncio.apply()
    # Inizializzazione del logger
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    # Definizione dei comandi e dei gestori di messaggi
    application = Application.builder().token(keys.API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("create", start)],
        states={
            GENDER: [MessageHandler(filters.TEXT, gender)],
            AGE: [MessageHandler(filters.TEXT, age)],
            PREGNANT: [MessageHandler(filters.TEXT, pregnant)],
            CM: [MessageHandler(filters.TEXT, height)],
            KG: [MessageHandler(filters.TEXT, weight)],
            GOALS: [MessageHandler(filters.TEXT, goals)],
            PH_ACTIVITY: [MessageHandler(filters.TEXT, ph_activity)],
            LACTOSEFREE: [MessageHandler(filters.TEXT, lactosefree)],
            GLUTENFREE: [MessageHandler(filters.TEXT, glutenfree)],
            DIABETES: [MessageHandler(filters.TEXT, diabetes)],
            VEGETERIAN: [MessageHandler(filters.TEXT, vegetarian)],
            HEALTHINESS_LEVEL: [MessageHandler(filters.TEXT, healthiness_level)],
            HEALTHINESS_INTEREST: [MessageHandler(filters.TEXT, healthiness_interest)],
            SUSTAINABILITY_LEVEL: [MessageHandler(filters.TEXT, sustainability_level)],
            SUSTAINABILITY_INTEREST: [MessageHandler(filters.TEXT, sustainability_interest)],
        },
        fallbacks=[MessageHandler(filters.TEXT, unknown)],
    )


    ##################################################################
    path_handler = ConversationHandler(
        entry_points=[CommandHandler("get_suggestions", healthiness_initialiation)],
        states={
            PRE_FIRST_COURSE_HEALTINESS: [MessageHandler(filters.TEXT, first_suggestion_healthiness_explanation)],
            POST_FIRST_COURSE_HEALTINESS: [MessageHandler(filters.TEXT, second_suggestion)],
            PRE_SECOND_COURSE_HEALTINESS: [MessageHandler(filters.TEXT, second_suggestion_healthiness_explanation)],
            POST_SECOND_COURSE_HEALTINESS: [MessageHandler(filters.TEXT, third_suggestion)],
            PRE_DESSERT_HEALTINESS: [MessageHandler(filters.TEXT, third_suggestion_healthiness_explanation)],
            POST_DESSERT_HEALTINESS: [MessageHandler(filters.TEXT, fourth_suggestion)],

            PRE_FIRST_COURSE_SUSTAINABILITY: [MessageHandler(filters.TEXT, fourth_suggestion_sustainability_explanation)],
            POST_FIRST_COURSE_SUSTAINABILITY: [MessageHandler(filters.TEXT, fifth_suggestion)],
            PRE_SECOND_COURSE_SUSTAINABILITY: [MessageHandler(filters.TEXT, fifth_suggestion_sustainability_explanation)],
            POST_SECOND_COURSE_SUSTAINABILITY: [MessageHandler(filters.TEXT, sixth_suggestion)],
            PRE_DESSERT_SUSTAINABILITY: [MessageHandler(filters.TEXT, sixth_suggestion_sustainability_explanation)],
            POST_DESSERT_SUSTAINABILITY: [MessageHandler(filters.TEXT, end_of_experiment)],
        },
        fallbacks=[MessageHandler(filters.TEXT, unknown)],
    )
    ##################################################################


    modification_handler = ConversationHandler(
        entry_points=[CommandHandler("modify", modify_profile)],
        states={
            ATTRIBUTE: [MessageHandler(filters.TEXT, choose_attribute)],
            TO_CHOICES: [MessageHandler(filters.TEXT, change_attribute_value)],
        },
        fallbacks=[MessageHandler(filters.TEXT, unknown)],
    )

    session_handler = ConversationHandler(
        entry_points=[CommandHandler("clear_session", clear_session)],
        states={},
        fallbacks=[MessageHandler(filters.TEXT, unknown)],
    )

    application.add_handler(conv_handler)
    application.add_handler(modification_handler)
    application.add_handler(session_handler)
    application.add_handler(path_handler)

    # Aggiunta del CommandHandler per il cambio modalità
    application.add_handler(MessageHandler(filters.TEXT, dialogflow_mode))

    # Aggiunta dell'ErrorHandler
    application.add_error_handler(error)

    logging.info("Bot avviato")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    asyncio.run(main())
