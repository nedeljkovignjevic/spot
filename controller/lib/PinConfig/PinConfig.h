#pragma once

#include "Arduino.h"

// CAMERA PINS
const int SIOD = SDA;
const int SIOC = SCL;

const int VSYNC = 27;
const int HREF = 23;

const int XCLK = 5;
const int PCLK = 14;

const int D0 = 16;
const int D1 = 25;
const int D2 = 17;
const int D3 = 33;
const int D4 = 18;
const int D5 = 32;
const int D6 = 19;
const int D7 = 35;

// MOTOR PINS
const int LEFT_PIN_1 = 4;
const int LEFT_PIN_2 = 0;
const int LEFT_SPEED_PIN = 2;

const int RIGHT_PIN_1 = 13;
const int RIGHT_PIN_2 = 12;
const int RIGHT_SPEED_PIN = 26;