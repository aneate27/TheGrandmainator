# The Grandma-inator
A knit fabric with three different sections of conductive thread, where for each part pressed individual a sound-byte from a grandma plays. When all three parts are pressed at once, it switches to Kardashian mode where a Kris Jenner sound-byte it played when each button is pressed.

<img width="1512" height="2016" alt="IMG_5476 2" src="https://github.com/user-attachments/assets/2000a468-3d04-4a99-adcd-fa888b8370ce" />


This project is a proof of concept that you can use conductive thread to knit a fabric into responsive buttons. There are a lot of things here that will be improved in my final project version, but this project was really helpful in teaching me what things I need to optimize and be careful of.

## Set-up
Knit a piece of fabric, and to add conductive thread in sections yarn over with both your working yarn and the thread. Then knit as usual, keeping in mind that the stiffness of the thread makes it difficult to work with. When you are finished with a section, leave a long tail to be tied to your ESP32. (although I will note that it may be useful to grab an Arduino Lilypad component to make the interfacing significantly easier) Make sure that you are using pins 2, 32, and 27.

Download the provided audio files as well as the source and sound code. Using PlatformIO, build and upload the source code to your ESP32 through a wired connection. Then run the sound code on your computer, where you will be prompted to select the port that connects your ESP32. It should now be up and running!

I also created an ESP32 case out of plastic cross-stitch cards. An example of one side of the enclosure is shown below:

<img width="4032" height="3024" alt="IMG_5485" src="https://github.com/user-attachments/assets/4dda0372-baca-405a-b7ad-baff29fb1104" />

