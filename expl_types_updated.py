import random
import numpy as np
from functools import reduce
import re
from datetime import datetime
import textwrap
import os

"""
The popularity_one explanation function returns a string
containing the average rating of the given recipe and the number of ratings.
"""
def popularity_one(recipe):
    explanation = recipe["title"] + " has an average rating of " + str(recipe["ratingValue"]) \
                  + "/5 out of " + str(recipe["ratingCount"])[:-2] + " community ratings."
    return explanation


"""
The popularity_two explanation function returns a string
with a comparison of recipeA's rating count with respect to recipeB's.
Their respective average ratings are also shown.
"""
def popularity_two(recipeA, recipeB):
    explanation = ""
    recipeA_name = recipeA["title"]
    recipeB_name = recipeB["title"]
    recipeA_rc = recipeA["ratingCount"]
    recipeB_rc = recipeB["ratingCount"]
    recipeA_rv = recipeA["ratingValue"]
    recipeB_rv = recipeB["ratingValue"]

    if recipeA_rc > recipeB_rc:
        explanation = recipeA_name + " (" + str(recipeA_rc)[:-2] + " ratings, average: " + str(recipeA_rv) \
                      + "/5) is more popular than " + recipeB_name + " (" + str(recipeB_rc)[:-2] \
                      + " ratings, average: " + str(recipeB_rv) + "/5) in the community."
    if recipeA_rc < recipeB_rc:
        explanation = recipeA_name + " (" + str(recipeA_rc)[:-2] + " ratings, average: " + str(recipeA_rv) \
                      + "/5) is less popular than " + recipeB_name + " (" + str(recipeB_rc)[:-2] \
                      + " ratings, average: " + str(recipeB_rv) + "/5) in the community."
    if recipeA_rc == recipeB_rc:
        explanation = recipeA_name + " (average rating: " + recipeA_rv + ") is as popular as " \
                      + recipeB_name + " (average rating: " + recipeB_rv + ") in the community (" \
                      + str(recipeA_rc)[:-2] + " ratings)."

    return explanation


"""
The foodGoals_one explanation function takes as input a recipe and a user.
The user's sex and goal (lose -> lose weight, gain -> gain weight, no -> maintain weight)
and the recipe's calories are taken into account to check if the given recipe
may be a good fit for the user.
"""
# def foodGoals_one(recipe, user):
#     explanation = ""
#     recipe_calories = recipe["calories"]
#     user_sex = user["Sex"]
#     user_goal = user["Goal"]
#     user_activity = user["Activity"]

#     explanation = recipe["title"] + " has " + str(recipe_calories) + " Kcal. "

#     # Average daily calorie intake for men: 2500 Kcal
#     # Average daily calorie intake for women: 2000 Kcal
#     # Assumption: a single meal is 40% of the daily intake

#     # Average daily calorie intake for men and women
#     average_daily_intake = {
#         "m": {"lose": 2000, "gain": 2500, "no": 2250},
#         "f": {"lose": 1600, "gain": 1900, "no": 1700},
#     }

#     if user_sex is None or user_sex == "": # TO CHECK cannot take none or "" as user[sex] value 
#         intake = average_daily_intake["m"]["no"] if user_goal == "no" else average_daily_intake["f"]["no"]
#         man_or_woman = "person of unspecified sex"
#         if user_activity == 'low':
#             intake += 0
#         elif user_activity == 'normal':
#             intake += 150
#         elif user_activity == 'high':
#             intake +=250

#     else:
#         intake = average_daily_intake[user_sex][user_goal]
#         man_or_woman = "man" if user_sex == "m" else "woman"
#         if user_activity == 'low':
#             intake += 0
#         elif user_activity == 'normal':
#             intake += 150
#         elif user_activity == 'high':
#             intake +=250

#     if recipe_calories < intake*0.07 and user_goal=='lose':
#         explanation += "It is a good choice, since you are aiming to " + user_goal + " weight. "
#     elif recipe_calories > intake*0.07 and user_goal=='lose':
#         explanation += "It may not be the best choice, since you are aiming to " + user_goal + " weight (high-kcal). "

#     if recipe_calories > intake*0.10 and user_goal=='gain':
#         explanation += "It is a good choice, since you are aiming to " + user_goal + " weight. "
#     elif recipe_calories < intake*0.10 and user_goal=='gain':
#         explanation += "It may not be the best choice, since you are aiming to " + user_goal + " weight (low-kcal). "

#     if intake*0.07 < recipe_calories < intake*0.10 and user_goal=='no':
#         explanation += "It is a good choice, since you are aiming to maintain weight. "
#     elif recipe_calories < intake*0.07  and user_goal=='no':
#         explanation += "It may not be the best choice, since you are aiming to maintain weight (low-kcal). "
#     elif recipe_calories > intake*0.10 and user_goal=='no':
#         explanation += "It may not be the best choice, since you are aiming to maintain weight (high-kcal). "

#     percentage = round((recipe_calories / intake) * 100, 2)
#     explanation += (
#         "The average daily calorie intake for a "
#         + man_or_woman
#         + " with your goal and type of activity is "
#         + str(intake)
#         + " Kcal and this recipe represents "
#         + str(percentage)
#         + "% of your daily intake. "
#     )

#     return explanation






#___________________________________________________________persuasive attempt_________________________________________________________________________________________________________

def foodGoals_one(recipe, user):
    explanation = "We're glad you're taking steps towards your nutritional goals! " ###################################positive language + commitment (aknowledgemnt of actions)
    recipe_calories = recipe["calories"]
    user_sex = user["Sex"]
    user_goal = user["Goal"]
    user_activity = user["Activity"]

    explanation = recipe["title"] + " has " + str(recipe_calories) + " Kcal. "

    # Average daily calorie intake for men: 2500 Kcal
    # Average daily calorie intake for women: 2000 Kcal
    # Assumption: a single meal is 40% of the daily intake

    # Average daily calorie intake for men and women
    average_daily_intake = {
        "m": {"lose": 2000, "gain": 2500, "no": 2250},
        "f": {"lose": 1600, "gain": 1900, "no": 1700},
    }

    if user_sex is None or user_sex == "": # TO CHECK cannot take none or "" as user[sex] value 
        intake = average_daily_intake["m"]["no"] if user_goal == "no" else average_daily_intake["f"]["no"]
        man_or_woman = "person of unspecified sex"
        if user_activity == 'low':
            intake += 0
        elif user_activity == 'normal':
            intake += 150
        elif user_activity == 'high':
            intake +=250

    else:
        intake = average_daily_intake[user_sex][user_goal]
        man_or_woman = "man" if user_sex == "m" else "woman"
        if user_activity == 'low':
            intake += 0
        elif user_activity == 'normal':
            intake += 150
        elif user_activity == 'high':
            intake +=250

    percentage = round((recipe_calories / intake) * 100, 2)
    additional_explanation = (
        "The average daily calorie intake for a "
        + man_or_woman
        + " with your goal and type of activity is "
        + str(intake)
        + " Kcal and this recipe represents "
        + str(percentage)
        + "% of your daily intake. "
    )

    if recipe_calories < intake*0.07 and user_goal=='lose':
        explanation += "It is a good choice, since you are aiming to " + user_goal + " weight. "
        explanation += additional_explanation
        explanation += "Many users with similar goals and activity levels have enjoyed this recipe." ###############################################social proof
        
    elif recipe_calories > intake*0.07 and user_goal=='lose':
        explanation += "It may not be the best choice, since you are aiming to " + user_goal + " weight (high-kcal). "
        explanation += additional_explanation
        explanation += "While this recipe may not align perfectly with your current goals and activity levels, there are plenty of other delicious options waiting for you." 
                            #########################pos language still encouraging the user

    if recipe_calories > intake*0.10 and user_goal=='gain':
        explanation += "It is a good choice, since you are aiming to " + user_goal + " weight. "
        explanation += additional_explanation
        explanation += "Many users with similar goals and activity levels have enjoyed this recipe." ###############################################social proof
    elif recipe_calories < intake*0.10 and user_goal=='gain':
        explanation += "It may not be the best choice, since you are aiming to " + user_goal + " weight (low-kcal). "
        explanation += additional_explanation
        explanation += "While this recipe may not align perfectly with your current goals and activity levels, there are plenty of other delicious options waiting for you."

    if intake*0.07 < recipe_calories < intake*0.10 and user_goal=='no':
        explanation += "It is a good choice, since you are aiming to maintain weight. "
        explanation += additional_explanation
        explanation += "Many users with similar goals and activity levels have enjoyed this recipe." ###############################################social proof
    elif recipe_calories < intake*0.07  and user_goal=='no':
        explanation += "It may not be the best choice, since you are aiming to maintain weight (low-kcal). "
        explanation += additional_explanation
        explanation += "While this recipe may not align perfectly with your current goals and activity levels, there are plenty of other delicious options waiting for you."
                                #########################pos language still encouraging the user
    elif recipe_calories > intake*0.10 and user_goal=='no':
        explanation += "It may not be the best choice, since you are aiming to maintain weight (high-kcal). "
        explanation += additional_explanation
        explanation += "While this recipe may not align perfectly with your current goals and activity levels, there are plenty of other delicious options waiting for you."
                                #########################pos language still encouraging the user
    
    return explanation

#______________________________________________________________________________________________________________________________________________________________________________________












