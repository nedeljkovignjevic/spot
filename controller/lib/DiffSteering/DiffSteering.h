#pragma once

#include "Arduino.h"

class DiffSteering
{
private:
    int leftMotorValue;
    int rightMotorValue;
    int range;
    int length;
    int wheelRadius;

public:
    DiffSteering();
    void begin(int length);
    void begin(int range, int length, int wheelRadius);
    void computeMotors(float xValue, float yValue);
    int getLeftMotorValue();
    int getRightMotorValue();
};