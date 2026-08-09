import json
import os

original_2_1_data = json.load(open('/Users/ssjw/IdeaProjects/factoriolab/public/data/2.1/data.json'))
original_spa_data = json.load(open('/Users/ssjw/IdeaProjects/factoriolab/public/data/2x1/data.json'))


def get_item_type(category):
    if category == 'technology':
        return 'technology'
    elif category == 'fluids':
        return 'fluid'
    else:
        return 'item'


def print_ids(data: dict):
    i = 0
    for key in data.keys():
        i += 1
        print(f'{i}: {key}')


def load_original_data(original_data):
    categories = {category['id']: category for category in original_data['categories']}
    items = {item['id']: item for item in original_data['items']}
    recipes = {recipe['id']: recipe for recipe in original_data['recipes']}
    locations = {location['id']: location for location in original_data['locations']}

    return categories, items, recipes, locations


def convert(original_data, exported, output_file):
    exported_data = json.load(open(exported, 'r', encoding='utf-8'))

    category_original, item_original, recipe_original, location_original = load_original_data(original_data)

    categories_exported = {x['id']: x for x in exported_data['categories']}
    items_exported = {x['id']: x for x in exported_data['items']}
    recipes_exported = {x['id']: x for x in exported_data['recipes']}
    locations_exported = {x['id']: x for x in exported_data['locations']}

    categories_new = {}
    items_new = {}
    recipes_new = {}
    locations_new = {}

    # categories
    for category_id in category_original:
        if category_id in categories_exported:
            categories_new[category_id] = categories_exported[category_id]['name']
        else:
            print(f'Category ID {category_id} not found in original data.')

    # item -> recipes -> technology
    
    # items
    print("Items:")
    for item_id in item_original:
        if item_id in items_exported:
            items_new[item_id] = items_exported[item_id]['name']
        elif (found := 'technology-' + item_id.split('-technology')[0]) in items_exported:
            items_new[item_id] = items_exported[found]['name']
        elif (found := get_item_type(item_original[item_id]['category']) + '-' + item_id) in items_exported:
            items_new[item_id] = items_exported[found]['name']
        else:
            print(f'Item ID {item_id} not found in original data.')
            items_new[item_id] = ''

    # recipes
    print("Recipes:")
    for recipe_id in recipe_original:
        if recipe_id in recipes_exported:
            recipes_new[recipe_id] = recipes_exported[recipe_id]['name']
        elif (found := 'technology-' + recipe_id.split('-technology')[0]) in recipes_exported:
            recipes_new[recipe_id] = recipes_exported[found]['name']
        elif (recipe_id.endswith('-recycling')):
            recipes_new[recipe_id] = items_new[recipe_id.replace('-recycling', '')] + ' 재활용'
        else:
            print(f'Recipe ID {recipe_id} not found in original data.')
            recipes_new[recipe_id] = ''
    
    # technology items

    # locations
    for location_id in location_original:
        if location_id in locations_exported:
            locations_new[location_id] = locations_exported[location_id]['name']
        else:
            print(f'Location ID {location_id} not found in original data.')

    new_data = {
        'categories': categories_new,
        'items': items_new,
        'recipes': recipes_new,
        'locations': locations_new
    }

    with open(os.path.join(os.path.dirname(exported), output_file), 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    exported_spa = '2.1/space-age data.json'
    convert(original_spa_data, exported_spa, 'ko_spa.json')

    # exported_2_1 = '2.1/vanilla data.json'
    # convert(original_2_1_data, exported_2_1, 'ko_2_1.json')