"""
The foodGoals_two explanation function takes as input two recipes and a user.
The user's sex and goal (lose -> lose weight, gain -> gain weight, no -> no goals)
and the recipes' calories are taken into account to compare the two recipes and
check which one may be a better fit for the user.
"""
def foodGoals_two(recipeA, recipeB, user):
    explanation_A = ""
    explanation_B = ""
    recipeA_calories = recipeA["calories"]
    recipeB_calories = recipeB["calories"]
    user_sex = user["Sex"]
    user_goal = user["Goal"]
    user_activity = user["Activity"]

    average_daily_intake = {
    "m": {"lose": 2000, "gain": 2500, "no": 2250},
    "f": {"lose": 1500, "gain": 1800, "no": 1650},
    }
    intake = average_daily_intake[user_sex][user_goal]
    man_or_woman = "man" if user_sex == "m" else "woman"

    if user_activity == 'low':
        intake += 0
    elif user_activity == 'normal':
        intake += 150
    elif user_activity == 'high':
        intake +=250

    if recipeA_calories == recipeB_calories:
        explanation = "Both recipies have the same amount of Kcals. "
        explanation += recipeA["title"] + " has " + str(recipeA_calories) + "Kcal and "
        explanation += recipeB["title"] + " has " + str(recipeB_calories) + "Kcal. "
        same_kcals = recipeA["calories"]

        average_daily_intake = {
        "m": {"lose": 2000, "gain": 2500, "no": 2250},
        "f": {"lose": 1500, "gain": 1800, "no": 1650},
        }

        if user_sex is None or user_sex == "": # TO CHECK cannot take none or "" as user[sex] value 
            intake = average_daily_intake["m"]["no"] if user_goal == "no" else average_daily_intake["f"]["no"]
            man_or_woman = "person of unspecified sex"

        if user_activity == 'low':
            intake += 0
        elif user_activity == 'normal':
            intake += 150
        elif user_activity == 'high':
            intake +=250

        if same_kcals < intake*0.15 and user_goal=='lose':
            explanation += "They are a good choice, since you are aiming to " + user_goal + " weight."
        elif same_kcals > intake*0.15 and user_goal=='lose':
            explanation += "They may not be the best choice, since you are aiming to " + user_goal + " weight (high-kcal). "

        if same_kcals > intake*0.25 and user_goal=='gain':
            explanation += "They are a good choice, since you are aiming to " + user_goal + " weight. "
        elif same_kcals < intake*0.25 and user_goal=='gain':
            explanation += "They may not be the best choice, since you are aiming to " + user_goal + " weight (low-kcal). "

        if intake*0.15 < same_kcals < intake*0.25 and user_goal=='no':
            explanation += "They are a good choice, since you are aiming to maintain weight. "
        elif same_kcals < intake*0.15  and user_goal=='no':
            explanation += "They may not be the best choice, since you are aiming to maintain weight (low-kcal). "
        elif same_kcals > intake*0.25 and user_goal=='no':
            explanation += "They may not be the best choice, since you are aiming to maintain weight (high-kcal). "

        percentage = round((same_kcals / intake) * 100, 2)
        explanation += (
            "The average daily calorie intake for a "
            + man_or_woman
            + " with your goal and type of activity is "
            + str(intake)
            + " Kcal and this recipe represents "
            + str(percentage)
            + "% of your daily intake. "
        )
    else:
        explanation_A = foodGoals_one(recipeA, user)
        explanation_B = foodGoals_one(recipeB, user)
        useless_expl = (
            ". The average daily calorie intake for a "
            + man_or_woman
            + " with your goal and type of activity is "
            + str(intake)
            + " Kcal and ")

        explanation_A = str(explanation_A).replace(useless_expl, ", ")
        explanation = explanation_A + explanation_B

            
        if user_goal == 'gain':
            if recipeA_calories > recipeB_calories:
                explanation += "Anyway, between the two, " + recipeA["title"] + " seems more suitable for you since it has more calories."
            else:
                explanation += "Anyway, between the two, " + recipeB["title"] + " seems more suitable for you since it has more calories."

        if user_goal == 'lose':
            if recipeA_calories > recipeB_calories:
                explanation += "Anyway, between the two, " + recipeB["title"] + " seems more suitable for you since it has less calories."
            else:
                explanation += "Anyway, between the two, " + recipeA["title"] + " seems more suitable for you since it has less calories."

        #caso maintain? non ha senso farlo
    return explanation  


"""
The foodPreferences_one explanation function checks if a given recipe follows
the user restrictions (vegetarian, lactose-free, gluten-free, low-nickel, light).
If they are all respected by the recipe, the returned string provides
explanations for all restrictions; otherwise, the restrictions that are
not followed by the recipe are listed.

Also, if no user restriction is specified (-1)
or if the specified user restrictions are not included in the list mentioned above (-2),
respective error codes are returned.
"""
def foodPreferences_one(userRestrictions, listRestrictions, restrictions, recipe):
    explanation = ""
    restr_and_desc = {}

    if userRestrictions is None or userRestrictions == "":
        explanation = -1
    else:
        userRestrictions = userRestrictions.split(",")

        for restr in userRestrictions:
            if restr in listRestrictions:
                restr_words = restr.split("-")
                isRestr = "is"
                for word in restr_words:
                    isRestr += word.capitalize()
                restr_and_desc[isRestr] = [restr, restrictions["explanation"][restr]]

        if not restr_and_desc:
            explanation = -2
        else:
            not_followed_restrictions = []
            for isRestr in restr_and_desc:
                if recipe[isRestr] == 0:
                    not_followed_restrictions.append(restr_and_desc[isRestr][0])

            if not_followed_restrictions:
                explanation = recipe["title"] + " does not respect your restrictions, since it is not "
                for restr in not_followed_restrictions:
                    explanation += restr + " nor "

                explanation = explanation[:-len(" nor ")]

            else:
                explanation = recipe["title"]

                for restr in restr_and_desc.keys():
                    explanation += " is a " + restr_and_desc[restr][0] + " recipe, so " + restr_and_desc[restr][1] + "; furthermore, it"

                explanation = explanation[:-len("; furthermore, it")]

            explanation += "."

    return explanation, not_followed_restrictions


"""
The foodPreferences_two explanation function calls foodPreferences_one on two recipes.
"""
def foodPreferences_two(userRestrictions, listRestrictions, restrictions, recipeA, recipeB): 
    explanation = ""

    explA, not_followed_rest_A = foodPreferences_one(userRestrictions, listRestrictions, restrictions, recipeA)
    explB, not_followed_rest_B = foodPreferences_one(userRestrictions, listRestrictions, restrictions, recipeB)
    if explA != -1 and explA != -2:
        explanation = explA + " On the other hand, " + explB
    else:
        explanation = explA

    if not_followed_rest_A > not_followed_rest_B:
        explanation += " It seems that " + recipeB["title"] + "fits better your restrictions."
    elif not_followed_rest_A < not_followed_rest_B:
        explanation += " It seems that " + recipeA["title"] + "fits better your restrictions."
    else:
        explanation += " In this case there really isn't a better recipe between the two."
        

    return explanation


"""
The foodFeatures explanation function compares the amounts of various nutrients (gr)
in one recipe to 40% of the respective daily reference intake (RI) (if recipeB == None)
or between two recipes (if recipeB != None).
(assumption: one meal contains 40% of the daily intake)
Two lists are also returned: greatList and smallList.
They respectively contain the nutrients that exceed and subceed
the average meal intake’s (or recipeB’s) respective quantity.
"""
def foodFeatures(recipeA, recipeB, nutrients): #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@meh@@@@@@@@@@@@@@@@@@@@@@@
    explanation = ""

    recipeA_name = recipeA["title"]
    if recipeB is not None:
        recipeB_name = recipeB["title"]

    smallList = []
    greatList = []

    # collecting the list of nutrients
    listNutrients = list(nutrients.keys())
    # randomize the nutrients list
    random.shuffle(listNutrients)

    if recipeB is None:
        for item in listNutrients:
            if not (np.isnan(recipeA[item])):
                if recipeA[item] <= nutrients[item]["RI"] * 0.4:
                    smallList.append(item)
                    nutrient = re.sub(r"(\w)([A-Z])", r"\1 \2", item)
                    explanation += recipeA_name + " has a smaller amount of " + nutrient.lower() + " (" + \
                                   str(recipeA[item]) + " gr) than 40% of its daily reference intake (" + \
                                   str(round(nutrients[item]["RI"] * 0.4, 3)) + " gr). "
                else:
                    greatList.append(item)
                    nutrient = re.sub(r"(\w)([A-Z])", r"\1 \2", item)
                    explanation += recipeA_name + " has a greater amount of " + nutrient.lower() + " (" + \
                                   str(recipeA[item]) + " gr) than 40% of its daily reference intake (" + \
                                   str(round(nutrients[item]["RI"] * 0.4, 3)) + " gr). "

        if not smallList:
            explanation += "There isn't a lower amount of any nutrient than 40% of its daily reference intake. "
        if not greatList:
            explanation += "There isn't a higher amount of any nutrient than 40% of its daily reference intake. "

    else:
        for item in listNutrients:
            if not (np.isnan(recipeA[item])) and not (np.isnan(recipeB[item])):
                if recipeA[item] < recipeB[item]:
                    smallList.append(item)
                    nutrient = re.sub(r"(\w)([A-Z])", r"\1 \2", item)
                    explanation += recipeA_name + " has a smaller amount of " + nutrient.lower() + " (" + \
                                   str(recipeA[item]) + " gr) than " + recipeB_name + " (" + \
                                   str(recipeB[item]) + " gr). "

                if recipeA[item] > recipeB[item]:
                    greatList.append(item)
                    nutrient = re.sub(r"(\w)([A-Z])", r"\1 \2", item)
                    explanation += recipeA_name + " has a greater amount of " + nutrient.lower() + " (" + \
                                   str(recipeA[item]) + " gr) than " + recipeB_name + " (" + \
                                   str(recipeB[item]) + " gr). "

    return explanation, smallList, greatList


"""
The convertRecipeDifficulty function takes as input
an Italian string for a recipe difficulty (Molto facile, Facile...) or a number in a 1-5 scale
and returns the corresponding number in a 1-5 scale and an English translation.
"""
def convertRecipeDifficulty(recipe_difficulty):
    num = -1
    en = ""
    if recipe_difficulty == "Molto facile" or recipe_difficulty == 1:
        num = 1
        en = "very simple"
    elif recipe_difficulty == "Facile" or recipe_difficulty == 2:
        num = 2
        en = "simple"
    elif recipe_difficulty == "Media" or recipe_difficulty == 3:
        num = 3
        en = "quite simple"
    elif recipe_difficulty == "Difficile" or recipe_difficulty == 4:
        num = 4
        en = "difficult"
    elif recipe_difficulty == "Molto difficile" or recipe_difficulty == 5:
        num = 5
        en = "very difficult"
    return num, en


"""
The userSkills_one explanation function takes as input the user's cooking experience and a recipe.
It returns a string with a comparison between the user's skills and the recipe's difficulty.
"""
def userSkills_one(user_skills, recipe):
    explanation = ""

    recipe_difficulty_num, recipe_difficulty_en = convertRecipeDifficulty(recipe["difficulty"])

    explanation = recipe["title"] + " is rated by the users as " + recipe_difficulty_en + " to prepare, "

    if recipe_difficulty_num > user_skills:
        explanation += "which is beyond your cooking skills."
    else:
        explanation += "and it is adequate to your cooking skills."

    return explanation


"""
The userSkills_twp explanation function takes as input the user's cooking experience and two recipes.
The recipes' difficulties are compared and the easier recipe is compared with the user's skills.
"""
def userSkills_two(user_skills, recipeA, recipeB):
    explanation = ""

    recipeA_name = recipeA["title"]
    recipeB_name = recipeB["title"]
    diffA_num, diffA_en = convertRecipeDifficulty(recipeA["difficulty"])
    diffB_num, diffB_en = convertRecipeDifficulty(recipeB["difficulty"])

    if diffA_num < diffB_num:
        explanation = recipeA_name + " (" + diffA_en + ") is rated by the users as easier to prepare than " \
                      + recipeB_name + " (" + diffB_en + "), "
        easier_diff = diffA_num
    elif diffA_num > diffB_num:
        explanation = recipeB_name + " (" + diffB_en + ") is rated by the users as easier to prepare than " \
                      + recipeA_name + " (" + diffA_en + "), "
        easier_diff = diffB_num
    else:
        explanation = recipeA_name + " is as easy to prepare as " + recipeB_name + " (" + diffA_en + "), "
        easier_diff = diffA_num

    if easier_diff > user_skills:
        explanation += "but it is beyond your cooking skills."
    else:
        explanation += "and it is adequate to your cooking skills."

    return explanation


