import pandas as pd
from fuzzywuzzy import fuzz
import math

def FSAscore():
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

    # Print the FSA score
    print(f"FSA Score for the recipe: {score}")

def replace_comma_with_period(value):
    # Replace comma with period if present and it's not part of a larger number
    if ',' in value and '.' not in value:
        value = value.replace(',', '.')
    return value

def calculate_iss(ingredient, co2_value, wfp_value, min_co2, max_co2, min_wfp, max_wfp):
    a = 0.8
    b = 0.2
    try:
        # Convert co2_value and wfp_value to floats
        # Replace commas with periods in all relevant values
        co2_value = replace_comma_with_period(co2_value)
        wfp_value = replace_comma_with_period(wfp_value)
        min_co2 = replace_comma_with_period(min_co2)
        max_co2 = replace_comma_with_period(max_co2)
        min_wfp = replace_comma_with_period(min_wfp)
        max_wfp = replace_comma_with_period(max_wfp)

        # Convert values to floats
        co2_value = float(co2_value)
        wfp_value = float(wfp_value)
        min_co2 = float(min_co2)
        max_co2 = float(max_co2)
        min_wfp = float(min_wfp)
        max_wfp = float(max_wfp)

        # Calculate normalized values
        ncfp = (co2_value - min_co2) / (max_co2 - min_co2)
        nwfp = (wfp_value - min_wfp) / (max_wfp - min_wfp)


        return a * ncfp + b * nwfp
    except Exception as e:
        print(f"Error calculating ISS for {ingredient}: {e}")
        return None


e=2.71
iss_values = []

# Load the CSV file into a pandas DataFrame
recipe_df = pd.read_csv('dataset_en.csv')
commodity_df = pd.read_csv('CSEL_df_cleaned.csv')

# Assuming 'url' is the column name containing the URLs
url_to_find = 'https://www.giallozafferano.it/images/ricette/201/20113/foto_hd/hd650x433_wm.jpg'  # Replace this with the actual URL you want to search for

# Filter the DataFrame based on the URL
filtered_recipe_df = recipe_df[recipe_df['imageURL'] == url_to_find]

# Minumum values of co2 and wf
min_co2 = commodity_df['final_co2'].min().replace(',', '.')
min_wfp = commodity_df['final_wfp'].min().replace(',', '.')
max_co2 = commodity_df['final_co2'].max().replace(',', '.')
max_wfp = commodity_df['final_wfp'].max().replace(',', '.')

minimums=[]
maximums=[]
min_dss = 0
max_dss = -math.inf
j=1

for url_to_find in recipe_df['imageURL'].unique():
    # Filter the DataFrame based on the URL
    filtered_recipe_df = recipe_df[recipe_df['imageURL'] == url_to_find]

    # Check if any rows are found for the given URL
    if not filtered_recipe_df.empty:
        # Extract the list of ingredients from the filtered row
        ingredients_list = [ingredient.strip().lower() for ingredient in filtered_recipe_df['ingredients'].values[0].split(',')]  # Convert to lowercase

        #FSAscore()

        food_commodities = commodity_df['Food commodity ITEM'].tolist()

        # Store matched ingredients and their corresponding 'final_co2' and 'final_wfp' values
        matched_ingredients = {}
        for ingredient in ingredients_list:
            for item in food_commodities:
                if fuzz.partial_ratio(ingredient, item.lower()) >= 90:  # Adjust the threshold as needed
                    matched_ingredients[item] = {
                        'final_co2': commodity_df.loc[commodity_df['Food commodity ITEM'] == item, 'final_co2'].values[0],
                        'final_wfp': commodity_df.loc[commodity_df['Food commodity ITEM'] == item, 'final_wfp'].values[0]
                    }
                    break

        if matched_ingredients:
            iss_values.clear()
            for ingredient, values in matched_ingredients.items():
                # Convert co2 and wfp values to floats
                iss = calculate_iss(ingredient, values['final_co2'], values['final_wfp'], min_co2, max_co2, min_wfp, max_wfp)
                if iss:
                    iss_values.append(iss)

            final_DSS = 0
            iss_values_sorted = sorted(iss_values, reverse=True)
            for i, iss in enumerate(iss_values_sorted):
                final_DSS += iss * math.exp(i + 1)
            
            # Update min_dss and max_dss if necessary
            min_dss = min(min_dss, final_DSS)
            minimums.append(min_dss)
            max_dss = max(max_dss, final_DSS)
            maximums.append(max_dss)

    else:
        print(f"URL {url_to_find} not found in the CSV file.")
    print("Recipe ", j)
    j=j+1

print("Minimum DSS:", min_dss)
print("Maximum DSS:", max_dss)
print("_______________")
print(minimums)
print("__________________________")
print(maximums)