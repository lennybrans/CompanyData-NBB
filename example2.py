import CompanyData as cd

list_of_companies = ['BE 0448.746.645', '0473416418']

dictionary = {}

for company in list_of_companies:
    key = company
    company_id = cd.CompanyData(company)
    company_references = company_id.fetch_references()
    company_data = company_id.fetch_data(company_references)
    dictionary[company] = company_data

print(dictionary.keys())

dreamland = dictionary['BE 0448.746.645']
telenet = dictionary['0473416418']

dreamland_fin_data = cd.fetch_fin_data(dreamland)
print(dreamland_fin_data)