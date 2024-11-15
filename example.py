import CompanyData as cd

company =cd.CompanyData("0627.792.215") # BE 0428.003.392

# Reference API call
company_references = company.fetch_references(year_span=2)
company_dict = company.fetch_data(company_references)
company_fin = cd.fetch_fin_data(company_dict, ['N', 'NM1'])
print(company_fin)

# # Data API call
# company_data = company.fetch_data(company_references)

# # Get sub_keys without prior information
# list_company_ref = list(company_data.keys())
# print(list_company_ref)

# list_sub_keys = []
# for reference in list_company_ref:
#     list_sub_keys.extend(list(company_data[reference].keys()))

# list_sub_keys = list(set(list_sub_keys))
# print(list_sub_keys)

# # Variables
# current_name = company_data[list_company_ref[-1]][var.enterprise_name]
# current_address = company_data[list_company_ref[-1]][var.address]
# current_administators = company_data[list_company_ref[-1]][var.administrators]
# # To be extended

# # DataFrame with financial data for requested years -> see fetch_references
# fin_data = cd.fetch_fin_data(company_data)
# fin_data = fin_data.apply(cd.inventory_cycle_finished, axis=1)
# print(fin_data.DIO_finished)
