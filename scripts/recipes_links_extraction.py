import requests, time, json
from parsel import Selector
import pandas as pd
from random import randrange

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

# extraxted from Dev tools console
# Array.from(document.querySelectorAll(".taxonomy-nodes__item.mntl-block a")).map(x => x.getAttribute("href"))
RECIPES_LINKS_BY_STATE = [
    'https://www.allrecipes.com/recipes/1601/us-recipes/us-recipes-by-state/texas/',
    'https://www.allrecipes.com/recipes/1621/us-recipes/us-recipes-by-state/washington-dc/',
    'https://www.allrecipes.com/recipes/1622/us-recipes/us-recipes-by-state/colorado/',
    'https://www.allrecipes.com/recipes/1623/us-recipes/us-recipes-by-state/arizona/',
    'https://www.allrecipes.com/recipes/1632/us-recipes/us-recipes-by-state/north-carolina/',
    'https://www.allrecipes.com/recipes/1753/us-recipes/us-recipes-by-state/illinois/',
    'https://www.allrecipes.com/recipes/1754/us-recipes/us-recipes-by-state/california/',
    'https://www.allrecipes.com/recipes/1756/us-recipes/us-recipes-by-state/alaska/',
    'https://www.allrecipes.com/recipes/1757/us-recipes/us-recipes-by-state/oregon/',
    'https://www.allrecipes.com/recipes/1758/us-recipes/us-recipes-by-state/washington/',
    'https://www.allrecipes.com/recipes/1759/us-recipes/us-recipes-by-state/wyoming/',
    'https://www.allrecipes.com/recipes/1760/us-recipes/us-recipes-by-state/montana/',
    'https://www.allrecipes.com/recipes/1761/us-recipes/us-recipes-by-state/utah/',
    'https://www.allrecipes.com/recipes/1762/us-recipes/us-recipes-by-state/idaho/',
    'https://www.allrecipes.com/recipes/1763/us-recipes/us-recipes-by-state/new-mexico/',
    'https://www.allrecipes.com/recipes/1764/us-recipes/us-recipes-by-state/oklahoma/',
    'https://www.allrecipes.com/recipes/1765/us-recipes/us-recipes-by-state/georgia/',
    'https://www.allrecipes.com/recipes/1766/us-recipes/us-recipes-by-state/florida/',
    'https://www.allrecipes.com/recipes/1767/us-recipes/us-recipes-by-state/louisiana/',
    'https://www.allrecipes.com/recipes/1768/us-recipes/us-recipes-by-state/maryland/',
    'https://www.allrecipes.com/recipes/1769/us-recipes/us-recipes-by-state/new-york/',
    'https://www.allrecipes.com/recipes/1770/us-recipes/us-recipes-by-state/pennsylvania/',
    'https://www.allrecipes.com/recipes/1771/us-recipes/us-recipes-by-state/massachusetts/',
    'https://www.allrecipes.com/recipes/1772/us-recipes/us-recipes-by-state/ohio/',
    'https://www.allrecipes.com/recipes/1773/us-recipes/us-recipes-by-state/indiana/',
    'https://www.allrecipes.com/recipes/1774/us-recipes/us-recipes-by-state/michigan/',
    'https://www.allrecipes.com/recipes/1775/us-recipes/us-recipes-by-state/wisconsin/',
    'https://www.allrecipes.com/recipes/1776/us-recipes/us-recipes-by-state/minnesota/',
    'https://www.allrecipes.com/recipes/1777/us-recipes/us-recipes-by-state/missouri/',
    'https://www.allrecipes.com/recipes/1778/us-recipes/us-recipes-by-state/iowa/',
    'https://www.allrecipes.com/recipes/1779/us-recipes/us-recipes-by-state/north-dakota/',
    'https://www.allrecipes.com/recipes/1780/us-recipes/us-recipes-by-state/south-dakota/',
    'https://www.allrecipes.com/recipes/1781/us-recipes/us-recipes-by-state/kansas/',
    'https://www.allrecipes.com/recipes/1782/us-recipes/us-recipes-by-state/nebraska/',
    'https://www.allrecipes.com/recipes/1808/us-recipes/us-recipes-by-state/connecticut/',
    'https://www.allrecipes.com/recipes/1809/us-recipes/us-recipes-by-state/maine/',
    'https://www.allrecipes.com/recipes/1810/us-recipes/us-recipes-by-state/new-hampshire/',
    'https://www.allrecipes.com/recipes/1811/us-recipes/us-recipes-by-state/rhode-island/',
    'https://www.allrecipes.com/recipes/1812/us-recipes/us-recipes-by-state/vermont/',
    'https://www.allrecipes.com/recipes/1813/us-recipes/us-recipes-by-state/delaware/',
    'https://www.allrecipes.com/recipes/1814/us-recipes/us-recipes-by-state/new-jersey/',
    'https://www.allrecipes.com/recipes/1815/us-recipes/us-recipes-by-state/virginia/',
    'https://www.allrecipes.com/recipes/1816/us-recipes/us-recipes-by-state/south-carolina/',
    'https://www.allrecipes.com/recipes/1817/us-recipes/us-recipes-by-state/alabama/',
    'https://www.allrecipes.com/recipes/1818/us-recipes/us-recipes-by-state/arkansas/',
    'https://www.allrecipes.com/recipes/1819/us-recipes/us-recipes-by-state/kentucky/',
    'https://www.allrecipes.com/recipes/1820/us-recipes/us-recipes-by-state/tennessee/',
    'https://www.allrecipes.com/recipes/2593/us-recipes/us-recipes-by-state/west-virginia/',
    'https://www.allrecipes.com/recipes/2824/us-recipes/us-recipes-by-state/mississippi/',
    'https://www.allrecipes.com/recipes/2832/us-recipes/us-recipes-by-state/nevada/',
    'https://www.allrecipes.com/recipes/734/us-recipes/us-recipes-by-state/hawaii/'
]

