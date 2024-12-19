import CompanyData as cd

company =cd.CompanyData("0428.003.392") # BE 0428.003.392 or BE 0627.792.215

# Reference API call
company_references = company.fetch_references(year_span=1)
company_dict = company.fetch_data(company_references)
company_fin = cd.fetch_fin_data(company_dict, period=['N', 'NM1'])
print(company_dict.keys())
print(company_fin)

cd.excel_export(company_dict, 'test.xlsx', period=['N'])