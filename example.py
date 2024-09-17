import CompanyData as cd
import variables as var


company =cd.CompanyData("BE 0473.416.418")

# Reference API call
company_references = company.fetch_references(year_span=2)

# Data API call
company_data = company.fetch_data(company_references)

# Get sub_keys without prior information
company_ref_id = list(company_data.keys())
print(company_ref_id)

sub_keys = []
for ref_id in company_ref_id:
    sub_keys.extend(list(company_data[ref_id].keys()))

sub_keys = list(set(sub_keys))
print(sub_keys)

# Variables
current_name = company_data[company_ref_id[-1]][var.enterprise_name]
current_address = company_data[company_ref_id[-1]][var.address]
current_administators = company_data[company_ref_id[-1]][var.administrators]
# To be extended

# DataFrame with financial data for requested years -> see fetch_references
extract_data = cd.fetch_fin_data(company_data)
print(extract_data)