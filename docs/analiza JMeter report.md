# flask_vue_rest_CRUD application


###https://flaskvue.azurewebsites.net
INTERFACE DLA USER  KOD FRONTEND https://github.com/ulou23/flask_vue_rest_FRONT/

HTTP requests  API request methods > w pliku BACKEND 
## application.py
KOD BACKEND https://github.com/ulou23/flask_vue_rest_BACKEND python Flask

adres backendu AppService Osobno NA AZURE

##TEST DOTYCZY API >>> 

###https://sendurlsback.azurewebsites.net/urls [DELETE i POST]
###https://sendurlsback.azurewebsites.net/urls/<id_url> [PUT I DELETE]

# ANALIZA RAPORTU JMETER
 test wydajnościowy
 grupa 100 usersa na 100 sekund
 
 throughput > 
 GET 1.0/sec
 POST 1.0/sec
 PUT 1.0/sec
 DELETE  1.0/sec

 Test Plan. 

    Add → Thread Group – element odpowiedzialny za ilość użytkowników jacy będą wywoływać zapytania HTTP na serwerze.
    Add → Sampler → HTTP Request – element odpowiedzialny za kliknięcie. Komponent generuje zapytanie GET / POST po protokole HTTP.

####the throughput
WYDAJNOŚĆ  liczba żądań przetwarzanych na sekundę.
####deviation 
Odchylenie standardowe określa ilościowo, jak długo czas odpowiedzi waha się wokół jego średniej.
 Nie zaleca się oceniania wydajności systemu na podstawie odchylenia standardowego. 
Odchylenia powinny być minimalne, tj. Mniejsze niż 5%
####latency 
Opóźnienie: liczba milisekund, które upłynęły między wysłaniem żądania przez JMeter a otrzymaniem wstępnej odpowiedzi
####sample time 
liczba milisekund wymaganych przez serwer do pełnego obsłużenia żądania (response + latency)
###how many users your application can handle 
without scaling

MAXIMUM LOAD SERVER =  RESPONSE TIME I RESPONSE ERROR
 
####response times &failing request
