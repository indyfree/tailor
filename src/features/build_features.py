

def group_dataframe_by_attribute(dataframe, attribute, mean=False):

    if(mean):
        return dataframe.groupby(attribute, as_index=False).mean()
    else:
        return dataframe.groupby(attribute, as_index=False).sum()


def main():
    return

if __name__ == '__main__':
    main()