from classes.Persistences.CountriesManager import CountriesManager
from classes.Persistences.CitiesManager import CitiesManager


countriesManager = CountriesManager()
print(countriesManager.getCountry("FR").toJSON())
citiesManager = CitiesManager()
print(citiesManager.getCity("5fc7012c-8a7f-4177-ac87-ab820b932e92").toJSON())
# countriesManager.createCountry({
#     "country_code": "RU",
#     "name": "Russian"
# })
# print(countriesManager.getCountry("RU"))
# countriesManager.updateCountry({
#     "country_code": "RU",
#     "name": "Russie"
# })
# print(countriesManager.getCountry("RU"))

citiesManager.updateCity({
    "id": "5fc7012c-8a7f-4177-ac87-ab820b932e92",
    "name": "poissy"
})
print(citiesManager.getCity("5fc7012c-8a7f-4177-ac87-ab820b932e92").toJSON())