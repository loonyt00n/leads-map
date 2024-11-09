import pandas as pd

def read_rm_list_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Convert DataFrame to a list of dictionaries
    rm_list = df.to_dict(orient='records')
    
    # Convert product_expertise from string to list
    for rm in rm_list:
        rm['product_expertise'] = rm['product_expertise'].split(', ')
    
    return rm_list


def read_leads_list_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Convert DataFrame to a list of dictionaries
    lead_list = df.to_dict(orient='records')
    
    return lead_list