# extraxted from Dev tools console
# Array.from(document.querySelectorAll(".taxonomy-nodes__item.mntl-block a")).map(x => x.textContent)
STATES_NAMES = [
    'Texas',
    'Washington D.C',
    'Colorado',
    'Arizona',
    'North Carolina',
    'Illinois',
    'California',
    'Alaska',
    'Oregon',
    'Washington',
    'Wyoming',
    'Montana',
    'Utah',
    'Idaho',
    'New Mexico',
    'Oklahoma',
    'Georgia',
    'Florida',
    'Louisiana',
    'Maryland',
    'New York',
    'Pennsylvania',
    'Massachusetts',
    'Ohio',
    'Indiana',
    'Michigan',
    'Wisconsin',
    'Minnesota',
    'Missouri',
    'Iowa',
    'North Dakota',
    'South Dakota',
    'Kansas',
    'Nebraska',
    'Connecticut',
    'Maine',
    'New Hampshire',
    'Rhode Island',
    'Vermont',
    'Delaware',
    'New Jersey',
    'Virginia',
    'South Carolina',
    'Alabama',
    'Arkansas',
    'Kentucky',
    'Tennessee',
    'West Virginia',
    'Mississippi',
    'Nevada',
    'Hawaii'
]

recipes_links = []

for link, state in zip(RECIPES_LINKS_BY_STATE, STATES_NAMES):
    print(f'extracting link: {link}')
    
    html = requests.get(link, headers=headers, timeout=30)
    selector = Selector(text=html.text)

    for link in selector.css('.card::attr(href)'):
        recipes_links.append({
            state: {'link': link.get()}
        })
    
    time.sleep(randrange(3, 6))

# pd.DataFrame(data=recipes_links).to_json('recipes-from-all-states.json')

# DROP ALL NAN
# not_formatted_json = pd.read_json('/workspace/us-recipes-analysis-by-state/scripts/recipes-from-all-states.json')
# df = pd.DataFrame(data=not_formatted_json).apply(lambda x: list(x.dropna()), axis=0)

# new_df = df
# new_df.to_json('recipes-from-all-states_fixed.json')