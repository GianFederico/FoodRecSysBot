from telegram import Update
import requests
from urllib.parse import urlencode
import urllib.parse
from recommender_script import Recommendation_due
from recommender_script import Recommendation
from translate import Translator

class Spiegazione:

        @staticmethod
        def spiegazione_restrizioni(update: Update, context):
            restr_list = []
            
            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 2,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_spiegazione = response.json()
            print("Response text:", risposta_spiegazione)
            explanation = risposta_spiegazione.get("explanations", {}).get("foodPreferences_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)       
        
                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_restrizioni_due_piatti(update: Update, context):
            restr_list = []
            
            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 2,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_spiegazione = response.json()
            print("Response text:", risposta_spiegazione)
            explanation = risposta_spiegazione.get("explanations", {}).get("foodPreferences_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def controllo_piatto(update: Update, context):
            restr_list = []
            
            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 3,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_spiegazione = response.json()
            print("Response text:", risposta_spiegazione)
            explanation = risposta_spiegazione.get("explanations", {}).get("foodFeatures_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)
            
        @staticmethod
        def controllo_piatto_due_piatti(update: Update, context):
            restr_list = []
            
            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 3,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_spiegazione = response.json()
            print("Response text:", risposta_spiegazione)
            explanation = risposta_spiegazione.get("explanations", {}).get("foodFeatures_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod        
        def spiegazione_obiettivo(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 1,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()
            print("Response text:", risposta_obiettivo)
            explanation = risposta_obiettivo.get("explanations", {}).get("foodGoals_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_benefici_salute(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 8,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            risposta = response.json()
            print("Response text:", risposta)
            explanation = risposta.get("explanations", {}).get("userFeatureHealthBenefits_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_rischi_salute(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 7,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta = response.json()
            print("Response text:", risposta)
            explanation = risposta.get("explanations", {}).get("userFeatureHealthRisk_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_benefici_salute_due_piatti(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 8,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta = response.json()
            print("Response text:", risposta)
            explanation = risposta.get("explanations", {}).get("userFeatureHealthBenefits_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)
            
        @staticmethod
        def spiegazione_rischi_salute_due_piatti(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 7,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta = response.json()
            print("Response text:", risposta)
            explanation = risposta.get("explanations", {}).get("userFeatureHealthRisk_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_costo(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 10,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            # Esegui la richiesta GET al secondo codice Flask
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            response_costo = response.json()
            explanation = response_costo.get("explanations", {}).get("userCosts_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_costo_due_piatti(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 10,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            # Esegui la richiesta GET al secondo codice Flask
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            response_costo = response.json()
            explanation = response_costo.get("explanations", {}).get("userCosts_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_popolarita(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 0,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()

            print("Response text:", risposta_obiettivo)
            explanation = risposta_obiettivo.get("explanations", {}).get("popularity_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_popolarita_due_piatti(update: Update, context):
            restr_list = []
            
            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 0,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_spiegazione = response.json()
          #  risposta_spiegazione = re.sub(r'\\', '', risposta_spiegazione)
            print("Response text:", risposta_spiegazione)
            explanation = risposta_spiegazione.get("explanations", {}).get("popularity_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_obiettivi_due_piatti(update: Update, context):
            restr_list = []
            
            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 1,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_spiegazione = response.json()
            print("Response text:", risposta_spiegazione)
            explanation = risposta_spiegazione.get("explanations", {}).get("foodGoals_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_tempo(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 9,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()
            print("Response text:", risposta_obiettivo)
            explanation = risposta_obiettivo.get("explanations", {}).get("userTime_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_tempo_due_piatti(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 9,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()
            print("Response text:", risposta_obiettivo)
            explanation = risposta_obiettivo.get("explanations", {}).get("userTime_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_lifestyle(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 11,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()
           # risposta_obiettivo = re.sub(r'\\', '', risposta_obiettivo)
            print("Response text:", risposta_obiettivo)
            explanation = risposta_obiettivo.get("explanations", {}).get("userLifestyle_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_lifestyle_due_piatti(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 11,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()
          #  risposta_obiettivo = re.sub(r'\\', '', risposta_obiettivo)
            print("Response text:", risposta_obiettivo)
            explanation = risposta_obiettivo.get("explanations", {}).get("userLifestyle_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_eta(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 13,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()
            print("Response text:", risposta_obiettivo)
            explanation = risposta_obiettivo.get("explanations", {}).get("userAge_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_eta_due_piatti(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 13,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()
          #  risposta_obiettivo = re.sub(r'\\', '', risposta_obiettivo)
            print("Response text:", risposta_obiettivo)

            explanation = risposta_obiettivo.get("explanations", {}).get("userAge_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_piatto(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 18,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()

            print("Response text:", risposta_obiettivo)
            explanation = risposta_obiettivo.get("explanations", {}).get("smartExplanation_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_piatto_due_piatti(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 18,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()
         #   risposta_obiettivo = re.sub(r'\\', '', risposta_obiettivo)
            print("Response text:", risposta_obiettivo)
            explanation = risposta_obiettivo.get("explanations", {}).get("smartExplanation_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_skill_cucina(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 4,  
                'style':0, 
                'imgurl1': Recommendation.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()

            print("Response text:", risposta_obiettivo)
            explanation = risposta_obiettivo.get("explanations", {}).get("userSkills_oneA")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)

        @staticmethod
        def spiegazione_skill_cucina_due_piatti(update: Update, context):
            restr_list = []

            if context.user_data['nickel'] == 1:
                restr_list.append("low_nickel")

            if context.user_data['vegetarian'] == 1:
                restr_list.append("vegetarian")

            if context.user_data['lactosefree'] == 1:
                restr_list.append("lactose-free")

            if context.user_data['light'] == 1:
                restr_list.append("light")

            if context.user_data['glutenfree'] == 1:
                restr_list.append("gluten-free")
            restr = ','.join(restr_list) if restr_list else None
            url = 'https://foodrecsysexpl-3e81d753188a.herokuapp.com/expl?'
            params = {
                'type': 4,  
                'style':1, 
                'imgurl1': Recommendation.img_url,
                'imgurl2': Recommendation_due.img_url,
                'difficulty': context.user_data['cook_exp'],
                'goal': context.user_data['goals'],
                'user_cost': context.user_data['max_cost_rec'],
                'user_time': context.user_data['time_cook'],
                'user_age': context.user_data['age'],
                'sex': context.user_data['gender'],
                'mood': context.user_data['mood'],
                'bmi': context.user_data['weight'],
                'activity': context.user_data['ph_activity'],
                'stress': context.user_data['stress'],
                'health_style': context.user_data['ht_lifestyle'],
                'health_condition': context.user_data['ht_lifestyle_importance'],
                'sleep': context.user_data['sleep'],
                'depression': context.user_data['depress'],
                'restr': restr
            }
            
            full_url = url + urlencode(params)
            print(full_url)
            response = requests.get(full_url)
            # così otteniamo la risposta come testo
            risposta_obiettivo = response.json()
            print("Response text:", risposta_obiettivo)
            explanation = risposta_obiettivo.get("explanations", {}).get("userSkills_two")
            if explanation:
                max_length = 500
                segments = [explanation[i:i+max_length] for i in range(0, len(explanation), max_length)]

                # così traduciamo ogni segmento separatamente
                translated_segments = []
                translator = Translator(to_lang='it', from_lang='en')
                for segment in segments:
                    translated_segment = translator.translate(segment)
                    translated_segments.append(translated_segment)

                # così concateniamo i segmenti tradotti
                italian_text = ''.join(translated_segments)

                return update.message.reply_text(italian_text)
