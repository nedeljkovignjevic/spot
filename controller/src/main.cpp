#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include "PinConfig.h"
#include "Driving.h"

const char *SSID = "internet";
const char *password = "asdf1246";

const char *apSSID = "SPOT";
const char *apPassword = "10371GGG";

AsyncWebServer infoServer(80);
AsyncWebServer driveServer(81);

AsyncWebSocket infoSocket("/info");
AsyncWebSocket driveSocket("/drive");

Driving driving;

float steer = 0.0;
float speed = 0.0;

void handleWebSocketInfoMessage(uint32_t id, void *arg, uint8_t *data, size_t len)
{
  AwsFrameInfo *info = (AwsFrameInfo *)arg;
  if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT)
  {
    data[len] = 0;
    if (strcmp((char *)data, "info") == 0)
    {
      infoSocket.textAll(String(steer, 2));
      // Serial.print("-----");
      // Serial.print(String(steer, 2));
      // Serial.print("-----\n");
    }
  }
}

void handleWebSocketDriveMessage(uint32_t id, void *arg, uint8_t *data, size_t len)
{
  AwsFrameInfo *info = (AwsFrameInfo *)arg;
  if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT)
  {
    data[len] = 0;
    if (data[0] == 'C')
    {
      // Parse first value
      int len1 = 5;
      // Ignore first character ('C')
      int i = 1;
      if (data[i] == '-')
      {
        len1 = 6;
      }
      char first[len1];
      while (data[i] != '|')
      {
        first[i - 1] = data[i];
        ++i;
      }
      first[i - 1] = 0;
      // Parse second value
      int len2 = 5;
      if (data[i] == '-')
      {
        len2 = 6;
      }
      char second[len2];
      while (data[i] != 0)
      {
        second[i - len1 - 1] = data[i];
        ++i;
      }
      second[i - 1] = 0;
      float gasValue = atof(first);
      float steerValue = atof(second);

      speed = gasValue;
      steer = steerValue;

      // Serial.print("*****");
      // Serial.print(steer);
      // Serial.print("*****\n");

      driving.moveVehicle(gasValue, steerValue);
    }
  }
}

void onInfoEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type,
                 void *arg, uint8_t *data, size_t len)
{
  switch (type)
  {
  case WS_EVT_CONNECT:
    Serial.printf("WebSocket client #%u connected to Info Socket from %s\n", client->id(), client->remoteIP().toString().c_str());
    break;
  case WS_EVT_DISCONNECT:
    Serial.printf("WebSocket client #%u disconnected from Info Socket\n", client->id());
    break;
  case WS_EVT_DATA:
    handleWebSocketInfoMessage(client->id(), arg, data, len);
    break;
  case WS_EVT_PONG:
  case WS_EVT_ERROR:
    break;
  }
}

void onDriveEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type,
                  void *arg, uint8_t *data, size_t len)
{
  switch (type)
  {
  case WS_EVT_CONNECT:
    Serial.printf("WebSocket client #%u connected to Drive Socket from %s\n", client->id(), client->remoteIP().toString().c_str());
    break;
  case WS_EVT_DISCONNECT:
    Serial.printf("WebSocket client #%u disconnected from Drive Socket\n", client->id());
    break;
  case WS_EVT_DATA:
    handleWebSocketDriveMessage(client->id(), arg, data, len);
    break;
  case WS_EVT_PONG:
  case WS_EVT_ERROR:
    break;
  }
}

void initInfoServer()
{
  infoSocket.onEvent(onInfoEvent);
  infoServer.addHandler(&infoSocket);
  infoServer.begin();
  Serial.println("Info server started");
}

void initDrivingServer()
{
  driveSocket.onEvent(onDriveEvent);
  driveServer.addHandler(&driveSocket);
  driveServer.begin();
  Serial.println("Driving server started");
}

void initWiFiAP()
{
  WiFi.disconnect(true);
  Serial.print("Setting Access Point…");
  WiFi.softAP(apSSID, apPassword);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
}

void initWiFi()
{
  WiFi.mode(WIFI_AP_STA);

  WiFi.softAP(apSSID, apPassword);
  WiFi.begin(SSID, password);

  Serial.println("Connecting to WiFi..");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.print("ESP32 IP as soft AP: ");
  Serial.println(WiFi.softAPIP());

  Serial.print("ESP32 IP on the WiFi network: ");
  Serial.println(WiFi.localIP());
}

void setup()
{
  Serial.begin(115200);
  driving.begin(1023);
  initWiFiAP();
  initInfoServer();
  initDrivingServer();
}

void loop()
{
}
