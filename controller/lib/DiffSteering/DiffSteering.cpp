#include "Arduino.h"
#include "DiffSteering.h"

DiffSteering::DiffSteering()
{
    leftMotorValue = 0;
    rightMotorValue = 0;
}

void DiffSteering::begin(int length)
{
    range = 1023;
    this->length = length;
    this->wheelRadius = wheelRadius;
}

void DiffSteering::begin(int range, int length, int wheelRadius)
{
    this->range = range;
    this->length = length;
    this->wheelRadius = wheelRadius;
}

void DiffSteering::computeMotors(float xValue, float yValue)
{
    int XValue = round(xValue * range);
    int YValue = round(yValue * range);
    float nMotPremixL = 0; // Motor (left)  premixed output        (-127..+127)
    float nMotPremixR = 0; // Motor (right) premixed output        (-127..+127)
    int nPivSpeed = 0;     // Pivot Speed                          (-127..+127)
    float fPivScale = 0;   // Balance scale b/w drive and pivot    (   0..1   )
    int m_fPivYLimit = 32;

    // Calculate Drive Turn output due to Joystick X input
    if (YValue >= 0)
    {
        // Forward
        nMotPremixL = (XValue >= 0) ? range : (range + XValue);
        nMotPremixR = (XValue >= 0) ? (range - XValue) : range;
    }
    else
    {
        // Reverse
        nMotPremixL = (XValue >= 0) ? (range - XValue) : range;
        nMotPremixR = (XValue >= 0) ? range : (range + XValue);
    }

    // Scale Drive output due to Joystick Y input (throttle)
    nMotPremixL = nMotPremixL * YValue / range;
    nMotPremixR = nMotPremixR * YValue / range;

    // Now calculate pivot amount
    // - Strength of pivot (nPivSpeed) based on Joystick X input
    // - Blending of pivot vs drive (fPivScale) based on Joystick Y input
    nPivSpeed = XValue;
    fPivScale = (abs(YValue) > m_fPivYLimit) ? 0.0 : (1.0 - abs(YValue) / m_fPivYLimit);

    // Calculate final mix of Drive and Pivot
    rightMotorValue = (1.0 - fPivScale) * nMotPremixL + fPivScale * (nPivSpeed);
    leftMotorValue = (1.0 - fPivScale) * nMotPremixR + fPivScale * (-nPivSpeed);
    // leftMotorValue = nMotPremixL;
    // rightMotorValue = nMotPremixR;
}

int DiffSteering::getLeftMotorValue()
{
    return this->leftMotorValue;
}

int DiffSteering::getRightMotorValue()
{
    return this->rightMotorValue;
}