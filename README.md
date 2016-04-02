# Start Here

Not everybody has a tesla car to be able to test with so this project allows you to create a virtual car that you can use to test with.

Please note there are several security processes inplace when working with a real tesla that this project will not replcate. Thing suich as urls for the calls and actual authentication to Tesla.

So if your here wondering what to do, don't worry this readme should get you up to speed. If you know what to do then just get cracking!

When you actually use the tesla app to control your real tesla what you do is send a message to Tesla.com and it then contacts your car. This is how we have built our project to reflect this.

This project has three parts:

Client

Server

Example


# Client - think of it as your virtual Tesla Car
1. This is your webpage that will create your virtual car.
2. It will show simulate how the tesla will react to what you ask it to do.

# Server - think of it as your virtual Tesla.com Server
1. This is the simulated tesla.com server this is where your api calls go and it then sends them on to the car.
2. This checks you are who you say you are (login/password etc) before sending the message.

# Example - What you could build with the two previous
You click a button it sends and API call to the Server which then changes the car on the Client

# This is as far as I have gone with the process when I have some more time I will update this page to show you how to set them up for yourself

