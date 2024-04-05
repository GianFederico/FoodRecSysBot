import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np

# Load the CSVs file into a pandas DataFrame
recipe_df = pd.read_csv('dataset_en.csv')
commodity_df = pd.read_csv('CSEL_df_cleaned.csv')
replies_df = pd.read_csv('replies.csv')


def FSAscore(url):
    #'https://www.giallozafferano.it/images/ricette/201/20113/foto_hd/hd650x433_wm.jpg'

    # Filter the DataFrame based on the URL
    filtered_recipe_df = recipe_df[recipe_df['imageURL'] == url]
    recipe_values = filtered_recipe_df.iloc[0][['fat', 'saturatedFat', 'sugars', 'sodium']].to_dict()

    # Divide each value by 1.2 for FSA score calculation
    for key in recipe_values:
        recipe_values[key] = float(recipe_values[key]) / 1.2

    # Calculate the FSA score using the provided calculation
    score = 0
    if recipe_values['fat'] <= 3.0:
        score += 1
    elif 3.0 < recipe_values['fat'] <= 17.5:
        score += 2
    else:
        score += 3

    if recipe_values['saturatedFat'] <= 1.5:
        score += 1
    elif 1.5 < recipe_values['saturatedFat'] <= 5.0:
        score += 2
    else:
        score += 3

    if recipe_values['sugars'] <= 5.0:
        score += 1
    elif 5.0 < recipe_values['sugars'] <= 22.5:
        score += 2
    else:
        score += 3

    sodium = recipe_values['sodium'] / 1000  # Convert sodium to grams
    salt = sodium * 2.5  # Calculate salt
    if salt <= 0.3:
        score += 1
    elif 0.3 < salt <= 1.5:
        score += 2
    else:
        score += 3

    if score <= 5.6:
        score_level_str = "Very Healthy"
    elif (score > 5.6) and (score <= 7.2):
        score_level_str = "Healthy"
    elif (score > 7.2) and (score <= 8.6):
        score_level_str = "Moderately Healthy"
    elif (score > 8.6) and (score <= 10.2):
        score_level_str = "Somewhat Unhealthy"
    else:
        score_level_str = "Unhealthy"

    # Print the FSA score
    print(f"FSA Score for the recipe: {score_level_str}")

def calculate_iss(ingredient, co2_value, wfp_value, min_co2, max_co2, min_wfp, max_wfp):
    a = 0.8
    b = 0.2
    try:
        # Calculate normalized values
        ncfp = (co2_value - min_co2) / (max_co2 - min_co2)
        nwfp = (wfp_value - min_wfp) / (max_wfp - min_wfp)

        if ncfp<0 or nwfp<0:
            print("something wrong because I have negative values")
            print(ncfp, nwfp)


        return a * ncfp + b * nwfp
    except Exception as e:
        print(f"Error calculating ISS for {ingredient}: {e}")
        return None

def find_scores(url):
    e=2.71
    iss_values = []

    url_to_find = url #'https://www.giallozafferano.it/images/ricette/201/20113/foto_hd/hd650x433_wm.jpg'

    # Minumum values of co2 and wf
    min_co2 = 0.19
    min_wfp = 41.0
    max_co2 = 25.23
    max_wfp = 126505.0

    # Filter the DataFrame based on the URL
    filtered_recipe_df = recipe_df[recipe_df['imageURL'] == url_to_find]

    # Check if any rows are found for the given URL
    if not filtered_recipe_df.empty:
        # Extract the list of ingredients from the filtered row
        ingredients_list = [ingredient.strip().lower() for ingredient in filtered_recipe_df['ingredients'].values[0].split(',')]  # Convert to lowercase

        FSAscore(url)

        food_commodities = commodity_df['Food commodity ITEM'].tolist()

        # Store matched ingredients and their corresponding 'final_co2' and 'final_wfp' values
        matched_ingredients = {}
        for ingredient in ingredients_list:
            for item in food_commodities:
                if fuzz.partial_ratio(ingredient, item.lower()) >= 90:  # threshold
                    matched_ingredients[item] = {
                        'final_co2': commodity_df.loc[commodity_df['Food commodity ITEM'] == item, 'final_co2'].values[0],
                        'final_wfp': commodity_df.loc[commodity_df['Food commodity ITEM'] == item, 'final_wfp'].values[0]
                    }
                    break

        if matched_ingredients:
            iss_values.clear()
            for ingredient, values in matched_ingredients.items():
                # Convert co2 and wfp values to floats
                iss = calculate_iss(ingredient, float(values['final_co2'].replace(',', '.')), float(values['final_wfp'].replace(',', '.')), min_co2, max_co2, min_wfp, max_wfp)
                if iss:
                    iss_values.append(iss)

            final_DSS = 0
            iss_values_sorted = sorted(iss_values, reverse=True)
            for i, iss in enumerate(iss_values_sorted):
                final_DSS += iss * (e**i)
                #dss_rounded=round(final_DSS,2)
                scaled_value = np.log(1 + final_DSS)

                #this was to gather all the scores for every recipe in the dataset
                # with open('sust_scores.txt', 'a') as file:
                #     file.write(str(round(scaled_value,4)) + ',')

                if scaled_value <= 0.6303:
                    sus_score_level_str = "Very Sustainable"
                elif (scaled_value > 0.6303) and (scaled_value <= 0.8355):
                    sus_score_level_str = "Sustainable"
                elif (scaled_value > 0.8355) and (scaled_value <= 0.9242):
                    sus_score_level_str = "Moderately Sustainable"
                elif (scaled_value > 0.9242) and (scaled_value <= 0.9651):
                    sus_score_level_str = "Somewhat Unsustainable"
                else:
                    sus_score_level_str = "Unsustainable"
            
            print("Sustainability Score for the recipe:",sus_score_level_str) #, round(scaled_value,5)
            print("_____________________________________________________")
                

    else:
        print(f"URL {url_to_find} not found in the CSV file.")


