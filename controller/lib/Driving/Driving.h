#pragma once

#include "PinConfig.h"
#include "DiffSteering.h"
#include "Arduino.h"

enum CarSide
{
    LEFT,
    RIGHT
};

enum Direction
{
    FORWARD,
    REVERSE,
    STOP
};

class Driving
{
private:
    const int PWM_RESOLUTION = 10;
    const int MAX_RESOLUTION = 1023;
    const int MIN_RESOLUTION = 100;
    const int PWM_FREQUENCY = 20;
    const int PWM_LEFT_CH = 8;
    const int PWM_RIGHT_CH = 9;

    int pin1[2] = {LEFT_PIN_1, RIGHT_PIN_1};
    int pin2[2] = {LEFT_PIN_2, RIGHT_PIN_2};
    int speedChannel[2] = {PWM_LEFT_CH, PWM_RIGHT_CH};
    int range;
    DiffSteering DiffSteer;

    Direction getDirectionFromSpeed(int speed);
    int scaleSpeed(int speed);
    void changeState(CarSide side, Direction direction, int speed);

public:
    Driving();
    void begin(int range);
    void moveVehicle(float gas, float steer);
    ~Driving();
};