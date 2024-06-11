def read_data():
    from pandas import read_csv
    data=read_csv('./data/train.csv',sep=',',decimal='.')
    print('shape: ',data.shape)
   

    return data


def clean_data(data):
    #remove errors
    data=data.loc[(data.isin(['NaN '])==False).prod(axis=1)==1,:]
    data=data.loc[(data.isna()==False).prod(axis=1)==1,:]


    #correct the columns types
    convert_columns = {
        'Delivery_person_Age':int,
        'Delivery_person_Ratings': float,
        'multiple_deliveries':int
    }
    data=data.astype(convert_columns)

    #tranform order_date to a data text
    from pandas import to_datetime
    data['Order_Date']=to_datetime(data['Order_Date'],format='%d-%m-%Y')

    #remove spaces of strings
    col_remove_space=['ID',
                      'Delivery_person_ID',
                      'Road_traffic_density',
                      'Type_of_order',
                      'Type_of_vehicle',
                      'Festival',
                      'City']
    data[col_remove_space]=data[col_remove_space].apply(lambda x: x.str.strip())
    #display(data.dtypes)
    return data
