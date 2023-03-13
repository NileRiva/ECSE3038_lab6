# Lab 6

For this lab, students will be implementing part of an end-to-end platform to be used to control the state of electronic devices connected to the ESP32 module.

Students will be asked to write two separate applications, one to be used as an API that should be accessible over the internet and the other to used as an arduino sketch to be programmed on to ESP32 module.

## Embedded

For consistency, use pins 22 and 23 for your Fan and Light pins respectively.

Also, use the variable names WIFI_USER and WIFI_PASS as the wifi information in your arduino code.

### PUT request

Create a function that reads the current temperature from a connected digital temperature sensor. This temperature value should be used to populate the body of a PUT request that should be sent form the ESP32 to your API.

```
PUT /api/temperature HTTP/1.1
Host: {https://your.api.domain}
Content-type: application/json
Content-length: 23

{ "temperature": 29.2 }
```

If you don't have access to a digital temperature sensor, you may create a function that generates and returns a random float between 21.0 and 33.0. 

### GET request

Your ESP32 module code should also include a get request that should be sent to your API.

```
GET /api/state HTTP/1.1
Host: {https://your.api.domain}
```

The response of this request should determine how your circuit reacts, ie, the state of your fan pin and light pin.

## API

You’ll be expected to make your API available over the internet by deploying your server application to an online cloud hosting service like [https://render.com/](https://render.com/).

Make sure that your code works from your local machine first then commit to GitHub so that render has access to it.

### GET request

The API response from the GET request handler should contain a JSON body that has a fan and and light attribute. 

The fan attribute of the JSON response should be true if the current temp in the database is greater than or equal to 28.0 and it should be false otherwise. 

The light attribute should be true if the current time is later than todays sunset time according to the below API, and should be false otherwise. 

```
GET /api/sunset HTTP/1.1
Host: https://ecse-sunset-api.onrender.com
```

### PUT request

The API response from the PUT request handler should return am HTTP 204 status code on a successful PUT and return an HTTP 400 otherwise.

Your request body from the ESP32 should be saved directly to the database.


API URL https://nilelab6.onrender.com
ALTERNATE https://ecse3038-lab6.onrender.com