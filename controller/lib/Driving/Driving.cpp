#include "Arduino.h"
#include "Driving.h"

Driving::Driving()
{
}

void Driving::begin(int range)
{
    DiffSteer.begin(range, 132, 34);

    // Motor controller
    pinMode(LEFT_PIN_1, OUTPUT);
    pinMode(LEFT_PIN_2, OUTPUT);
    pinMode(RIGHT_PIN_1, OUTPUT);
    pinMode(RIGHT_PIN_2, OUTPUT);

    // PWM setup
    ledcSetup(PWM_LEFT_CH, PWM_FREQUENCY, PWM_RESOLUTION);
    ledcAttachPin(LEFT_SPEED_PIN, PWM_LEFT_CH);
    ledcSetup(PWM_RIGHT_CH, PWM_FREQUENCY, PWM_RESOLUTION);
    ledcAttachPin(RIGHT_SPEED_PIN, PWM_RIGHT_CH);

    this->range = range;
}

Direction Driving::getDirectionFromSpeed(int speed)
{
    if (speed < -1 * this->range || speed > this->range)
    {
        return STOP;
    };
    if (speed == 0)
    {
        return STOP;
    }
    else if (speed < 0)
    {
        return REVERSE;
    }
    else if (speed > 0)
    {
        return FORWARD;
    }
    return STOP;
};

int Driving::scaleSpeed(int speed)
{
    // TODO check formula
    if (speed == 0)
        return 0;
    // float normalized = abs(speed * 1.0 / range);
    // // empirical −1116.38x^2+2169.38x−52.9079
    // float calc = -1116.38 * normalized * normalized + 2169.38 * normalized - 52.9079;
    // if (calc <= 5)
    // {
    //     return 0;
    // }
    // return round(calc);
    return speed;
}

void Driving::changeState(CarSide side, Direction direction, int speed)
{
    int p1 = this->pin1[side];
    int p2 = this->pin2[side];
    int sCh = this->speedChannel[side];
    int scaledSpeed = this->scaleSpeed(speed);
    // DEBUG
    // Serial.printf("SCALED: %d | ACTUAL: %d | SIDE: %d | DIRECTION: %d\n", scaledSpeed, speed, side, direction);

    switch (direction)
    {
    case FORWARD:
        digitalWrite(p1, HIGH);
        digitalWrite(p2, LOW);
        ledcWrite(sCh, scaledSpeed);
        break;
    case REVERSE:
        digitalWrite(p1, LOW);
        digitalWrite(p2, HIGH);
        ledcWrite(sCh, scaledSpeed);
        break;
    case STOP:
        digitalWrite(p1, LOW);
        digitalWrite(p2, LOW);
        ledcWrite(sCh, 0);
        break;
    default:
        break;
    }
}

void Driving::moveVehicle(float gas, float steer)
{
    // Get camputed vales for left and right motor
    DiffSteer.computeMotors(steer, gas);
    int leftMotorSpeed = DiffSteer.getLeftMotorValue();
    int rightMotorSpeed = DiffSteer.getRightMotorValue();

    // DEBUG
    Serial.printf("C-GAS: %d | C-STEER: %d\n", leftMotorSpeed, rightMotorSpeed);

    // Get directions
    Direction leftDirection = getDirectionFromSpeed(leftMotorSpeed);
    Direction rightDirection = getDirectionFromSpeed(rightMotorSpeed);

    changeState(LEFT, leftDirection, leftMotorSpeed);
    changeState(RIGHT, rightDirection, rightMotorSpeed);
}

Driving::~Driving()
{
}
