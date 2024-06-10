from classes.Persistences.CountriesManager import CountriesManager

countriesManager = CountriesManager()
print(countriesManager.getCountry("FR"))
countriesManager.updateCountry({
    "country_code": "FR",
    "name": "France"
})
print(countriesManager.getCountry("FR"))