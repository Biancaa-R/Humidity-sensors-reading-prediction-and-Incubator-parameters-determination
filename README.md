# Humidity-sensors-reading-prediction-and-Incubator-parameters-determination

<b>Problem:</b>

Preterm birth or more commonly known as premature birth, is the birth of an infant less than 38 weeks of gestational age and also with a weight less than two kilograms. Premature birth indicates that the infant had less time to develop in the mothers womb and is not fully developed enough for survival. They can easily have complicated medical problems. Most of the premature babies suffer from respiratory related ailments as their lungs are not fully developed to endure the outside atmosphere . In 2021, preterm birth affected about 1 of every 10 infants born in the United States. (cite:https://www.cdc.gov/reproductivehealth/maternalinfanthealth/pretermbirth)

<b>The proposed infant incubator system:</b>

In the proposed infant incubator system, Is going to predict the incubator parameters. That is the temperature and the relative humidity to be maintained inside the incubator for the highest chance of success rate for the child placed inside the incubator. This ideology can also be extended for hatcheries as well, making sure that with the predicted values of parameters , the baby is present in an optimum environment.  

<b> Connected external circuit</b>

<img src="https://github.com/Biancaa-R/Humidity-sensors-reading-prediction-and-Incubator-parameters-determination/blob/main/pictures/diag.png" allign="center">

<b>3.1:Features in the application</b>

1. A register that contains all the previous records, which it retrieves from the cloud so that all the previously added and stored data can be accessed through the app.

2. Signup and login page with database integration, so unauthorized members don’t have access to the information.
 
3. Facility to add new record and get the prediction result immediately,with the ml model running in the backend.
 
4. Customized dashboard which is varied for each user.
 
5.Telegram bot integration. Therefore , anyone can access the data easily.

6.The added values are sent to the cloud immediately without glitch/


<b><u>4.1The prediction of the incubator parameters are based on:</b></u>

4.1.1.Age of the infant: The gestational period in weeks is the age of the infant , greater the gestational age ,greater is the health of the infant, higher is the chances of survival for the infant.

4.1.2.weight of the infant: The weight in grams of the infant is also a rough estimate of its overall growth and development, which can be used to estimate the incubator parameters.

4.1.3.room temperature: The predicted value of incubator parameters can also vary based on the surrounding.

4.1.4.Room humidity: The predicted value of incubator parameters can also vary based on the surrounding.

4.1.5.Heat out of incubator: The heat that is given out ,during the operation of the incubator is the heat out of the incubator.

 humidity inside the incubator is measured using the fabricated sensor and the temperature using dht11, therefore the parameters currently present inside the incubator are measured and displayed and the predicted values are also displayed, and immediately stored to the cloud. The system is also connected to a telegram bot ,so even when the doctor is at a far off location, they can access the data through the telegram bot or through the cloud directly.

 # The UI 
 <b> Signin page</b>
 <img src="https://github.com/Biancaa-R/Humidity-sensors-reading-prediction-and-Incubator-parameters-determination/blob/main/pictures/2023-09-01%20(11).png">

 <b> Page to activate the telebot</b>
 <img src="https://github.com/Biancaa-R/Humidity-sensors-reading-prediction-and-Incubator-parameters-determination/blob/main/pictures/2023-09-01%20(10).png">

 <b> Login page</b>
 <img src="https://github.com/Biancaa-R/Humidity-sensors-reading-prediction-and-Incubator-parameters-determination/blob/main/pictures/2023-09-01%20(4).png">

 <b> Dashboard</b>
 <img src="https://github.com/Biancaa-R/Humidity-sensors-reading-prediction-and-Incubator-parameters-determination/blob/main/pictures/2023-09-01%20(7).png">

 <b>Register connected to cloud</b>
 <img src="https://github.com/Biancaa-R/Humidity-sensors-reading-prediction-and-Incubator-parameters-determination/blob/main/pictures/2023-09-01%20(8).png">

 <b>Adding new input values for prediction</b>
 <img src="https://github.com/Biancaa-R/Humidity-sensors-reading-prediction-and-Incubator-parameters-determination/blob/main/pictures/2023-09-01%20(9).png">

 