"""
The compareCalories function provides a comparison of the quantity of calories between two recipes.
"""
def compareCalories(recipeA_name, recipeB_name, recipeA_cal, recipeB_cal):
    explanation = ""

    if not np.isnan(recipeA_cal) and not np.isnan(recipeB_cal):
        if recipeA_cal > recipeB_cal:
            explanation += "Furthermore, " + recipeA_name + " has more calories (" + str(recipeA_cal) \
                           + " Kcal) than " + recipeB_name + " (" + str(recipeB_cal) + " Kcal)."
        elif recipeA_cal < recipeB_cal:
            explanation += "Furthermore, " + recipeA_name + " has less calories (" + str(recipeA_cal) \
                           + " Kcal) than " + recipeB_name + " (" + str(recipeB_cal) + " Kcal)."
        else:
            explanation += "Furthermore, both recipes have got the same amount of calories (" + str(recipeA_cal) \
                           + " Kcal)."

    return explanation


"""
The rankNutrientsOffsets function is used in foodFeatureHealthRiskBenefit if the type of explanation is "risks"
and in userFeatureHealthRisk.
The output is two lists:
- one containing recipeA's top 2 nutrients that surpass 40% of the reference daily intake (or recipeB if recipeB != None)
- one containing recipeA's 2 nutrients with the lowest quantities
"""
def rankNutrientsOffsets(recipeA, recipeB, nutrients):
    greatList = []
    smallList = []
    offsetDict = {}

    for nutr in nutrients.keys():
        if recipeB is None:
            offset = round((recipeA[nutr] - nutrients[nutr]["RI"] * 0.4), 3)
        else:
            offset = round((recipeA[nutr] - recipeB[nutr]), 3)

        offsetDict[nutr] = offset

    for i in range(2):
        maxOffset = 0
        maxNutr = ""
        minOffset = 0
        minNutr = ""
        for key in offsetDict.keys():
            if offsetDict[key] > maxOffset:
                maxOffset = offsetDict[key]
                maxNutr = key
            elif offsetDict[key] < minOffset:
                minOffset = offsetDict[key]
                minNutr = key
        if maxOffset != 0:
            greatList.append(maxNutr)
            del offsetDict[maxNutr]
        if minOffset != 0:
            smallList.append(minNutr)
            del offsetDict[minNutr]

    return smallList, greatList


"""
The checkClosestNutrientsToRI function is used in FoodFeatureHealthRiskBenefit if the type of explanation is "benefits"
and in userFeatureHealthBenefits.
It returns a list containing the top 2 nutrients whose values in the given recipe are
closest to 40% of their respective reference daily intake.
"""
def checkClosestNutrientsToRI(recipe, nutrients):
    offsetDict = {}
    closest_to_RI = []
    for nutr in nutrients.keys():
        if not np.isnan(recipe[nutr]):
            offsetDict[nutr] = abs(round((recipe[nutr] - nutrients[nutr]["RI"] * 0.4), 3))

    for i in range(2):
        minOffset = 1000
        minNutr = ""
        for key in offsetDict.keys():
            if offsetDict[key] < minOffset:
                minOffset = offsetDict[key]
                minNutr = key
        closest_to_RI.append(minNutr)
        del offsetDict[minNutr]

    return closest_to_RI


"""
The foodFeatureHealthRiskBenefit explanation function calls the foodFeatures function.

Then, if the type of explanation is "risks",
random risks associated to a high assumption of rankNutrientsOffsets's greatList nutrients
are added to the explanation.
If rankNutrientsOffsets's greatList is empty,
random risks associated to a low assumption of rankNutrientsOffsets's smallList nutrients
are added to the explanation instead.

Otherwise, if the type of explanation is "benefits",
random benefits associated to a healthy assumption of checkClosestNutrientsToRI's nutrients
are added to the explanation.

Then, if recipeB != None, there is a comparison of the amount of calories of the two recipes.
"""
def foodFeatureHealthRiskBenefit(recipeA, recipeB, nutrients, type):
    explanation = ""
    smallList = []
    greatList = []
    risk_benefit = ""

    recipeA_name = recipeA["title"]
    if recipeB is not None:
        recipeB_name = recipeB["title"]

    explanation, _, _ = foodFeatures(recipeA, recipeB, nutrients)

    if type == "risks":
        smallList, greatList = rankNutrientsOffsets(recipeA, recipeB, nutrients)

        if greatList:
            kind_of_risks = "risksTooMuch"
            nutrList = greatList
            higher_or_lower = "higher"
        else:
            kind_of_risks = "risksTooLittle"
            nutrList = smallList
            higher_or_lower = "lower"

        for item in nutrList:
            risk_benefit = random.choice(nutrients[item][kind_of_risks])
            nutrient = re.sub(r"(\w)([A-Z])", r"\1 \2", item)
            explanation += recipeA_name + "'s quantity of " + nutrient.lower() + " (" + str(recipeA[item]) \
                           + " g) is " + higher_or_lower + " than "
            if recipeB is None:
                explanation += "40% of its daily reference intake (" \
                               + str(round(nutrients[item]["RI"] * 0.4)) + " g)"
            else:
                explanation += recipeB_name + "'s (" + str(recipeB[item]) + " g)"
            explanation += "; a " + higher_or_lower[:-2] + " intake of " + nutrient.lower() \
                        + " could increase the risk of " + risk_benefit + "."

    else:
        # benefits
        closest_to_RI = checkClosestNutrientsToRI(recipeA, nutrients)
        closestNutrient1 = re.sub(r"(\w)([A-Z])", r"\1 \2", closest_to_RI[0]).lower()
        closestNutrient2 = re.sub(r"(\w)([A-Z])", r"\1 \2", closest_to_RI[1]).lower()

        explanation += recipeA_name + "'s quantities of " + closestNutrient1 + " and " + closestNutrient2 \
                       + ", among all nutrients in the recipe, are the closest to the respective recommended intakes; " \
                       + closestNutrient1 + " can " + random.choice(nutrients[closest_to_RI[0]]["benefits"]) \
                       + ", while " + closestNutrient2 + " can " + random.choice(nutrients[closest_to_RI[1]]["benefits"]) \
                       + "."

    if recipeB is not None:
        explanation += compareCalories(recipeA_name, recipeB_name, recipeA["calories"], recipeB["calories"])

    return explanation


"""
The userFeatureHealthRisks explanation function calls the rankNutrientsOffsets function
and then connects the recipe A with user characteristics (BMI, mood, depressed/stressed).
It returns a string with a risk related to the nutrient and the mood/BMI of the user.
If recipeB != None, there is also a comparison between the recipes' calories.
"""
def userFeatureHealthRisk(user, recipeA, recipeB, nutrients):
    smallA = []
    greatA = []
    explanation = ""

    recipeA_name = recipeA["title"]
    if recipeB is not None:
        recipeB_name = recipeB["title"]
    smallA, greatA = rankNutrientsOffsets(recipeA, recipeB, nutrients)

    _, full_smallA, full_greatA = foodFeatures(recipeA, recipeB, nutrients)

    if user["BMI"] == "over" and greatA:
        listMood = ["sugars", "carbohydrates", "proteins"]

        for item in greatA:
            item_fixed = re.sub(r"(\w)([A-Z])", r"\1 \2", item).lower()
            explanation += recipeA_name + "'s quantity of " + item_fixed + " (" + str(recipeA[item]) \
                           + " g) is higher than "
            if recipeB is None:
                explanation += "40% of its reference daily intake (" \
                               + str(round(nutrients[item]["RI"] * 0.4)) + " g). "
            else:
                explanation += recipeB_name + "'s (" + str(recipeB[item]) + " g). "

            if user["Mood"] == "bad" or user["Mood"] == "neutral" \
                    or user["Depressed"] == "yes" or user["Stressed"] == "yes":

                if item in listMood:
                    explanation += "An excess of " + item_fixed + " can swing your mood. "

        # check if there is a significant difference
        if len(full_greatA) >= len(full_smallA) * 2:
            explanation += "Given that you are overweight, keep in mind that " \
                        + recipeA_name + " may not be able to help you to lose weight. "

    elif user["BMI"] == "under" and smallA:
        for item in smallA:
            item_fixed = re.sub(r"(\w)([A-Z])", r"\1 \2", item).lower()
            explanation += recipeA_name + "'s quantity of " + item_fixed + " (" + str(recipeA[item]) \
                           + " g) is lower than "
            if recipeB is None:
                explanation += "40% of its reference daily intake (" \
                               + str(round(nutrients[item]["RI"] * 0.4)) + " g). "
            else:
                explanation += recipeB_name + "'s (" + str(recipeB[item]) + " g). "

        # check if there is a significant difference
        if len(full_greatA) * 2 <= len(full_smallA):
            explanation += "Given that you are underweight, keep in mind that " \
                        + recipeA_name + " may not be able to help you to gain weight. "

    elif user["BMI"] == "over" or user["BMI"] == "under":
        if user["BMI"] == "over":
            more_or_less = " exceeds "
        else:
            more_or_less = " is less than "

        explanation += "Considering that you are " + user["BMI"] + "weight, " \
                    + recipeA_name + " has no nutrient whose quantity" + more_or_less
        if recipeB is None:
            explanation += "40% of its daily reference intake, "
        else:
            explanation += recipeB_name + "'s, "
        explanation += "which is a good fit for you. "

    else:
        explanation, _, _ = foodFeatures(recipeA, recipeB, nutrients)

    if recipeB is not None:
        explanation += compareCalories(recipeA_name, recipeB["title"], recipeA["calories"], recipeB["calories"])

    return explanation


"""
The userFeatureHealthBenefits explanation function calls the checkClosestNutrientsToRI function
and then connects the recipe A with user characteristics (BMI, mood, depressed/stressed).
It returns a string with a benefit related to the nutrient and the mood/BMI of the user.
If recipeB != None, there is also a comparison between the recipes' calories.
"""
def userFeatureHealthBenefits(user, recipeA, recipeB, nutrients):
    explanation = ""

    recipeA_name = recipeA["title"]
    recipeA_closest_to_RI = checkClosestNutrientsToRI(recipeA, nutrients)

    recipeA_nutr1 = recipeA_closest_to_RI[0]
    recipeA_nutr2 = recipeA_closest_to_RI[1]

    if recipeB is not None:
        recipeB_name = recipeB["title"]
        recipeB_closest_to_RI = checkClosestNutrientsToRI(recipeB, nutrients)

    if user["BMI"] == "under":
        lose_or_gain = "gain"
    elif user["BMI"] == "over":
        lose_or_gain = "lose"

    explanation += recipeA_name + "'s quantities of " + re.sub(r"(\w)([A-Z])", r"\1 \2", recipeA_nutr1).lower() \
                + " (" + str(recipeA[recipeA_nutr1]) \
                + " g) and " + re.sub(r"(\w)([A-Z])", r"\1 \2", recipeA_nutr2).lower() \
                + " (" + str(recipeA[recipeA_nutr2]) \
                + " g), among all nutrients in the recipe, are the closest to the respective recommended intakes (" \
                + str(round(nutrients[recipeA_nutr1]["RI"] * 0.4)) + " g and " + str(round(nutrients[recipeA_nutr2]["RI"] * 0.4)) + " g). "

    if user["BMI"] == "under" or user["BMI"] == "over":
        explanation += "A correct intake of such nutrients can help you to " + lose_or_gain + " weight. "

    if user["Mood"] == "bad" or user["Mood"] == "neutral" \
            or user["Depressed"] == "yes" or user["Stressed"] == "yes":

        listMood = ["sugars", "carbohydrates", "proteins"]
        closest_mood = list(set(recipeA_closest_to_RI) & set(listMood))

        if len(closest_mood) != 0:
            explanation += "Furthermore, " + recipeA_name + "'s intake of " + closest_mood[0]
            if len(closest_mood) == 2:
                explanation += " and " + closest_mood[1]
            explanation += " is good for your mood. "

    if recipeB is not None:
        recipeA_closestRI_sum = recipeA_nutr1 + recipeA_nutr2
        recipeB_closestRI_sum = recipeB_closest_to_RI[0] + recipeB_closest_to_RI[1]
        if recipeA_closestRI_sum < recipeB_closestRI_sum:
            explanation += "Also, " + recipeA_name + "'s nutrients closest to the recommended intake are closer than " \
                        + recipeB_name + "'s. "
        else:
            explanation += "On the other hand, " + recipeB_name + "'s nutrients closest to the recommended intake are closer than " \
                           + recipeA_name + "'s, which may be better for you. "

        explanation += compareCalories(recipeA_name, recipeB["title"], recipeA["calories"], recipeB["calories"])

    return explanation


