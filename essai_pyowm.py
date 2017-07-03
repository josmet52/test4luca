import pyowm
owm = pyowm.OWM('9820dafa77974dfdc5e1b0ff667d3079')  
observation = owm.weather_at_place("Sion,ch")  
weather = observation.get_weather()  

fc = owm.daily_forecast('Sion,ch', limit=4)
f = fc.get_forecast()
index = 1

for weather in f:
#    print (weather.get_reference_time('iso'),weather.get_status(),weather.get_temperature('celsius'))

    date = weather.get_reference_time('iso')
    jour = date[8:10]
    mois = date [5:7]

    meteo = weather.get_status()
    if len(meteo) == 4:
        meteo = meteo + '  '
    if len(meteo) == 5:
        meteo = meteo + ' '

    
    temperature = str(weather.get_temperature('celsius'))
    lenString = len(temperature) - 6
    temp = temperature[lenString:lenString +5 ]

    if index == 1 :
        display1 = (jour+'-'+mois+' '+meteo+' '+temp)
    if index == 2 :
        display2 = (jour+'-'+mois+' '+meteo+' '+temp)
    if index == 3 :
        display3 = (jour+'-'+mois+' '+meteo+' '+temp)
    if index == 4 :
        display4 = (jour+'-'+mois+' '+meteo+' '+temp)

    index = index + 1

print display1
print display2
print display3
print display4
