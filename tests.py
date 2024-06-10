from classes.Persistences.CountriesManager import CountriesManager

countriesManager = CountriesManager()
print(countriesManager.getCountry("RU"))
countriesManager.createCountry({
    "country_code": "RU",
    "name": "Russian"
})
print(countriesManager.getCountry("RU"))