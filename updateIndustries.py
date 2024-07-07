from database import storage

Industry_list = [
     "Retail",
     "Healthcare",
     "Technology",
     "Real Estate",
     "Finance",
     "Entertainment",
     "Education",
     "Construction",
     "Consulting",
     "Wholesale",
     "Agriculture",
     "Mining"
]

if __name__ == "__main__":
    for industry in Industry_list:
        storage.create_industry(industry)
    print("Industries list updated")
    for industry in storage.get_industry_list():
        print(industry.name)
    storage.end_session()