i=1
# for url in recipe_df['imageURL'].unique():
#     print("--------RICETTA ",i, ":")
#     find_scores(url)
#     if i==7:
#         i=1
#     else:
#         i=i+1



url_columns = ['RICETTA1_URL', 'RICETTA2_URL', 'RICETTA3_URL', 'RICETTA4_URL', 'RICETTA5_URL', 'RICETTA6_URL']
for index, row in replies_df.iterrows():
    for column in url_columns:
        user = row['Utente']
        url = row[column]
        print(f"----------User: {user} - RICETTA {i}:")
        find_scores(url)
        if i==6:
            i=1
        else:
            i=i+1





























# #___________________________________________________________________________
# e=2.71
# iss_values = []
# # Load the CSV file into a pandas DataFrame
# recipe_df = pd.read_csv('dataset_en.csv')
# commodity_df = pd.read_csv('CSEL_df_cleaned.csv')

# # Assuming 'url' is the column name containing the URLs
# url_to_find = 'https://www.giallozafferano.it/images/ricette/201/20113/foto_hd/hd650x433_wm.jpg'  # Replace this with the actual URL you want to search for

# # Filter the DataFrame based on the URL
# filtered_recipe_df = recipe_df[recipe_df['imageURL'] == url_to_find]

# # Minumum values of co2 and wf
# min_co2 = 0.19
# min_wfp = 41.0
# max_co2 = 25.23
# max_wfp = 126505.0

# # min_co2 = float(commodity_df['final_co2'].min().replace(',', '.'))
# # min_wfp = float(commodity_df['final_wfp'].min().replace(',', '.'))
# # max_co2 = float(commodity_df['final_co2'].max().replace(',', '.'))
# # max_wfp = float(commodity_df['final_wfp'].max().replace(',', '.'))

# print("@@@@@@@@@@@@",min_co2, max_co2, min_wfp, max_wfp)

# min_dss = 0
# max_dss = 0
# j=1

# DSSs=[]
# for url_to_find in recipe_df['imageURL'].unique():
#     # Filter the DataFrame based on the URL
#     filtered_recipe_df = recipe_df[recipe_df['imageURL'] == url_to_find]

#     # Check if any rows are found for the given URL
#     if not filtered_recipe_df.empty:
#         # Extract the list of ingredients from the filtered row
#         ingredients_list = [ingredient.strip().lower() for ingredient in filtered_recipe_df['ingredients'].values[0].split(',')]  # Convert to lowercase

#         #FSAscore()

#         food_commodities = commodity_df['Food commodity ITEM'].tolist()

#         # Store matched ingredients and their corresponding 'final_co2' and 'final_wfp' values
#         matched_ingredients = {}
#         for ingredient in ingredients_list:
#             for item in food_commodities:
#                 if fuzz.partial_ratio(ingredient, item.lower()) >= 90:  # threshold
#                     matched_ingredients[item] = {
#                         'final_co2': commodity_df.loc[commodity_df['Food commodity ITEM'] == item, 'final_co2'].values[0],
#                         'final_wfp': commodity_df.loc[commodity_df['Food commodity ITEM'] == item, 'final_wfp'].values[0]
#                     }
#                     break

#         if matched_ingredients:
#             iss_values.clear()
#             for ingredient, values in matched_ingredients.items():
#                 # Convert co2 and wfp values to floats
#                 print("INGREDIENT: ", ingredient, "FINAL_CO2: ",values['final_co2'],"FINAL_WFP: ", values['final_wfp'])
#                 print(min_co2, max_co2, min_wfp, max_wfp)
#                 iss = calculate_iss(ingredient, float(values['final_co2'].replace(',', '.')), float(values['final_wfp'].replace(',', '.')), min_co2, max_co2, min_wfp, max_wfp)
#                 if iss:
#                     iss_values.append(iss)

#             final_DSS = 0
            
#             iss_values_sorted = sorted(iss_values, reverse=True)
#             for i, iss in enumerate(iss_values_sorted):
#                 final_DSS += iss * (e**i)
#                 dss_rounded=round(final_DSS,2)
#                 DSSs.append(dss_rounded)
            
#             # Update min_dss and max_dss if necessary
#             min_dss = min(min_dss, final_DSS)
#             max_dss = max(max_dss, final_DSS)

#     else:
#         print(f"URL {url_to_find} not found in the CSV file.")
#     print("Recipe ", j)
#     j=j+1

# print("Minimum DSS:", min_dss)
# print("Maximum DSS:", max_dss)
# print("_______________")
# print(iss_values_sorted)
# print(sorted(DSSs))