"""
The userTime_one explanation function takes as input the user's preferred preparation time and a recipe.
It returns a comparison between the user's preference and the recipe's preparation time.
"""
def userTime_one(user_time, recipe_values):
    explanation = ""

    recipe_prepTime = int(re.findall(r'\d+', recipe_values['totalTime'])[0])

    if recipe_prepTime > user_time:
        compare = "longer than"
    elif recipe_prepTime < user_time:
        compare = "shorter than"
    else:
        compare = "equal to"

    # value 0 stands for 'no constraints'
    if user_time != 0:
        explanation = recipe_values['title'] + " takes " + str(recipe_prepTime) \
                      + " minutes as preparation time, which is " + compare + " the time you requested (" \
                      + str(user_time) + " minutes)."
    else:
        explanation = recipe_values['title'] + " takes " + str(recipe_prepTime) \
                      + " minutes as preparation time."
    return explanation


"""
The userTime_two explanation function takes as input the user's preferred preparation time and two recipes.
It returns a comparison between the recipes' preparation times.
"""
def userTime_two(user_time, recipeA_values, recipeB_values):
    explanation = ""

    recipeA_prepTime = int(re.findall(r'\d+', recipeA_values['totalTime'])[0])
    recipeB_prepTime = int(re.findall(r'\d+', recipeB_values['totalTime'])[0])



    if recipeA_prepTime < recipeB_prepTime:
        explanation = recipeA_values['title'] + " can be prepared in less time (" \
                      + str(recipeA_prepTime) + " minutes) than " + recipeB_values['title'] + " (" \
                      + str(recipeB_prepTime) + " minutes)"
    elif recipeA_prepTime > recipeB_prepTime:
        explanation = recipeA_values['title'] + " takes more preparation time (" \
                      + str(recipeA_prepTime) + " minutes) than " + recipeB_values['title'] + " (" \
                      + str(recipeB_prepTime) + " minutes)"
    else:  # same preparation time
        explanation = recipeA_values['title'] + " takes the same preparation time as " \
                      + recipeB_values['title'] + " (" + str(recipeA_prepTime) + " minutes)"

    if user_time != 0:
        diffA = abs(recipeA_prepTime - int(user_time))
        diffB = abs(recipeB_prepTime - int(user_time))
        explanation += ", and you prefer recipes that require a maximum of " \
                       + str(user_time) + " minutes of preparation time. "
        if diffA > diffB:
            explanation +=  recipeB_values['title'] + " seems closer to your time-frame."
        else:
            explanation +=  recipeA_values['title'] + " seems closer to your time-frame."
    else:
        explanation += "."
    

    return explanation


"""
The convertCost function takes as input
an Italian string for a recipe cost (molto basso, basso...) or a 1-4 value
and returns the corresponding number in a 1-4 scale and an English translation.
"""
def convertCost(cost):
    num = -1
    en = ""
    if cost == "Molto basso" or cost == 1:
        num = 1
        en = "very low"
    elif cost == "Basso" or cost == 2:
        num = 2
        en = "low"
    elif cost == "Medio" or cost == 3:
        num = 3
        en = "medium"
    elif cost == "Elevato" or cost == 4:
        num = 4
        en = "high"
    return num, en


"""
The userCosts_one explanation function takes as input the user's preference about cost and a recipe.
It returns a comparison between the user's preference and the recipe's cost.
"""
def userCosts_one(user_cost, recipe_values):
    explanation = ""
    recipe_cost_num, recipe_cost_en = convertCost(recipe_values['cost'])
    user_cost_num, user_cost_en = convertCost(user_cost)

    if recipe_cost_num != -1:
        # if the user cost is 5, it means that for the user the cost is not important,
        # so we show only the cost level of the recommended recipe
        if user_cost != 5:
            explanation = recipe_values['title'] + " has a " + recipe_cost_en + " cost level, "
            if recipe_cost_num > user_cost:
                explanation += "which is beyond your intended cost level (" + user_cost_en + ")."
            else:
                explanation += "in line with how much you intend to spend (" + user_cost_en + " cost level)."
        else:
            explanation = recipe_values['title'] + " has a " \
                          + recipe_cost_en + " cost level."
    return explanation


"""
The userCosts_two explanation function takes as input the user's preference about cost and two recipes.
It returns a comparison between the recipes' costs.
"""


def userCosts_two(user_cost, recipeA_values, recipeB_values):
    explanation = ""

    recipeA_cost_num, recipeA_cost_en = convertCost(recipeA_values['cost'])
    recipeB_cost_num, recipeB_cost_en = convertCost(recipeB_values['cost'])
    user_cost_num, user_cost_en = convertCost(user_cost)

    if recipeA_cost_num != -1 and recipeB_cost_num != -1:
        # if the user cost is 5, it means that for the user the cost is not important,
        # so we show only the cost level of the recommended recipe
        if recipeA_cost_num == recipeB_cost_num:
            explanation = recipeA_values['title'] + " has the same cost level of " \
                          + recipeB_values['title'] + " (" + recipeA_cost_en + ")"
        elif recipeA_cost_num > recipeB_cost_num:
            explanation = recipeA_values['title'] + " has an higher cost level (" + recipeA_cost_en + ") than " \
                          + recipeB_values['title'] + " (" + recipeB_cost_en + ")"
        else:
            explanation = recipeA_values['title'] + " has a lower cost level (" + recipeA_cost_en + ") than " \
                          + recipeB_values['title'] + " (" + recipeB_cost_en + ")"

        if user_cost != 5:
            explanation += ", and your preference on the level cost is " + user_cost_en + "."
        else:
            explanation += "."

    return explanation


"""
The rsa_score function computes a score that establishes how healthy a given recipe is according to the FSA guidelines.
"""
def rsa_score(recipe_values):
    # divide each value by 1.2 because in the dataset we have
    # the values per portion but the score is calculated per 100g
    score = 0.0
    # get all the recipe's nutrients
    fat = float(recipe_values['fat']) / 1.2
    saturated_fat = float(recipe_values['saturatedFat']) / 1.2
    sugar = float(recipe_values['sugars']) / 1.2
    # http://www.istitutodanone.it/novita-etichetta/sale-sodio-limportante-conoscere-differenza/ si moltiplica per 2.5 il sodio
    sodium = float(recipe_values['sodium']) / 1000
    sodium = sodium / 1.2
    salt = sodium * 2.5
    # FAT SCORE
    if fat <= 3.0:
        score += 1
    elif (fat > 3.0) and (fat <= 17.5):
        score += 2
    else:
        score += 3
    # SATURATED FAT SCORE
    if saturated_fat <= 1.5:
        score += 1
    elif (saturated_fat > 1.5) and (saturated_fat <= 5.0):
        score += 2
    else:
        score += 3
    # SUGAR SCORE
    if sugar <= 5.0:
        score += 1
    elif (sugar > 5.0) and (sugar <= 22.5):
        score += 2
    else:
        score += 3
    # SALT SCORE
    if salt <= 0.3:
        score += 1
    elif (salt > 0.3) and (salt <= 1.5):
        score += 2
    else:
        score += 3
    # TOTAL SCORE is a number between 4 (very healthy) to 12 (very unhealthy)
    return score


"""
This function converts a FSA score into a string and into a comparable number for the user lifestyle.
"""
def getScores(score):
    if score <= 5.6:
        score_level_str = "very healthy"
        score_level_num = 5
    elif (score > 5.6) and (score <= 7.2):
        score_level_str = "healthy"
        score_level_num = 4
    elif (score > 7.2) and (score <= 8.6):
        score_level_str = "average healthy"
        score_level_num = 3
    elif (score > 8.6) and (score <= 10.2):
        score_level_str = "unhealthy"
        score_level_num = 2
    else:
        score_level_str = "very unhealthy"
        score_level_num = 1
    return score_level_num, score_level_str


"""
The userLifestyle_one explanation function takes as input the user's desired lifestyle, his current condition and a recipe.
The getScores function is called on rsa_score and its output is then taken into account while comparing
the desired lifestyle and the current condition.
"""
def userLifestyle_one(user_health_lifestyle, user_health_condition, recipe_values):
    explanation = ""
    score_level_cmp, score_level_str = getScores(rsa_score(recipe_values))

    if user_health_lifestyle > user_health_condition:
        # user wants to improve the lifestyle
        explanation = "You want to improve your lifestyle, "
    elif user_health_lifestyle == user_health_condition:
        # user wants to maintain the lifestyle
        explanation = "You want to maintain your lifestyle, "
    # else: user wants a worse lifestyle. Since this can be an error, we don't show this in the string

    if score_level_cmp > user_health_condition:
        explanation += recipe_values['title'] + " allows you to have a better diet, because" \
                       + " it's a " + score_level_str + " recipe (according to FSA guidelines)."
    elif score_level_cmp == user_health_condition:
        explanation += recipe_values['title'] + " allows you to maintain your lifestyle, because" \
                       + " it's a " + score_level_str + " recipe (according to FSA guidelines). "
    else:
        explanation += "but " + recipe_values['title'] \
                       + " doesn't allow to maintain your lifestyle, because" \
                       + " it's a " + score_level_str + " recipe (according to FSA guidelines). " \
                       + "This recipe is less healthy than the ones you usually choose."

    return explanation


"""
The userLifestyle_two explanation function takes as input the user's current condition and two recipes.
The getScores function is called on rsa_score to obtain the recipes' healthiness scores,
which are then compared in relation to the user's condition.
"""
def userLifestyle_two(user_health_condition, recipeA_values, recipeB_values):
    explanation = ""
    scoreA_level_cmp, scoreA_level_str = getScores(rsa_score(recipeA_values))
    scoreB_level_cmp, scoreB_level_str = getScores(rsa_score(recipeB_values))

    if (scoreA_level_cmp > user_health_condition) or (scoreB_level_cmp > user_health_condition):
        str_equal = "Both recipes allow you to improve your lifestyle"
        str_different = "and can help you to improve your lifestyle."
    elif (scoreA_level_cmp == user_health_condition) or (scoreB_level_cmp == user_health_condition):
        str_equal = "Both recipes allow you to maintain your lifestyle"
        str_different = "and can help you to maintain your lifestyle."
    else:
        str_equal = "Both recipes make your lifestyle worse"
        str_different = "but both recipes make your lifestyle worse."

    if scoreA_level_cmp == scoreB_level_cmp:
        explanation = str_equal + ", since they are " + scoreA_level_str + " (according to FSA guidelines)."
    else:
        if scoreA_level_cmp > scoreB_level_cmp:
            # recipeA is better
            better = recipeA_values['title']
            worse = recipeB_values['title']
        else:
            # recipeB is better
            better = recipeB_values['title']
            worse = recipeA_values['title']

        explanation = better + " is healthier than " + worse + " (according to FSA guidelines) " + str_different

    return explanation


