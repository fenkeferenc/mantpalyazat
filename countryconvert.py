import country_converter as coco
import pandas as pd

def get_country_name(name):
    df = pd.DataFrame({'code': [name]})
    df['short name'] = df.code.apply(lambda x: coco.convert(names=x, to='name_short', not_found=None))
    df['short name'] = coco.convert(names=df.code.tolist(), to='name_short', not_found=None)
    return df