import country_converter as coco
import pandas as pd

def get_country_name(name):
    df = pd.DataFrame({'code': [name]})
    df['short name'] = df.code.apply(lambda x: coco.convert(names=x, to='name_short', not_found=None))
    dict = df.to_dict()
    country = dict.get('short name')
    country = str(country).split("'")
    print(country[1])
    return country[1]