import CompanyData as cd


telenet =cd.CompanyData("BE 0473.416.418")

# Reference API call
telenet_references = telenet.fetch_references(year_span=2)

# Data API call
telenet_data = telenet.fetch_data(telenet_references)

print(telenet_data.keys())
print(telenet_data['2024-00091714'].keys())