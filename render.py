#!/usr/bin/env python3

import json
import csv
import jinja2
import pprint

import pandas as pd

url = "https://raw.githubusercontent.com/digital-land/alpha-data/master/mhclg-registers/developer-contribution-purpose.csv"

data = pd.read_csv(url,sep=",")

# strip spaces introduced to values
data_frame_trimmed = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# strip spaces introduced to column headers
data_frame_trimmed = data_frame_trimmed.rename(columns=lambda x: x.strip())

json_data = json.loads(data_frame_trimmed.to_json(orient='records'))
pprint.pprint(json_data)



# set up paths to where the templates are
def register_templates():
    multi_loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader(searchpath="./templates"),
        jinja2.PrefixLoader({
            'govuk-jinja-components': jinja2.PackageLoader('govuk_jinja_components'),
            'digital-land-frontend': jinja2.PackageLoader('digital_land_frontend')
        })
    ])
    return jinja2.Environment(loader=multi_loader)

#from resource_generator.filters import pluralise, curie_org_url

static_folder = "https://digital-land-design.herokuapp.com/static"

# register filters with jinja context
# def register_filters(env):
#     env.filters["pluralise"] = pluralise
#     env.filters["curie_url"] = curie_org_url

# jinja setup
env = register_templates()
#register_filters(env)

page_template = env.get_template("index.html")

def render_page():
    with open(f"developer-contribution-purposes.html", "w") as f:
        f.write(page_template.render(
            static_folder=static_folder,
            data=json_data)
        )

if __name__ == '__main__':
    render_page()
