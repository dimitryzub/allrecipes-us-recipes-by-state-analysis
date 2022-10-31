import requests, time, json
from parsel import Selector
from random import randrange
import pandas as pd


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

data = []

with open('/workspace/us-recipes-analysis-by-state/scripts/recipes-from-all-states.json', 'r') as json_file:
    RECIPE_LINKS = json.load(json_file)
    
    for state, recipe_link in RECIPE_LINKS.items():
        print(f'Extracting data from {state}')

        for link in recipe_link:
            
            recipes_data = {
                'state': None,
                'basic_info': {},
                'prep_data': {},
                'ingridients': [],
                'nutritions': {}
            }
            
            print(f'Link: {link["link"]}')
            
            html = requests.get(link['link'], headers=headers, timeout=30)
            selector = Selector(text=html.text)

            recipes_data['state'] = state
            recipes_data['basic_info']['title'] = selector.css('#article-heading_1-0::text').get().strip()
            recipes_data['basic_info']['category'] = selector.css('#mntl-text-link_2-0-1 .link__wrapper::text').get()
            recipes_data['basic_info']['rating'] = selector.css('#mntl-recipe-review-bar__rating_1-0::text').get()
            recipes_data['basic_info']['rating_count'] = selector.css('#mntl-recipe-review-bar__rating-count_1-0::text').get()
            recipes_data['basic_info']['reviews'] = selector.css('#mntl-recipe-review-bar__comment-count_1-0::text').get()
            recipes_data['basic_info']['recipe_by'] = selector.css('.mntl-attribution__item-name::text').get().strip()
            
            prep_detail_key = selector.css('.mntl-recipe-details__label::text').getall()
            prep_detail_value = selector.css('.mntl-recipe-details__value::text').getall()

            for prep_key, prep_value in zip(prep_detail_key, prep_detail_value):
                recipes_data['prep_data'][prep_key.lower().replace(' ', '_')] = prep_value.strip()

            calories_key = selector.css('.type--dog-bold+ .mntl-nutrition-facts-summary__table-cell::text').getall()
            calories_value = selector.css('.type--dog-bold::text').getall()

            for calorie_key, calorie_value in zip(calories_key, calories_value):
                recipes_data['nutritions'][calorie_key.lower()] = calorie_value.strip()
                
            for ingridient in selector.css('.mntl-structured-ingredients__list-item p'):
                recipes_data['ingridients'].append(ingridient.xpath('normalize-space()').get())
            
            data.append(recipes_data)
            
            time.sleep(randrange(1, 2))
            

pd.DataFrame(data=data).to_json('complete-recipes-list.json', orient='records')
print(json.dumps(data, indent=2, ensure_ascii=False))
