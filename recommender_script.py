
from telegram import Update
import requests
from urllib.parse import urlencode


class Recommendation:
    
    def __init__(self,img_url=None):
        self.img_url = img_url
    @staticmethod
    def suggerimento(update: Update, context):
        # Costruire l'URL di richiesta con i parametri
        url = 'https://foodrecsys-673ed7929678.herokuapp.com/mood?'
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
        print("Response content:", risposta)

        data = risposta.get('data', [])  # Recuperare la lista dei dati delle ricette o una lista vuota se la chiave 'data' non è presente
        if data:
            recipe_data = data[0]  # Recuperare il primo elemento della lista o None se la lista è vuota
            if recipe_data:
                url_ricetta = recipe_data[0]
                title = recipe_data[1]
                Recommendation.img_url = recipe_data[4]
        return update.message.reply_text(f"Ricetta: {title}\nURL: {url_ricetta}")

class Recommendation_due:
    
    def __init__(self,img_url=None):
        self.img_url = img_url
    @staticmethod    
    def altro_suggerimento(update: Update, context):
        # Costruire l'URL di richiesta con i parametri
        url = 'https://foodrecsys-673ed7929678.herokuapp.com/mood?'
        params = {
            'n':4,
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
            print("Response content:", risposta)
            data = risposta.get('data', [])
            if data:
                recipe_data = data[1]
                if recipe_data:
                    url_ricetta = recipe_data[0]
                    title = recipe_data[1]
                    Recommendation_due.img_url = recipe_data[4]
                return update.message.reply_text(f"Ricetta: {title}\nURL: {url_ricetta}")
 
        update.message.reply_text("Mi scuso,ma è probabile che in riferimento a ciascuna delle tue informazioni, l'unica ricetta presente nel database è la prima che ti ho consigliato.\nCi adoperemo sicuramente ad inserire ulteriori ricette tenendo presente la combinazione delle tue caratteristiche!\nSe vuoi, puoi ricominciare e cambiare qualche parametro e quasi sicuramente potrò aiutarti con più di una ricetta!")