"""
The checkRecipeIngredientsInList function takes as input
a list of ingredients that satisfy certain properties
(e.g.: rich in specific nutrients, user's favourite, sustainable...)
and a recipe. The overlapping ingredients are returned.
"""
def checkRecipeIngredientsInList(ingredients, recipe_values):
    ingredients_found = []
    recipe_ingredients_str = recipe_values['ingredients']

    # clean string
    recipe_ingredients_str.translate({ord('['): None})
    recipe_ingredients_str.translate({ord(']'): None})
    recipe_ingredients_str.translate({ord('"'): None})
    recipe_ingredients = recipe_ingredients_str.split(',')  # array of ingredients

    # look for the given ingredients in the recipe
    for ingredient in ingredients:
        for recipe_ingredient in recipe_ingredients:
            recipe_ingredient_clean = "".join([c if c.isalnum() else "" for c in recipe_ingredient.lower()])
            ingredient_clean = "".join([c if c.isalnum() else "" for c in ingredient.lower()])
            if recipe_ingredient_clean == ingredient_clean \
                    or recipe_ingredient_clean + "s" == ingredient_clean \
                    or recipe_ingredient_clean == ingredient_clean + "s" \
                    or recipe_ingredient_clean + "es" == ingredient_clean \
                    or recipe_ingredient_clean == ingredient_clean + "es":
                ingredients_found.append(ingredient)

    # remove duplicates
    ingredients_found = list(dict.fromkeys(ingredients_found))

    # remove empty strings
    if "" in ingredients_found:
        ingredients_found.remove("")
    if "" in ingredients_found:
        ingredients_found.remove("")

    return ingredients_found


"""
The listFavIngredientsInRecipe function is used in userIngredients_one and userIngredients_two
to show a list of the user's favourite ingredients contained in a given recipe.
"""
def listFavIngredientsInRecipe(favIngredientsInRecipe, recipe_values):
    explanation = ""
    if len(favIngredientsInRecipe) == 1:
        explanation = recipe_values['title'] + " is prepared with " + favIngredientsInRecipe[0] \
                      + ", which is one of your favourite ingredients"
    else:
        explanation = recipe_values['title'] + " is prepared with "
        # concatenate list of ingredients separated by ',' to the explanation
        explanation += str(reduce(lambda x, y: x + ", " + y, favIngredientsInRecipe))
        explanation += " which are some of your favourite ingredients"

    return explanation


"""
The userIngredients_one explanation function checks if a given recipe contains the user's favourite 
ingredients. If any of them are present, it provides an explanation that lists them.
The list of favourite ingredients contained in the recipe is also returned.
"""
def userIngredients_one(user_ingredients, recipe_values):
    explanation = ""
    favIngredientsInRecipe = checkRecipeIngredientsInList(user_ingredients, recipe_values)

    if len(favIngredientsInRecipe) > 0:
        explanation = listFavIngredientsInRecipe(favIngredientsInRecipe, recipe_values) + "."
    else:
        explanation = recipe_values['title'] + " does not contain any of your favourite ingredients."

    return explanation, favIngredientsInRecipe


"""
The userIngredients_two explanation function checks if two given recipes contain the user's favourite 
ingredients. If any of them are present, it provides an explanation that lists them and compares
the recipes. The list of favourite ingredients contained in the recipes are also returned.
"""
def userIngredients_two(user_ingredients, recipeA_values, recipeB_values):
    explanation = ""

    favIngredientsInRecipeA = checkRecipeIngredientsInList(user_ingredients, recipeA_values)
    favIngredientsInRecipeB = checkRecipeIngredientsInList(user_ingredients, recipeB_values)

    if (len(favIngredientsInRecipeA) > 0) or (len(favIngredientsInRecipeB) > 0):

        if len(favIngredientsInRecipeB) == 0:
            # recipe B doesn't contain any fav ingredient
            explanation = listFavIngredientsInRecipe(favIngredientsInRecipeA, recipeA_values) \
                          + ", compared to " + recipeB_values['title'] \
                          + " which doesn't contain any favourite ingredients."
        elif len(favIngredientsInRecipeA) == 0:
            # recipe A doesn't contain any fav ingredient
            explanation = listFavIngredientsInRecipe(favIngredientsInRecipeB, recipeB_values) \
                          + ", compared to " + recipeA_values['title'] \
                          + " which doesn't contain any favourite ingredients."
        else:
            # both recipes contain some fav ingredients
            explanation = listFavIngredientsInRecipe(favIngredientsInRecipeA, recipeA_values) \
                          + ". On the other hand, " \
                          + listFavIngredientsInRecipe(favIngredientsInRecipeB, recipeB_values) + "."

    else:
        explanation = "Both recipes don't contain any of your favourite ingredients."

    return explanation, favIngredientsInRecipeA, favIngredientsInRecipeB


"""
The convertAge function takes the user's age as input.
If it is numeric, it is converted into a range ("U20","U30"...)
that is compatible with the userAge_one and userAge_two functions.
"""
def convertAge(user_age):
    if user_age.isnumeric():
        if int(user_age) < 20:
            user_age = "U20"
        elif int(user_age) < 30:
            user_age = "U30"
        elif int(user_age) < 40:
            user_age = "U40"
        elif int(user_age) < 50:
            user_age = "U50"
        elif int(user_age) < 60:
            user_age = "U60"
        else:
            user_age = "O60"
    return user_age


"""
The userAge_one explanation function evaluates if ingredients that are rich in specific nutrients
(depending on the user's age group) are present in a given recipe. An explanation of
the nutrients needed in the specific age group is also provided.
"""
def userAge_one(user_age, recipe_values, richIn):
    explanation = ""
    present_list = []
    lacking_list = []

    user_age = convertAge(user_age)

    # we build sets of ingredients with certain characteristics (for example rich in calcium) to evaluate
    # if the recipes contain them
    # from https://www.myfooddata.com/articles/foods-high-in-calcium.php
    # from https://www.myfooddata.com/articles/food-sources-of-iron.php
    # from https://www.myfooddata.com/articles/foods-high-in-magnesium.php#magnesium-rich-foods-list
    # to evaluate whether an ingredient is antioxidant, it is necessary to evaluate whether it contains
    # elements that are. The main antioxidants in foods are lycopene and beta carotene.
    # from https://www.myfooddata.com/articles/high-lycopene-foods.php
    # from https://www.myfooddata.com/articles/natural-food-sources-of-beta-carotene.php
    # from https://www.myfooddata.com/articles/vitamin-c-foods.php
    # from https://www.myfooddata.com/articles/vitamin-e-foods.php
    # from https://www.myfooddata.com/articles/high-vitamin-D-foods.php

    if user_age == 'U20' or user_age == 'U30':
        # in this age group we want recipes that contain ingredients rich in calcium and iron
        calciumIngredientsInRecipe = checkRecipeIngredientsInList(richIn['richIn']['calcium'], recipe_values)
        ironIngredientsInRecipe = checkRecipeIngredientsInList(richIn['richIn']['iron'], recipe_values)

        if len(calciumIngredientsInRecipe) > 0:
            present_list.append("calcium")
        else:
            lacking_list.append("calcium")

        if len(ironIngredientsInRecipe) > 0:
            present_list.append("iron")
        else:
            lacking_list.append("iron")

    elif user_age == 'U40':
        # in this age group we want recipes that contain ingredients rich in magnesium
        magnesiumIngredientsInRecipe = checkRecipeIngredientsInList(richIn['richIn']['magnesium'], recipe_values)

        if len(magnesiumIngredientsInRecipe) > 0:
            present_list.append("magnesium")
        else:
            lacking_list.append("magnesium")

    elif user_age == 'U50':
        # in this age group we want recipes that contain ingredients rich in vitamin C and E, and antioxidants
        antioxidantIngredientsInRecipe = checkRecipeIngredientsInList(richIn['richIn']['antioxidant'], recipe_values)
        vitaminCIngredientsInRecipe = checkRecipeIngredientsInList(richIn['richIn']['vitaminC'], recipe_values)
        vitaminEIngredientsInRecipe = checkRecipeIngredientsInList(richIn['richIn']['vitaminE'], recipe_values)

        if len(antioxidantIngredientsInRecipe) > 0:
            present_list.append("antioxidants")
        else:
            lacking_list.append("antioxidants")

        if len(vitaminCIngredientsInRecipe) > 0:
            present_list.append("vitamin C")
        else:
            lacking_list.append("vitamin C")

        if len(vitaminEIngredientsInRecipe) > 0:
            present_list.append("vitamin E")
        else:
            lacking_list.append("vitamin E")

    elif (user_age == 'U60') or (user_age == 'O60'):
        # in this age group we want recipes that contain ingredients rich in calcium and vitamin D
        calciumIngredientsInRecipe = checkRecipeIngredientsInList(richIn['richIn']['calcium'], recipe_values)
        vitaminDIngredientsInRecipe = checkRecipeIngredientsInList(richIn['richIn']['vitaminD'], recipe_values)

        if len(calciumIngredientsInRecipe) > 0:
            present_list.append("calcium")
        else:
            lacking_list.append("calcium")

        if len(vitaminDIngredientsInRecipe) > 0:
            present_list.append("vitamin D")
        else:
            lacking_list.append("vitamin D")

    if user_age in ['U20', 'U30', 'U40', 'U50', 'U60', 'O60']:
        explanation += richIn['motivation'][user_age][:-1] + "; "
        if present_list:
            explanation += recipe_values['title'].lower() + " contains "
            i = 0
            for item in present_list:
                explanation += item
                i += 1
                if i != len(present_list):
                    explanation += " and "
        if lacking_list:
            if present_list:
                explanation += ", but it lacks "
            else:
                explanation += recipe_values['title'].lower() + " lacks "
            i = 0
            for item in lacking_list:
                explanation += item
                i += 1
                if i != len(lacking_list):
                    explanation += " and "
        explanation += "."

    explanation = explanation.replace('[', '')
    explanation = explanation.replace(']', '')

    return explanation


"""
The userAge_two explanation function calls the userAge_one function on two recipes.
"""
def userAge_two(user_age, recipeA_values, recipeB_values, richIn):
    explanation = ""

    user_age = convertAge(user_age)

    explA = userAge_one(user_age, recipeA_values, richIn)
    explB = userAge_one(user_age, recipeB_values, richIn).replace(richIn["motivation"][user_age][:-1], "")

    explanation += explA + " On the other hand, " + explB[2:]

    return explanation


