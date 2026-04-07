#include <Arduino.h>

#define TOUCH_THRESHOLD 40  // Adjust this value based on your touch sensor readings

//TODO: check pins (T1 might have issue cause it's used for booting, maybe use T5)
const int touchPins[3] = {T0, T1, T2};  // Touch pins: T0 (GPIO4), T1 (GPIO0), T2 (GPIO2)
bool previousState[3] = {false, false, false};

void setup() {
    Serial.begin(115200);
    delay(1000);  // Give some time for serial to initialize
}

void loop() {
    for (int i = 0; i < 3; i++) {
        int touchValue = touchRead(touchPins[i]);
        //If it is below threshold it's considered touched
        //TODO: check if input goes up or down lol
        bool isTouched = touchValue < TOUCH_THRESHOLD;

        if (isTouched != previousState[i]) {
            previousState[i] = isTouched;
            if (isTouched) {
                Serial.printf("TOUCH%d_START\n", i);
            } else {
                Serial.printf("TOUCH%d_END\n", i);
            }
        }
    }
    delay(100);  // Small delay to debounce and prevent flooding serial
}

