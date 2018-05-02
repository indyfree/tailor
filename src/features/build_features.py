import src.data.load_dataframe as ld
import pandas as pd

def group_dataframe_by_attribute(dataframe, attribute, mean=False):

    if(mean):
        return dataframe.groupby(attribute, as_index=False).mean()
    else:
        return dataframe.groupby(attribute, as_index=False).sum()


def main():
    raw_dataframe = ld.load_raw_dataframe()
    grouped_dataframe = group_dataframe_by_attribute(raw_dataframe, 'time_on_sale')

if __name__ == '__main__':
    main()