"""
The ingredientsSustainability_one explanation function
returns a string that lists the ingredients with high and low sustainability
that are present in a given recipe, as well as the respective lists.
"""
def ingredientsSustainability_one(recipe, sustainability):
    explanation = ""

    highSustainabilityList = sustainability["highSustainability"]["CFP"] + sustainability["highSustainability"]["WFP"]
    lowSustainabilityList = sustainability["lowSustainability"]["CFP"] + sustainability["lowSustainability"]["WFP"]

    recipe_sustainable = checkRecipeIngredientsInList(highSustainabilityList, recipe)
    recipe_notSustainable = checkRecipeIngredientsInList(lowSustainabilityList, recipe)

    if recipe_sustainable:
        has_or_have = "has"
        explanation += recipe["title"] + " contains " + recipe_sustainable[0]
        if len(recipe_sustainable) > 1:
            has_or_have = "have"
            for i in range(1, len(recipe_sustainable)):
                explanation += " and " + recipe_sustainable[i]
        explanation += ", which " + has_or_have + " high carbon/water footprint sustainability."

        if recipe_notSustainable:
            explanation += " On the other hand, "

    if recipe_notSustainable:
        has_or_have = "has"
        explanation += recipe["title"] + " contains " + recipe_notSustainable[0]
        if len(recipe_notSustainable) > 1:
            has_or_have = "have"
            for i in range(1, len(recipe_notSustainable)):
                explanation += " and " + recipe_notSustainable[i]
        explanation += ", which " + has_or_have + " low carbon/water footprint sustainability."

    if not recipe_sustainable and not recipe_notSustainable:
        explanation += recipe["title"] + \
                       " contains no ingredient that has either high or low carbon/water footprint sustainability."

    return explanation, recipe_sustainable, recipe_notSustainable


"""
The ingredientsSustainability_two explanation function
calls ingredientsSustainability_one on two recipes and then
compares the quantity of ingredients with high and low sustainability between the recipes.
It also returns the lists of ingredients with high and low sustainability for both recipes.
"""
def ingredientsSustainability_two(recipeA, recipeB, sustainability):
    explanation = ""

    recipeA_name = recipeA["title"]
    recipeB_name = recipeB["title"]

    explA, recipeA_sustainable, recipeA_notSustainable = ingredientsSustainability_one(recipeA, sustainability)
    explB, recipeB_sustainable, recipeB_notSustainable = ingredientsSustainability_one(recipeB, sustainability)

    explanation = explA + " " + explB + " "

    if recipeA_sustainable or recipeB_sustainable:
        if len(recipeA_sustainable) > len(recipeB_sustainable):
            explanation += recipeA_name + " has more ingredients with high sustainability than " + recipeB_name + "."
        elif len(recipeA_sustainable) < len(recipeB_sustainable):
            explanation += recipeA_name + " has less ingredients with high sustainability than " + recipeB_name + "."
        else:
            explanation += "Both recipes have the same amount of ingredients with high sustainability."

        if recipeA_notSustainable or recipeB_notSustainable:
            explanation += " On the other hand, "

    if recipeA_notSustainable or recipeB_notSustainable:
        if len(recipeA_notSustainable) > len(recipeB_notSustainable):
            explanation += recipeA_name + " has more ingredients with low sustainability than " + recipeB_name + "."
        elif len(recipeA_notSustainable) < len(recipeB_notSustainable):
            explanation += recipeA_name + " has less ingredients with low sustainability than " + recipeB_name + "."
        else:
            explanation += "Both recipes have the same amount of ingredients with low sustainability."

    return explanation, recipeA_sustainable, recipeA_notSustainable, recipeB_sustainable, recipeB_notSustainable


"""
The ingredientsSeasonality_one explanation function
checks if a given recipe contains ingredients that are in season
compared to a specified season ("winter", "spring", "summer" or "autumn").
If the season is specified as a number (1-4), it is converted into a string.
If the season is not specified at all, it is extracted from the current date.
A list containing the recipe's seasonal ingredients is also returned.
"""
def ingredientsSeasonality_one(recipe, season, seasonality):
    explanation = ""

    if season is None or season == "":
        now = datetime.now()
        season = now.month % 12 // 3 + 1

    if season == 1:
        season = "winter"
    elif season == 2:
        season = "spring"
    elif season == 3:
        season = "summer"
    elif season == 4:
        season = "autumn"

    recipe_seasonal = checkRecipeIngredientsInList(seasonality[season], recipe)

    if recipe_seasonal:
        is_or_are = "is"
        explanation += recipe["title"] + " contains " + recipe_seasonal[0]
        if len(recipe_seasonal) > 1:
            is_or_are = "are"
            for i in range(1, len(recipe_seasonal)):
                explanation += " and " + recipe_seasonal[i]
        explanation += ", which " + is_or_are + " in season in " + season + "."

    else:
        explanation += recipe["title"] + \
                       " contains no ingredient that is in season in " + season + "."

    return explanation, recipe_seasonal


"""
The ingredientsSeasonality_two explanation function
calls ingredientsSeasonality_one on two recipes and then
compares the quantity of seasonal ingredients between the recipes.
It also returns the lists of seasonal ingredients for both recipes.
"""

def ingredientsSeasonality_two(recipeA, recipeB, season, seasonality):
    explanation = ""

    recipeA_name = recipeA["title"]
    recipeB_name = recipeB["title"]

    explA, recipeA_seasonal = ingredientsSeasonality_one(recipeA, season, seasonality)
    explB, recipeB_seasonal = ingredientsSeasonality_one(recipeB, season, seasonality)

    explanation = explA + " On the other hand, " + explB + " "

    if len(recipeA_seasonal) > len(recipeB_seasonal):
        explanation += recipeA_name + " has more seasonal ingredients than " + recipeB_name + "."
    elif len(recipeA_seasonal) < len(recipeB_seasonal):
        explanation += recipeA_name + " has less seasonal ingredients than " + recipeB_name + "."
    elif len(recipeA_seasonal) != 0:
        explanation += "Both recipes have the same amount of seasonal ingredients."

    return explanation, recipeA_seasonal, recipeB_seasonal


"""
The ingredientsDopamine_one explanation function
checks if a given recipe contains ingredients that enhance dopamine production.
A list containing the recipe's dopamine-inducing ingredients is also returned.
"""
def ingredientsDopamine_one(recipe, dopamine):
    explanation = ""

    recipe_dopamine = checkRecipeIngredientsInList(dopamine["dopamine"], recipe)

    if recipe_dopamine:
        explanation += recipe["title"] + " contains " + recipe_dopamine[0]
        if len(recipe_dopamine) > 1:
            for i in range(1, len(recipe_dopamine)):
                explanation += " and " + recipe_dopamine[i]
        explanation += ", which enhances"
        if len(recipe_dopamine) > 1:
            explanation = explanation[:-1]
        explanation += " dopamine production. "

    else:
        explanation += recipe["title"] + \
                       " contains no ingredient that enhances dopamine production. "

    explanation += dopamine["motivation"]

    return explanation, recipe_dopamine


"""
The ingredientsDopamine_two explanation function
calls ingredientsDopamine_one on two recipes and then
compares the quantity of dopamine-inducing ingredients between the recipes.
It also returns the lists of dopamine-inducing ingredients for both recipes.
"""
def ingredientsDopamine_two(recipeA, recipeB, dopamine):
    explanation = ""

    recipeA_name = recipeA["title"]
    recipeB_name = recipeB["title"]

    explA, recipeA_dopamine = ingredientsDopamine_one(recipeA, dopamine)
    explA = explA.replace(dopamine["motivation"], "")

    explB, recipeB_dopamine = ingredientsDopamine_one(recipeB, dopamine)

    explanation = explA + "On the other hand, " + explB + " "

    if len(recipeA_dopamine) > len(recipeB_dopamine):
        explanation += recipeA_name + " has more dopamine-inducing ingredients than " + recipeB_name + "."
    elif len(recipeA_dopamine) < len(recipeB_dopamine):
        explanation += recipeA_name + " has less dopamine-inducing ingredients than " + recipeB_name + "."
    elif len(recipeA_dopamine) != 0:
        explanation += "Both recipes have the same amount of dopamine-inducing ingredients."

    return explanation, recipeA_dopamine, recipeB_dopamine


