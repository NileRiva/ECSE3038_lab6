# Lab 5

## Reporting the state of LEDs using Arduino and HTTP

In this assignment, students will learn how to use Arduino to send HTTP requests to a server to report the states of three LEDs in their circuit to a webpage. 

Students should create an Arduino sketch that sends an HTTP request with a JSON body to an API to set the desired state of the light switches on a webpage.

### Set up the circuit

Connect three LEDs to digital output pins on the ESP32 board. Use a resistor for each LED to limit the current and prevent damage to the LEDs.

The API has already been built for you and can be accessed at the following URL:

```
https://ecse-three-led-api-v2.onrender.com
```

### Embedded HTTP Input

You’ll be allowed to view the set state of each of the three LEDs by using this [tester site](https://ecse-three-led-v2.netlify.app/). The site should allow to see the current state of your circuit after the LED states have been changed. 

Note the assigned username in the top left corner of the webpage. This is a unique identifier and should be included in your PUT requests to the API as an API key.

This ensures that each person is able to control their own instance of the webpage.

The API expects a PUT request to include an API key in the request headers:

```
PUT /api/state HTTP/1.1
Host: https://ecse-three-led-api-v2.onrender.com
X-API-Key: {username}
Content-type: application/json
Content-length: 76

{ "light_switch_1": true, "light_switch_2": false, "light_switch_3": false }
```

### Write the Arduino sketch

Use the relevant libraries to connect to the API and send a PUT request to the `/api/state` route of the API. 

Create a two dimensional array that contains the desired state of the LEDs. 

Two dimensional array should should allow your three LEDs to flash in the order of a 3 bit binary counter, for example:

```
false, false, false
false, false, true
...
```

Your array should contain, at least, 8 arrays, and each inner array should be one that has 3 Boolean values. 

Use a for loop to iterate through your array to digitally write the the desired state of each LED.

The PUT request should be made after the states of all three LEDs are set.

Pause for at least 2 seconds after each request.

It is not necessary, in this case to parse the response of the API as no usable information is reported back after a successful request.

You may still need to see what that response looks like in case you’re facing any unexpected errors.

**NOTE**

Treat the Wifi name, Wifi password, API URL and API Key as sensitive information.