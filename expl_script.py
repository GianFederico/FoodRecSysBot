from telegram import Update
import requests
from urllib.parse import urlencode
from recommender_script import Recommendation, Recommendation_due, Recommendation_tre, SpecificRec


class Spiegazione:
    def __init__(self, img_url=None):
        self.img_url = img_url

    @staticmethod
    async def smart_explanation(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")

        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 18,
            "style":-1,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("smartExplanation_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def smartExplanation_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 18,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("smartExplanation_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_restrizioni(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 2,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("foodPreferences_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_restrizioni_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 2,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("foodPreferences_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def controllo_piatto(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 3,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("foodFeatures_oneA")
        if explanation:
            max_length = 50000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def controllo_piatto_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            print("@@@@@@@@@@@@@@@@@@@@here")
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            print("@@@@@@@@@@@@@@hope not@@@@@@here")
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 3,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("foodFeatures_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_obiettivo(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 1,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("foodGoals_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_benefici_salute(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 8,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userFeatureHealthBenefits_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_rischi_salute(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 7,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userFeatureHealthRisk_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_benefici_salute_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            print("@@@@@@@@@@@@@@@@@@@@here")
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            print("@@@@@@@@@@@@@@hope not@@@@@@here")
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 8,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userFeatureHealthBenefits_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_rischi_salute_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 7,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userFeatureHealthRisk_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_costo(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 10,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userCosts_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')
        
    @staticmethod
    async def spiegazione_costo_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 10,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userCosts_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_popolarita(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 0,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("popularity_oneA")
        explanation
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n").replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_popolarita_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 0,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("popularity_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_obiettivi_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 1,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("foodGoals_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_tempo(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 9,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userTime_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_tempo_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 9,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userTime_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_lifestyle(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 11,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userLifestyle_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_lifestyle_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type":11,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userLifestyle_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_eta(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 13,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userAge_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_eta_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 13,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userAge_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_piatto(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 17,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("descriptionA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_piatto_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 17,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("descriptions")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_skill_cucina(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 4,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userSkills_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_skill_cucina_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 4,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("userSkills_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_macros(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 19,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("foodMacros_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            #message = str(explanation_text)[2:-2].replace(r"\n", "\n")
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')
        
    @staticmethod
    async def spiegazione_macros_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 19,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("foodMacros_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')
        
    @staticmethod
    async def spiegazione_sustainability(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 14,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("ingredientsSustainability_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            #message = str(explanation_text)[2:-2].replace(r"\n", "\n")
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_sustainability_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 14,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("ingredientsSustainability_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')

    @staticmethod
    async def spiegazione_seasonability(update: Update, context):
        if not hasattr(Recommendation, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to say.\nYou should ask for a suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        # if context.user_data["light"] == 1:
        #     restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(SpecificRec, 'img_url'):
            imgurl=SpecificRec.img_url
        elif hasattr(Recommendation_tre, 'img_url'):
            imgurl=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            imgurl=Recommendation_due.img_url
        elif hasattr(Recommendation, 'img_url'):
            imgurl=Recommendation.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 15,
            "style":0,
            "imgurl1": imgurl,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }
        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("ingredientsSeasonality_oneA")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            #message = str(explanation_text)[2:-2].replace(r"\n", "\n")
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')
        
    @staticmethod
    async def spiegazione_seasonability_due_piatti(update: Update, context):
        if not hasattr(Recommendation_due, 'img_url'):
            return await update.message.reply_text("Sorry, I don't know what to compare.\nYou should ask for another suggestion first.")
        
        restr_list = []

        if context.user_data["nickel"] == 1:
            restr_list.append("low_nickel")

        if context.user_data["vegetarian"] == 1:
            restr_list.append("vegetarian")

        if context.user_data["lactosefree"] == 1:
            restr_list.append("lactose-free")

        if context.user_data["light"] == 1:
            restr_list.append("light")

        if context.user_data["glutenfree"] == 1:
            restr_list.append("gluten-free")

        if hasattr(Recommendation_tre, 'img_url'):
            first=Recommendation_due.img_url
            second=Recommendation_tre.img_url
        elif hasattr(Recommendation_due, 'img_url'):
            first=Recommendation.img_url
            second=Recommendation_due.img_url

        restr = ",".join(restr_list) if restr_list else None
        url = "http://127.0.0.1:5000/expl?"
        params = {
            "type": 15,
            "style": 1,
            "imgurl1": first,
            "imgurl2": second,
            "difficulty": context.user_data["cook_exp"],
            "goal": context.user_data["goals"],
            "user_cost": context.user_data["max_cost_rec"],
            "user_time": context.user_data["time_cook"],
            "user_age": context.user_data["age"],
            "sex": context.user_data["gender"],
            "mood": context.user_data["mood"],
            "bmi": context.user_data["weight"],
            "activity": context.user_data["ph_activity"],
            "stress": context.user_data["stress"],
            "health_style": context.user_data["ht_lifestyle"],
            "health_condition": context.user_data["ht_lifestyle_importance"],
            "sleep": context.user_data["sleep"],
            "depression": context.user_data["depress"],
            "restr": restr,
        }

        full_url = url + urlencode(params)
        print(full_url)
        response = requests.get(full_url)
        # così otteniamo la risposta come testo
        risposta_spiegazione = response.json()
        print("Response text:", risposta_spiegazione)
        explanation = risposta_spiegazione.get("explanations", {}).get("ingredientsSeasonality_two")
        if explanation:
            max_length = 5000
            segments = [
                explanation[i : i + max_length]
                for i in range(0, len(explanation), max_length)
            ]

            explanation_text=[]
            for segment in segments:
                explanation_text.append(segment)

            print("@@@@@@@@@@@@@@@@ EXPLANATION TEXT:", explanation_text)
            return await update.message.reply_text(str(explanation_text)[2:-2].replace(r"\n", "\n"), parse_mode='Markdown')