from classes.Persistences.CountriesManager import CountriesManager

countriesManager = CountriesManager()
print(countriesManager.getCountry("RU"))
countriesManager.createCountry({
    "country_code": "RU",
    "name": "Russian"
})
print(countriesManager.getCountry("RU"))
countriesManager.updateCountry({
    "country_code": "RU",
    "name": "Russie"
})
print(countriesManager.getCountry("RU"))