from classes.Persistences.CountriesManager import CountriesManager
from classes.Persistences.CitiesManager import CitiesManager

countriesManager = CountriesManager()
print(countriesManager.getCountry("FR").toJSON())
citiesManager = CitiesManager()
print(citiesManager.getCity(1).toJSON())
print(citiesManager.getCity(2).toJSON())
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