"""
The smartExplanation explanation function provides a personalized explanation
for one or two recipes based on various user characteristics.
"""
def smartExplanation(user, recipeA, recipeB, listRestrictions, nutrients, restrictions, richIn, sustainability, seasonality, dopamine):
    explanation = ""
    explanationDone_flag = 0

    if recipeB is None:
        expl = foodPreferences_one(user["User_restriction"], listRestrictions, restrictions, recipeA)
    else:
        expl = foodPreferences_two(user["User_restriction"], listRestrictions, restrictions, recipeA, recipeB)
    if expl != -1 and expl != -2:
        explanation += expl

    if user["Goal"] == "lose" or user["Goal"] == "gain":
        explanationDone_flag = 1
        if user["Mood"] == "bad" or user["Depressed"] == "yes" or user["Stressed"] == "yes":
            explanation += userFeatureHealthBenefits(user, recipeA, recipeB, nutrients)
        else:
            if user["Sex"] is None:
                explanation += userFeatureHealthRisk(user, recipeA, recipeB, nutrients)
                if recipeB is None: #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    explanation += foodMacros_one(recipeA, user)
                else:
                    explanation += foodMacros_two(recipeA, recipeB, user)
            else:
                if user["Activity"] == "low" or user["Activity"] == "high" or user["Activity"] == "normal": #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    if recipeB is None:
                        explanation += foodGoals_one(recipeA, user)
                    else:
                        explanation += foodGoals_two(recipeA, recipeB, user)   
                

        if user["Health_style"] is not None and user["Health_condition"] is not None:
            if (int(user["Health_style"]) - int(user["Health_condition"]) >= 2) and (int(user["Health_condition"]) <= 2):
                if recipeB is None:
                    explanation += userAge_one(user["Age"], recipeA, richIn)
                else:
                    explanation += userAge_two(user["Age"], recipeA, recipeB, richIn)

    else:
        if user["Health_style"] is not None and user["Health_condition"] is not None:
            if int(user["Health_style"]) - int(user["Health_condition"]) >= 2:
                explanationDone_flag = 1
                if user["Mood"] == "bad" or user["Depressed"] == "yes" or user["Stressed"] == "yes":
                    explanation += foodFeatureHealthRiskBenefit(recipeA, recipeB, nutrients, "benefits")
                else:
                    explanation += foodFeatureHealthRiskBenefit(recipeA, recipeB, nutrients, "risks")
                if recipeB is None:
                    explanation += userAge_one(user["Age"], recipeA, richIn)
                else:
                    explanation += userAge_two(user["Age"], recipeA, recipeB, richIn)

        if explanationDone_flag == 0 and user["Health_condition"] is not None:
            if int(user["Health_condition"]) <= 2:
                explanationDone_flag = 1
                explanation += foodFeatureHealthRiskBenefit(recipeA, recipeB, nutrients, "benefits")
                if recipeB is None:
                    explanation += userAge_one(user["Age"], recipeA, richIn)
                else:
                    explanation += userAge_two(user["Age"], recipeA, recipeB, richIn)

        elif user["Mood"] == "bad" or user["Depressed"] == "yes" or user["Stressed"] == "yes" or user["Sleep"] == "low":
            if recipeB is None:
                expl, dopamine = ingredientsDopamine_one(recipeA, dopamine)
                if dopamine:
                    explanationDone_flag = 1
                    explanation += expl
            else:
                expl, dopamineA, dopamineB = ingredientsDopamine_two(recipeA, recipeB, dopamine)
                if dopamineA or dopamineB:
                    explanationDone_flag = 1
                    explanation += expl

        if explanationDone_flag == 0 and user["User_ingredients"] != None:
            user_ingredients = user["User_ingredients"].split(",")
            if recipeB is None:
                expl, favInRecipe = userIngredients_one(user_ingredients, recipeA)
                if favInRecipe:
                    explanationDone_flag = 1
                    explanation += expl
            else:
                expl, favInRecipeA, favInRecipeB = userIngredients_two(user_ingredients, recipeA, recipeB)
                if favInRecipeA or favInRecipeB:
                    explanationDone_flag = 1
                    explanation += expl

        if explanationDone_flag == 0:

            if user["Cooking_exp"] is not None:
                if int(user["Cooking_exp"]) != 5:
                    explanationDone_flag = 1
                    if recipeB is None:
                        explanation += userSkills_one(int(user["Cooking_exp"]), recipeA)
                    else:
                        explanation += userSkills_two(int(user["Cooking_exp"]), recipeA, recipeB)

            if explanationDone_flag == 0 and user["User_time"] is not None:
                if int(user["User_time"]) != 0:
                    explanationDone_flag = 1
                    if recipeB is None:
                        explanation += userTime_one(int(user["User_time"]), recipeA)
                    else:
                        explanation += userTime_two(int(user["User_time"]), recipeA, recipeB)

            if explanationDone_flag == 0 and user["User_cost"] is not None:
                if int(user["User_cost"]) != 5:
                    explanationDone_flag = 1
                    if recipeB is None:
                        explanation += userCosts_one(int(user["User_cost"]), recipeA)
                    else:
                        explanation += userCosts_two(int(user["User_cost"]), recipeA, recipeB)

            if explanationDone_flag == 0:

                if recipeB is None:
                    sust_expl, sustA, notSustA = ingredientsSustainability_one(recipeA, sustainability)
                    if sustA or notSustA:
                        explanationDone_flag = 1
                        explanation += sust_expl
                else:
                    sust_expl, sustA, notSustA, sustB, notSustB = ingredientsSustainability_two(recipeA, recipeB, sustainability)
                    if sustA or notSustA or sustB or notSustB:
                        explanationDone_flag = 1
                        explanation += sust_expl

                if explanationDone_flag == 0:
                    if recipeB is None:
                        seas_expl, seasA = ingredientsSeasonality_one(recipeA, user["Season"], seasonality)
                        if seasA:
                            explanationDone_flag = 1
                            explanation += seas_expl
                    else:
                        seas_expl, seasA, seasB = ingredientsSeasonality_two(recipeA, recipeB, user["Season"], seasonality)
                        if seasA or seasB:
                            explanationDone_flag = 1
                            explanation += seas_expl

                if explanationDone_flag == 0:
                    explanation += recipeA["description"]

                    if recipeB is not None:
                        explanation += recipeB["description"]
                        explanation += popularity_two(recipeA, recipeB)
                    else:
                        explanation += popularity_one(recipeA)

    return explanation


"""
The get_str_exp function returns an explanation of a given type
(popularity, food features, user features, ecc...)
"""
def get_str_exp(user,
                recipeA_values,
                recipeB_values,
                type_explanation,
                listRestrictions,
                nutrients,
                restrictions,
                richIn,
                sustainability,
                seasonality,
                dopamine):
    global description
    expl = ""

    recipeA_name = recipeA_values['title']
    if recipeB_values is not None:
        recipeB_name = recipeB_values['title']

    # TYPE: popularity
    if type_explanation == 'popularity_one':
        expl = popularity_one(recipeA_values)
    elif type_explanation == 'popularity_two':
        expl = popularity_two(recipeA_values, recipeB_values)

    # TYPE: foodGoals
    elif type_explanation == 'foodGoals_one':
        expl = foodGoals_one(recipeA_values, user)
    elif type_explanation == 'foodGoals_two':
        expl = foodGoals_two(recipeA_values, recipeB_values, user)

    # TYPE: foodPreferences
    elif type_explanation == 'foodPreferences_one' or type_explanation == 'foodPreferences_two':
        userRestrictions = user["User_restriction"]

        if type_explanation == 'foodPreferences_one':
            expl = foodPreferences_one(userRestrictions, listRestrictions, restrictions, recipeA_values)
        elif type_explanation == 'foodPreferences_two':
            expl = foodPreferences_two(userRestrictions, listRestrictions, restrictions, recipeA_values, recipeB_values)

        if expl == -1:
            expl = "No user restrictions were specified. " \
                   "Compatible user restrictions: vegetarian, lactose-free, gluten-free, low-nichel, light."
        elif expl == -2:
            expl = "No compatible user restrictions were specified. " \
                   "Compatible user restrictions: vegetarian, lactose-free, gluten-free, low-nichel, light."

    # TYPE: foodFeatures
    elif type_explanation == 'foodFeatures_one':
        expl, _, _ = foodFeatures(recipeA_values, None, nutrients)
    elif type_explanation == 'foodFeatures_two':
        expl, _, _ = foodFeatures(recipeA_values, recipeB_values, nutrients)

    # TYPE: userSkills
    elif type_explanation == 'userSkills_one' or type_explanation == 'userSkills_two':
        if user["Cooking_exp"] is None or user["Cooking_exp"] == "":
            expl = "No cooking experience was specified. Possible values: 1-5"
        elif not user["Cooking_exp"].isnumeric():
            expl = "The specified cooking experience is not numeric. Possible values: 1-5"
        elif type_explanation == 'userSkills_one':
            expl = userSkills_one(int(user['Cooking_exp']), recipeA_values)
        elif type_explanation == 'userSkills_two':
            expl = userSkills_two(int(user['Cooking_exp']), recipeA_values, recipeB_values)

    # TYPE: foodFeatureHealthRisk
    elif type_explanation == 'foodFeatureHealthRisk_one':
        expl = foodFeatureHealthRiskBenefit(recipeA_values, None, nutrients, "risks")
    elif type_explanation == 'foodFeatureHealthRisk_two':
        expl = foodFeatureHealthRiskBenefit(recipeA_values, recipeB_values, nutrients, "risks")

    # TYPE: foodFeatureHealthBenefits
    elif type_explanation == 'foodFeatureHealthBenefits_one':
        expl = foodFeatureHealthRiskBenefit(recipeA_values, None, nutrients, "benefits")
    elif type_explanation == 'foodFeatureHealthBenefits_two':
        expl = foodFeatureHealthRiskBenefit(recipeA_values, recipeB_values, nutrients, "benefits")

    # TYPE: userFeatureHealthRisk
    elif type_explanation == 'userFeatureHealthRisk_one':
        expl = userFeatureHealthRisk(user, recipeA_values, None, nutrients)
    elif type_explanation == 'userFeatureHealthRisk_two':
        expl = userFeatureHealthRisk(user, recipeA_values, recipeB_values, nutrients)

    # TYPE: userFeatureHealthBenefits
    elif type_explanation == 'userFeatureHealthBenefits_one':
        expl = userFeatureHealthBenefits(user, recipeA_values, None, nutrients)
    elif type_explanation == 'userFeatureHealthBenefits_two':
        expl = userFeatureHealthBenefits(user, recipeA_values, recipeB_values, nutrients)

    # TYPE: userTime
    elif type_explanation == "userTime_one" or type_explanation == "userTime_two":
        if user["User_time"] is None or user["User_time"] == "":
            user["User_time"] = "0"

        if not user["User_time"].isnumeric():
            expl = "The specified user time is not numeric. Possible values: [1,200] mins. 0 stands for 'no costraints'."
        else:
            if type_explanation == 'userTime_one':
                expl = userTime_one(int(user['User_time']), recipeA_values)
            elif type_explanation == 'userTime_two':
                expl = userTime_two(int(user['User_time']), recipeA_values, recipeB_values)

    # TYPE: userCosts
    elif type_explanation == 'userCosts_one' or type_explanation == 'userCosts_two':
        if user["User_cost"] is None or user["User_cost"] == "":
            user["User_cost"] = "5"

        if not user["User_cost"].isnumeric():
            expl = "The specified user cost is not numeric. Possible values: 1-5. 5 stands for 'not important'."
        else:
            if type_explanation == 'userCosts_one':
                if recipeA_values['cost'] == "":
                    expl = recipeA_name + "'s cost is unknown."
                else:
                    expl = userCosts_one(int(user['User_cost']), recipeA_values)

            elif type_explanation == 'userCosts_two':
                if recipeA_values['cost'] == "" or recipeB_values['cost'] == "":
                    if recipeA_values['cost'] == "":
                        expl = recipeA_name + "'s cost is unknown. "
                    if recipeB_values['cost'] == "":
                        expl += recipeB_name + "'s cost is unknown."
                else:
                    expl = userCosts_two(int(user['User_cost']), recipeA_values, recipeB_values)

    # TYPE: userLifestyle
    elif type_explanation == 'userLifestyle_one' or type_explanation == 'userLifestyle_two':
        if user["Health_style"] is None or user["Health_style"] == "" \
                    or user["Health_condition"] is None or user["Health_condition"] == "":

            if user["Health_style"] is None or user["Health_style"] == "":
                expl = "No user health style was specified. Possible values: 1-5."
            elif not user["Health_style"].isnumeric():
                expl = "The specified user health style is not numeric. Possible values: 1-5."

            if user["Health_condition"] is None or user["Health_condition"] == "":
                expl += "No user health condition was specified. Possible values: 1-5."
            elif not user["Health_condition"].isnumeric():
                expl += "The specified user health condition is not numeric. Possible values: 1-5."

        elif not user["Health_style"].isnumeric() or not user["Health_condition"].isnumeric():
            if not user["Health_style"].isnumeric():
                expl += "The specified user health style is not numeric. Possible values: 1-5."

            if not user["Health_condition"].isnumeric():
                expl += "The specified user health condition is not numeric. Possible values: 1-5."

        elif type_explanation == 'userLifestyle_one':
            expl = userLifestyle_one(int(user['Health_style']), int(user['Health_condition']), recipeA_values)
        elif type_explanation == 'userLifestyle_two':
            expl = userLifestyle_two(int(user['Health_condition']),
                                         recipeA_values, recipeB_values)

    # TYPE: userIngredients
    elif type_explanation == 'userIngredients_one' or type_explanation == 'userIngredients_two':
        user_ingredients = user['User_ingredients']
        if user_ingredients is None or user_ingredients == "" or user_ingredients.isnumeric():
            expl = "No favourite ingredients were specified."
        else:
            user_ingredients = user_ingredients.split(",")
            if type_explanation == 'userIngredients_one':
                expl, _ = userIngredients_one(user_ingredients, recipeA_values)
            elif type_explanation == 'userIngredients_two':
                expl, _, _ = userIngredients_two(user_ingredients, recipeA_values, recipeB_values)

    # TYPE: userAge
    elif type_explanation == 'userAge_one' or type_explanation == 'userAge_two':
        if user['Age'] is None or user['Age'] == "":
            expl = "The user age was not specified."
        elif user["Age"] not in ["U20", "U30", "U40", "U50", "U60", "O60"] and not user["Age"].isnumeric():
            expl = "The specified user age is not valid. Possible values: a numeric value or U20,U30,U40,U50,U60,O60."

        elif type_explanation == 'userAge_one':
            expl = userAge_one(user['Age'], recipeA_values, richIn)
        elif type_explanation == 'userAge_two':
            expl = userAge_two(user['Age'], recipeA_values, recipeB_values, richIn)

    # TYPE: sustainability
    elif type_explanation == 'ingredientsSustainability_one':
        expl, _, _ = ingredientsSustainability_one(recipeA_values, sustainability)
    elif type_explanation == 'ingredientsSustainability_two':
        expl, _, _, _, _ = ingredientsSustainability_two(recipeA_values, recipeB_values, sustainability)

    # TYPE: seasonality
    elif type_explanation == 'ingredientsSeasonality_one':
        expl, _ = ingredientsSeasonality_one(recipeA_values, user["Season"], seasonality)
    elif type_explanation == 'ingredientsSeasonality_two':
        expl, _, _ = ingredientsSeasonality_two(recipeA_values, recipeB_values, user["Season"], seasonality)

    # TYPE: dopamine
    elif type_explanation == 'ingredientsDopamine_one':
        expl, _ = ingredientsDopamine_one(recipeA_values, dopamine)
    elif type_explanation == 'ingredientsDopamine_two':
        expl, _, _ = ingredientsDopamine_two(recipeA_values, recipeB_values, dopamine)

    # TYPE: description
    elif type_explanation == 'description' or type_explanation == 'descriptions':
        if recipeA_values['description'] != "":
            expl = recipeA_values['description']
        if type_explanation == 'descriptions' and recipeB_values['description'] != "":
            expl += recipeB_values['description']

    # TYPE: smartExplanation
    elif type_explanation == 'smartExplanation_one' or type_explanation == 'smartExplanation_two':
        expl += smartExplanation(user, recipeA_values, recipeB_values, listRestrictions, nutrients, restrictions, \
                                 richIn, sustainability, seasonality, dopamine)

    # TYPE: foodMacros   
    elif type_explanation == 'foodMacros_one':
        expl, _ = foodMacros_one(recipeA_values, user)
    elif type_explanation == 'foodMacros_two':
        expl = foodMacros_two(recipeA_values, recipeB_values, user)

    return expl

