
from telegram import Update
import requests
from urllib.parse import urlencode
import inflect


class Recommendation:
    
    def __init__(self,img_url=None):
        self.img_url = img_url
    @staticmethod
    async def suggerimento(update: Update, context):
        if 'gender' not in context.user_data:
            return await update.message.reply_text("You do not have a profile yet!\nJust /create it. ", parse_mode="Markdown")

        # Costruire l'URL di richiesta con i parametri
        url = 'http://127.0.0.1:3000/mood?'
        params = {
            'n':1,
            'category': context.user_data['category'],
            'isLowNickel': context.user_data['nickel'],
            'isVegetarian': context.user_data['vegetarian'],
            'isLactoseFree': context.user_data['lactosefree'],
            'isGlutenFree': context.user_data['glutenfree'],
            'isLight': context.user_data['light'],
            'isDiabetes': context.user_data['diabetes'],
            'isPregnant': context.user_data['pregnant'],
            'difficulty': context.user_data['cook_exp'],
            'goal': context.user_data['goals'],
            'user_cost': context.user_data['max_cost_rec'],
            'user_time': context.user_data['time_cook'],
            'fatclass': context.user_data['weight'],
            'age': context.user_data['age'],
            'sex': context.user_data['gender'],
            'mood': context.user_data['mood'],
            'activity': context.user_data['ph_activity'],
            'stress': context.user_data['stress'],
            'sleep': context.user_data['sleep'],
            'depression': context.user_data['depress']
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta = response.json()

        data = risposta.get('data', [])  # Recuperare la lista dei dati delle ricette o una lista vuota se la chiave 'data' non è presente
        if data:
            recipe_data = data[0]  # Recuperare il primo elemento della lista o None se la lista è vuota
            if recipe_data:
                url_ricetta = recipe_data[0]
                title = recipe_data[1]
                Recommendation.img_url = recipe_data[4]
        return await update.message.reply_text(f"Recipe: {title}\nURL: {url_ricetta} \n\nYou can ask me something about this recipe, such as:\nits nutritional facts, its cost, its popularity...and much more!\nOr we could focus on another recipe if you don't like it.\nJust try me.", parse_mode="Markdown")

class Recommendation_due:
    
    def __init__(self,img_url=None):
        self.img_url = img_url
    @staticmethod    
    async def altro_suggerimento2(update: Update, context):
        # Costruire l'URL di richiesta con i parametri
        url = 'http://127.0.0.1:3000/mood?'
        params = {
            'n':2,
            'category': context.user_data['category'],
            'isLowNickel': context.user_data['nickel'],
            'isVegetarian': context.user_data['vegetarian'],
            'isLactoseFree': context.user_data['lactosefree'],
            'isGlutenFree': context.user_data['glutenfree'],
            'isLight': context.user_data['light'],
            'isDiabetes': context.user_data['diabetes'],
            'isPregnant': context.user_data['pregnant'],
            'difficulty': context.user_data['cook_exp'],
            'goal': context.user_data['goals'],
            'user_cost': context.user_data['max_cost_rec'],
            'user_time': context.user_data['time_cook'],
            'fatclass': context.user_data['weight'],
            'age': context.user_data['age'],
            'sex': context.user_data['gender'],
            'mood': context.user_data['mood'],
            'activity': context.user_data['ph_activity'],
            'stress': context.user_data['stress'],
            'sleep': context.user_data['sleep'],
            'depression': context.user_data['depress']
            
        }

        full_url = url + urlencode(params)
        print(full_url)

        response = requests.get(full_url)
        risposta = response.json()
        if response.status_code == 200 and 'data' in risposta:
            data = risposta.get('data', [])
            if data:
                recipe_data = data[1]
                if recipe_data:
                    url_ricetta = recipe_data[0]
                    title = recipe_data[1]
                    Recommendation_due.img_url = recipe_data[4]
                return await update.message.reply_text(f"Ricetta: {title}\nURL: {url_ricetta}")
 
        # await update.message.reply_text("Mi scuso,ma è probabile che in riferimento a ciascuna delle tue informazioni, l'unica ricetta presente nel database è la prima che ti ho consigliato.\nCi adoperemo sicuramente ad inserire ulteriori ricette tenendo presente la combinazione delle tue caratteristiche!\nSe vuoi, puoi ricominciare e cambiare qualche parametro e quasi sicuramente potrò aiutarti con più di una ricetta!")


class Recommendation_tre:
    
    def __init__(self,img_url=None):
        self.img_url = img_url
    @staticmethod    
    async def altro_suggerimento3(update: Update, context):
        # Costruire l'URL di richiesta con i parametri
        url = 'http://127.0.0.1:3000/mood?'
        params = {
            'n':3,
            'category': context.user_data['category'],
            'isLowNickel': context.user_data['nickel'],
            'isVegetarian': context.user_data['vegetarian'],
            'isLactoseFree': context.user_data['lactosefree'],
            'isGlutenFree': context.user_data['glutenfree'],
            'isLight': context.user_data['light'],
            'isDiabetes': context.user_data['diabetes'],
            'isPregnant': context.user_data['pregnant'],
            'difficulty': context.user_data['cook_exp'],
            'goal': context.user_data['goals'],
            'user_cost': context.user_data['max_cost_rec'],
            'user_time': context.user_data['time_cook'],
            'fatclass': context.user_data['weight'],
            'age': context.user_data['age'],
            'sex': context.user_data['gender'],
            'mood': context.user_data['mood'],
            'activity': context.user_data['ph_activity'],
            'stress': context.user_data['stress'],
            'sleep': context.user_data['sleep'],
            'depression': context.user_data['depress']
            
        }

        full_url = url + urlencode(params)
        print(full_url)

        response = requests.get(full_url)
        risposta = response.json()
        if response.status_code == 200 and 'data' in risposta:
            data = risposta.get('data', [])
            if data:
                recipe_data = data[2]
                if recipe_data:
                    url_ricetta = recipe_data[0]
                    title = recipe_data[1]
                    Recommendation_tre.img_url = recipe_data[4]
                return await update.message.reply_text(f"Ricetta: {title}\nURL: {url_ricetta}")
 
        # await update.message.reply_text("Mi scuso,ma è probabile che in riferimento a ciascuna delle tue informazioni, l'unica ricetta presente nel database è la prima che ti ho consigliato.\nCi adoperemo sicuramente ad inserire ulteriori ricette tenendo presente la combinazione delle tue caratteristiche!\nSe vuoi, puoi ricominciare e cambiare qualche parametro e quasi sicuramente potrò aiutarti con più di una ricetta!")
            

def convert_to_lowercase_and_singular(word_list):
    result = []
    for word in word_list:
        lowercase_word = word.lower()
        singular_word = inflect.engine().singular_noun(lowercase_word) or lowercase_word
        result.append(singular_word)
        print(singular_word)
    return result

class SpecificRec:
    
    def __init__(self,img_url=None):
        self.img_url = img_url
    @staticmethod
    async def specific_sugg(update: Update, context, ingredient):
        # Costruire l'URL di richiesta con i parametri
        url = 'http://127.0.0.1:3000/mood?'
        params = {
            'n':15,
            'category': context.user_data['category'],
            'isLowNickel': context.user_data['nickel'],
            'isVegetarian': context.user_data['vegetarian'],
            'isLactoseFree': context.user_data['lactosefree'],
            'isGlutenFree': context.user_data['glutenfree'],
            'isLight': context.user_data['light'],
            'isDiabetes': context.user_data['diabetes'],
            'isPregnant': context.user_data['pregnant'],
            'difficulty': context.user_data['cook_exp'],
            'goal': context.user_data['goals'],
            'user_cost': context.user_data['max_cost_rec'],
            'user_time': context.user_data['time_cook'],
            'fatclass': context.user_data['weight'],
            'age': context.user_data['age'],
            'sex': context.user_data['gender'],
            'mood': context.user_data['mood'],
            'activity': context.user_data['ph_activity'],
            'stress': context.user_data['stress'],
            'sleep': context.user_data['sleep'],
            'depression': context.user_data['depress']
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta = response.json()

        data = risposta.get('data', [])  # Recuperare la lista dei dati delle ricette o una lista vuota se la chiave 'data' non è presente
        print(data[0][25])

        i=0
        recipe_data=None
        ingredient=ingredient.lower()
        single_ingredient= inflect.engine().singular_noun(ingredient) or ingredient
        for i in range(14):
            recipe=data[i]
            ingredient_list = recipe[25][1:-1].split(", ")
            title_words = recipe[1].split(" ")
            single_ingredient_list = convert_to_lowercase_and_singular(ingredient_list)
            single_title_words= convert_to_lowercase_and_singular(title_words)
            if single_ingredient in single_ingredient_list or single_ingredient in single_title_words:
                recipe_data= data[i]
                break
        if recipe_data:
            url_ricetta = recipe_data[0]
            title = recipe_data[1]
            SpecificRec.img_url = recipe_data[4]
        else:
            return await update.message.reply_text(f"I'm sorry, but with the parameters you have chosen there is no good recipe with {ingredient} to suggest.\nYou can /modify you profile and try again.")

        return await update.message.reply_text(f"Recipe: {title}\nURL: {url_ricetta}")