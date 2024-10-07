import CompanyData as cd
import variables as var


company =cd.CompanyData("0428003392") # BE 0428.003.392

# Reference API call
company_references = company.fetch_references(year_span=1)
print(company_references)

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
