import CompanyData as cd

company = cd.CompanyData("0428.003.392") # BE 0428.003.392 or BE 0627.792.215

# Check company attributes such as company.data and company.reference_table
# company.data is a dictionary that contains Filing objects
# E.g. {'reference_number': Filing-class object}
# The object contains all information, inlcuding metadata about the filing
# Check the class for its attributes