"""
The foodMacros_one function 
checks if the recipe's macronutrient distribution deviates from an ideal ratio (50-20-30) adjusted based on sex and activity.
    - ideal_macros["carbs"] / 100                           -> converts the percentage value of the ideal carbs distribution to a decimal.
    - total_recipe_macros                                   -> sum of the actual values of carbs, fats, and proteins in the recipe. 
    - total_recipe_macros * (ideal_macros["carbs"] / 100)   -> calculates the amount of carbs that would be present in the recipe if it perfectly matched the ideal distribution(%).                                                        
    - recipe_macros["carbs"] - (total_recipe_macros * (ideal_macros["carbs"] / 100)) ->
        subtracts the expected amount of carbs from the actual amount of carbs in the recipe. 
        The result is the deviation, representing how much the actual carbs content deviates from what is expected based on the ideal distribution.
"""
def foodMacros_one(recipe, user):
    explanation = ""
    recipe_macros = {
        "carbs": recipe["carbohydrates"],
        "fats": recipe["fat"],
        "proteins": recipe["proteins"],
    }
    
    user_sex = user["Sex"]
    user_activity = user["Activity"]

    explanation = recipe["title"] + " has the following macronutrient distribution: "
    explanation += f"{recipe_macros['carbs']}g of carbs, {recipe_macros['fats']}g of fats, and {recipe_macros['proteins']}g of proteins. "

    # Ideal macronutrient distribution (50%-20%-30%)
    ideal_macros_distribution = {"carbs": 50, "fats": 20, "proteins": 30} #fonte

    if user_sex is None or user_sex == "":
        ideal_macros = {
            "carbs": ideal_macros_distribution["carbs"],
            "fats": ideal_macros_distribution["fats"],
            "proteins": ideal_macros_distribution["proteins"]
        }
        man_or_woman = "person of unspecified sex"
    else:
        ideal_macros = {
            "carbs": ideal_macros_distribution["carbs"],
            "fats": ideal_macros_distribution["fats"],
            "proteins": ideal_macros_distribution["proteins"]
        }
        man_or_woman = "man" if user_sex == "m" else "woman"

    # Is this useful in this kind of explanation? 
    if user_activity == 'low':
        ideal_macros["carbs"] += 5
        ideal_macros["fats"] += 2
        ideal_macros["proteins"] -= 3
    elif user_activity == 'normal':
        ideal_macros["carbs"] += 10
        ideal_macros["fats"] += 5
        ideal_macros["proteins"] += 5
    elif user_activity == 'high':
        ideal_macros["carbs"] += 15
        ideal_macros["fats"] += 8
        ideal_macros["proteins"] += 10

    explanation += (
        "The ideal macronutrient distribution for a "
        + man_or_woman
        + " with your type of activity is "
        + f"{ideal_macros['carbs']}% carbs, {ideal_macros['fats']}% fats, {ideal_macros['proteins']}% proteins. ")

    total_recipe_macros = (recipe_macros["carbs"] + recipe_macros["fats"] + recipe_macros["proteins"])

    carbs_deviation = recipe_macros["carbs"] - (total_recipe_macros * (ideal_macros["carbs"] / 100))
    fats_deviation = recipe_macros["fats"] - (total_recipe_macros * (ideal_macros["fats"] / 100))
    proteins_deviation = recipe_macros["proteins"] - (total_recipe_macros * (ideal_macros["proteins"] / 100))

    deviation_threshold = 4

    deviation_summary = []

    if carbs_deviation > deviation_threshold:
        deviation_summary.append("It is high in carbs.")
    elif carbs_deviation < -deviation_threshold:
        deviation_summary.append("It is low in carbs.")

    if fats_deviation > deviation_threshold:
        deviation_summary.append("It is high in fats.")
    elif fats_deviation < -deviation_threshold:
        deviation_summary.append("It is low in fats.")

    if proteins_deviation > deviation_threshold:
        deviation_summary.append("It is high in proteins.")
    elif proteins_deviation < -deviation_threshold:
        deviation_summary.append("It is low in proteins.")

    if deviation_summary:
        explanation += "This recipe may not be the best choice as it deviates significantly from the ideal macronutrient ratio. "
        explanation += " ".join(deviation_summary) + " Consider adjusting the portion size or exploring other recipes. "
    else:
        explanation += "This recipe is a good choice as it closely aligns with the ideal macronutrient distribution, in fact "

    #remove?
    explanation += f"The deviations from ideal values are: carbs = {round(carbs_deviation, 2)}, "
    explanation += f"fats= {round(fats_deviation, 2)}, "
    explanation += f"proteins = {round(proteins_deviation, 2)}"
    explanation += " (anything in [-"+ str(deviation_threshold) + "," + str(deviation_threshold) + "] is good). "

    return explanation, deviation_summary
    

"""
The foodMacros_two function 
combines the foodMacros_one explanations for different recipes and chooses one of the two recipes based on how many macro-ratios they respect 
"""
def foodMacros_two(recipeA, recipeB, user):
    user_activity= user["Activity"]
    user_sex= user["Sex"]
    explanationA, deviation_summaryA= foodMacros_one(recipeA, user)
    explanationB, deviation_summaryB = foodMacros_one(recipeB, user)

    ideal_macros_distribution = {"carbs": 50, "fats": 20, "proteins": 30}  #Kreider, R. B., Wilborn, C. D., Taylor, L., Campbell, B., Almada, A. L., Collins, R., Cooke, M., Earnest, C. P., Greenwood, M., Kalman, D. S., Kerksick, C. M., Kleiner, S. M., Leutholtz, B., Lopez, H., Lowery, L. M., Mendel, R., Smith, A., Spano, M., Wildman, R., . . .  Antonio, J. (2010). ISSN exercise & sport nutrition review: Research & recommendations. Journal of the International Society of Sports Nutrition, 7, 7. https://doi.org/10.1186/1550-2783-7-7

    if user_sex is None or user_sex == "":
        ideal_macros = {
            "carbs": ideal_macros_distribution["carbs"],
            "fats": ideal_macros_distribution["fats"],
            "proteins": ideal_macros_distribution["proteins"]
        }
        man_or_woman = "person of unspecified sex"
    else:
        ideal_macros = {
            "carbs": ideal_macros_distribution["carbs"],
            "fats": ideal_macros_distribution["fats"],
            "proteins": ideal_macros_distribution["proteins"]
        }
        man_or_woman = "man" if user_sex == "m" else "woman"


    # Is this useful in this kind of explanation? 
    if user_activity == 'low':
        ideal_macros["carbs"] += 5
        ideal_macros["fats"] += 2
        ideal_macros["proteins"] -= 3
    elif user_activity == 'normal':
        ideal_macros["carbs"] += 10
        ideal_macros["fats"] += 5
        ideal_macros["proteins"] += 5
    elif user_activity == 'high':
        ideal_macros["carbs"] += 15
        ideal_macros["fats"] += 8
        ideal_macros["proteins"] += 10

    useless_expl = (
        "The ideal macronutrient distribution for a "
        + man_or_woman
        + " with your goal and type of activity is "
        + f"{ideal_macros['carbs']}% carbs, {ideal_macros['fats']}% fats, {ideal_macros['proteins']}% proteins. "
        )

    explanation = explanationA + explanationB
    explanation = str(explanation).replace(useless_expl, "")

    if deviation_summaryA == [] and deviation_summaryB == []:
        explanation += "In this case there is really no recipe better than the other, they both seem well balanced in the macro-nurients composition."

    if deviation_summaryA == [] and deviation_summaryB != []:
        explanation += "Between the two, " + recipeA["title"] + " seems more balanced in the macro-nurients composition."

    if deviation_summaryB == [] and deviation_summaryA != []:
        explanation += "Between the two, " + recipeB["title"] + " seems more balanced in the macro-nurients composition."

    if deviation_summaryA != [] and deviation_summaryB != []:
        if len(deviation_summaryA) == len(deviation_summaryB):
            if deviation_summaryA.count('low') == deviation_summaryB.count('low'):
                explanation += "In this case there is really no recipe better than the other, they both seem very unbalanced in the macro-nurients composition."

            if deviation_summaryA.count('low') > deviation_summaryB.count('low'):
                explanation += "Between the two, " + recipeA["title"] + " seems less unbalanced in the macro-nurients composition."
            elif deviation_summaryA.count('low') < deviation_summaryB.count('low'):
                explanation += "Between the two, " + recipeB["title"] + " seems less unbalanced in the macro-nurients composition."

        if len(deviation_summaryA) < len(deviation_summaryB):
            explanation += "Between the two, " + recipeA["title"] + " seems less unbalanced in the macro-nurients composition."
        elif len(deviation_summaryA) > len(deviation_summaryB):
            explanation += "Between the two, " + recipeB["title"] + " seems less unbalanced in the macro-nurients composition."

    return explanation
