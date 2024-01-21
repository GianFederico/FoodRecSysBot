import os
from flask import Flask
from flask import request, json
import pandas as pd
import expl_types_updated as et

"""
REQUEST EXAMPLE:

http://127.0.0.1:5000/expl?type=2&style=-1&mood=neutral&stress=no&depression=no&bmi=over&activity=low&goal=lose&sleep=low&
restr=gluten-free,vegetarian&imgurl1=https%3A%2F%2Fwww.giallozafferano.it%2Fimages%2Fricette%2F201%2F20113%2Ffoto_hd%2Fhd650x433_wm.jpg&
imgurl2=https%3A%2F%2Fwww.giallozafferano.it%2Fimages%2Fricette%2F176%2F17635%2Ffoto_hd%2Fhd650x433_wm.jpg&
difficulty=1&user_time=0&user_cost=5&health_style=5&health_condition=5&user_ingredients=oil,carrot&user_age=U40&sex=m&season=winter
"""
app = Flask(__name__)


@app.route("/")
def main_page():
    return "I'm working correctly"

@app.route('/expl')
#class Explain(Resource):
def get_expl():
        nutrientsPath = 'Nutrient.json'
        restrictionsPath = 'Restrictions.json'
        richInPath = 'RichIn.json'
        sustainabilityPath = 'Sustainability.json'
        seasonalityPath = 'Seasonality.json'
        dopaminePath = 'Dopamine.json'

        recipeA_url = request.args.get('imgurl1')
        recipeB_url = request.args.get('imgurl2')

        url_dataset_en = 'dataset_en.csv'

        # df = pd.read_csv(url_dataset_en)

        # read files
        with open(nutrientsPath, 'r') as myfile:
            dataNutrients = myfile.read()

        with open(restrictionsPath, 'r') as myfile:
            dataRestrictions = myfile.read()

        with open(richInPath, 'r') as myfile:
            dataRich = myfile.read()

        with open(sustainabilityPath, 'r') as myfile:
            dataSustainability = myfile.read()

        with open(seasonalityPath, 'r') as myfile:
            dataSeasonality = myfile.read()

        with open(dopaminePath, 'r') as myfile:
            dataDopamine = myfile.read()

        nutrients = json.loads(dataNutrients)
        restrictions = json.loads(dataRestrictions)
        listRestrictions = list(restrictions["explanation"].keys())
        richIn = json.loads(dataRich)
        sustainability = json.loads(dataSustainability)
        seasonality = json.loads(dataSeasonality)
        dopamine = json.loads(dataDopamine)

        df = pd.read_csv(url_dataset_en, sep=',')

        recipeA_values = {}
        recipeB_values = {}

        for index, row in df.iterrows():
            if row["imageURL"] == recipeA_url:
                recipeA_values = row
            if row["imageURL"] == recipeB_url:
                recipeB_values = row

        if 'sodium' in recipeA_values:
            recipeA_values["sodium"] = recipeA_values["sodium"] / 1000
        else:
            recipeA_values["sodium"] = 0

        if 'sodium' in recipeB_values:
            recipeB_values["sodium"] = recipeB_values["sodium"] / 1000
        else:
            recipeB_values["sodium"] = 0

        if 'cholesterol' in recipeA_values:
            recipeA_values["cholesterol"] = recipeA_values["cholesterol"] / 1000
        else:
            recipeA_values["cholesterol"] = 0

        if 'cholesterol' in recipeB_values:
            recipeB_values["cholesterol"] = recipeB_values["cholesterol"] / 1000
        else:
            recipeB_values["cholesterol"] = 0

        user = {
            'Age': request.args.get('user_age'),  # numerical age or U20/U30/U40/U50/U60/060
            'Mood': request.args.get('mood'),  # bad/good/neutral
            'Stressed': request.args.get('stress'),  # yes/no
            'Depressed': request.args.get('depression'),  # yes/no
            'BMI': request.args.get('bmi'),  # over/under/normal
            'Health_style': request.args.get('health_style'),  # 1/2/3/4/5
            'Health_condition': request.args.get('health_condition'),  # 1/2/3/4/5
            'Activity': request.args.get('activity'),  # low/high/normal
            'Sleep': request.args.get('sleep'),  # low/good
            'Cooking_exp': request.args.get('difficulty'),  # 1/2/3/4/5
            'User_time': request.args.get('user_time'),  # time for prep in mins [1,200]; 0 stands for "no constraints"
            'User_cost': request.args.get('user_cost'),  # 1/2/3/4 5= not important
            'Goal': request.args.get('goal'),  # lose/gain/no
            'User_restriction': request.args.get('restr'),  # encoded(vegetarian,lactose-free,gluten-free,low-nickel,light)
            'User_ingredients': request.args.get('user_ingredients'),
            'Sex': request.args.get('sex'),  # m,f
            'Season': request.args.get('season')   # winter, spring, summer, autumn
        }

        # exps for the configuration
        two_recipes_experiment = [
            "popularity_two",                   # 0
            "foodGoals_two",                    # 1
            "foodPreferences_two",              # 2
            "foodFeatures_two",                 # 3
            "userSkills_two",                   # 4
            "foodFeatureHealthRisk_two",        # 5
            "foodFeatureHealthBenefits_two",    # 6
            "userFeatureHealthRisk_two",        # 7
            "userFeatureHealthBenefits_two",    # 8
            "userTime_two",                     # 9
            "userCosts_two",                    # 10
            "userLifestyle_two",                # 11
            "userIngredients_two",              # 12
            "userAge_two",                      # 13
            "ingredientsSustainability_two",    # 14
            "ingredientsSeasonality_two",       # 15
            "ingredientsDopamine_two",          # 16
            "descriptions",                     # 17
            "smartExplanation_two"              # 18
        ]

        one_recipe_experiment = [
            "popularity_one",                   # 0
            "foodGoals_one",                    # 1
            "foodPreferences_one",              # 2
            "foodFeatures_one",                 # 3
            "userSkills_one",                   # 4
            "foodFeatureHealthRisk_one",        # 5
            "foodFeatureHealthBenefits_one",    # 6
            "userFeatureHealthRisk_one",        # 7
            "userFeatureHealthBenefits_one",    # 8
            "userTime_one",                     # 9
            "userCosts_one",                    # 10
            "userLifestyle_one",                # 11
            "userIngredients_one",              # 12
            "userAge_one",                      # 13
            "ingredientsSustainability_one",    # 14
            "ingredientsSeasonality_one",       # 15
            "ingredientsDopamine_one",          # 16
            "description",                      # 17
            "smartExplanation_one"              # 18
        ]

        explanations = {}

        # web app requests a specific type of explanation for every recipe(use if u want that same type of exp is shown)
        req_explanation_index = int(request.args.get('type'))
        req_style_index = int(request.args.get('style'))

        if req_explanation_index < 0 or req_explanation_index >= len(one_recipe_experiment):
            explanations.update({"Error": "Explanation type index must be in range 0-"+str(len(one_recipe_experiment)-1)})
        elif req_style_index not in [-1, 0, 1]:
            explanations.update({"Error": "Explanation style index must be -1, 0 or 1"})
        else:
            # if the requested explanation index is -1 -> it will return every expl
            if req_explanation_index == -1:
                # requested style index == -1 -> both single and comparative explanations
                # requested style index == 0  -> only single explanations
                # requested style index == 1  -> only comparative explanation
                if req_style_index == -1 or req_style_index == 0:
                    # expls type 1 a
                    for elem in one_recipe_experiment:
                        expl = et.get_str_exp(user, recipeA_values, None, elem, listRestrictions, nutrients, restrictions, richIn, sustainability, seasonality, dopamine)
                        if expl != "":
                            type_for_recipe_a = elem + "A"
                            explWithTypeA = {type_for_recipe_a: expl}
                            explanations.update(explWithTypeA)

                    # recipeB_url is "" if the parameter imgurl2 is in the request without any associated value,
                    # and it is None if the parameter is not present at all in the request
                    if recipeB_url != "" and recipeB_url != None:
                        # expls type 1 b
                        for elem in one_recipe_experiment:
                                expl = et.get_str_exp(user, recipeB_values, None, elem, listRestrictions, nutrients, restrictions, richIn, sustainability, seasonality, dopamine)
                                if expl != "":
                                    type_for_recipe_b = elem + "B"
                                    explWithTypeB = {type_for_recipe_b: expl}
                                    explanations.update(explWithTypeB)

                if req_style_index == -1 or req_style_index == 1:
                    # expls type 2
                    if recipeB_url != "" and recipeB_url != None:
                        for elem in two_recipes_experiment:
                            expl = et.get_str_exp(user, recipeA_values, recipeB_values, elem, listRestrictions, nutrients, restrictions, richIn, sustainability, seasonality, dopamine)
                            if expl != "":
                                explWithType = {elem: expl}
                                explanations.update(explWithType)

            else:
                type_exp = one_recipe_experiment[req_explanation_index]

                # requested style index == -1 -> both single and comparative explanations
                # requested style index == 0  -> only single explanations
                # requested style index == 1  -> only comparative explanation
                if req_style_index == -1 or req_style_index == 0:
                    # expls type 1 a
                    expl = et.get_str_exp(user, recipeA_values, None, type_exp, listRestrictions, nutrients, restrictions, richIn, sustainability, seasonality, dopamine)
                    if expl != "":
                        type_for_recipe_a = type_exp + "A"
                        explWithTypeA = {type_for_recipe_a: expl}
                        explanations.update(explWithTypeA)

                    # recipeB_url is "" if the parameter imgurl2 is in the request without any associated value,
                    # and it is None if the parameter is not present at all in the request
                    if recipeB_url != "" and recipeB_url != None:
                        # expls type 1 b
                        expl = et.get_str_exp(user, recipeB_values, None, type_exp, listRestrictions, nutrients, restrictions, richIn, sustainability, seasonality, dopamine)
                        if expl != "":
                            type_for_recipe_b = type_exp + "B"
                            explWithTypeB = {type_for_recipe_b: expl}
                            explanations.update(explWithTypeB)

                if req_style_index == -1 or req_style_index == 1:
                    # expls type 2
                    if recipeB_url != "" and recipeB_url != None:
                        type_exp = two_recipes_experiment[req_explanation_index]
                        expl = et.get_str_exp(user, recipeA_values, recipeB_values, type_exp, listRestrictions, nutrients, restrictions, richIn, sustainability, seasonality, dopamine)
                        if expl != "":
                            explWithType = {type_exp: expl}
                            explanations.update(explWithType)

        # conversion Array to JSON
        json_exp = json.dumps({'explanations': explanations})

        return json_exp

#api.add_resource(Explain, '/exp/')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)))


