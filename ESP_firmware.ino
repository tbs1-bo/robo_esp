/* 
Esp firmware for the robot to use with ESP8266
This firmware is used to control the robot via MQTT
To Setup In Arduino IDE: Follow the instructions on https://randomnerdtutorials.com/how-to-install-esp8266-board-arduino-ide/
As Board select "NodeMCU 1.0 (ESP-12E Module)"
Tip: Set the CPU Frequency to 160 MHz for better performance

Script created by: Luc Trottmann Last modified: 2024-01-15

*/

// Import required libraries
#include <ESP8266WiFi.h> //Included in ESP8266 Board Manager package
#include <PubSubClient.h> //https://github.com/knolleary/pubsubclient
#include <ArduinoJson.h> //Benoit Blanchon


// Hardware pin definitions
#define PIN_FORWARD_MOTOR_LEFT D5
#define PIN_BACKWARD_MOTOR_LEFT D4
#define PIN_ENABLE_MOTOR_LEFT D6
#define PIN_FORWARD_MOTOR_RIGHT D3
#define PIN_BACKWARD_MOTOR_RIGHT D2
#define PIN_ENABLE_MOTOR_RIGHT D1

// WiFi credentials
const char *ssid = "Lublicus";
const char *password = "gurkensalat";

// MQTT broker IP address
const char *mqtt_server = "10.1.48.107";
// MQTT topic
#define TOPIC "robos/rob_trottmann/movement"

// Function to set up pins
void setup_pins() {
  pinMode(PIN_FORWARD_MOTOR_LEFT, OUTPUT);
  pinMode(PIN_BACKWARD_MOTOR_LEFT, OUTPUT);
  pinMode(PIN_ENABLE_MOTOR_LEFT, OUTPUT);
  pinMode(PIN_FORWARD_MOTOR_RIGHT, OUTPUT);
  pinMode(PIN_BACKWARD_MOTOR_RIGHT, OUTPUT);
  pinMode(PIN_ENABLE_MOTOR_RIGHT, OUTPUT);
}

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

// Function to set up WiFi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

// MQTT callback function for motor control
void callback(char *topic, byte *payload, unsigned int length) {
  Serial.println("Message received");
  payload[length] = '\0'; // Null-terminate the string
  String message = String((char *)payload);

  DynamicJsonDocument doc(200); // Allocate memory for the JSON document "200 bytes/chars"
  deserializeJson(doc, message);

  String m_left_direction = doc["motor_left"]["direction"];
  int m_left_speed = doc["motor_left"]["speed"];

  String m_right_direction = doc["motor_right"]["direction"];
  int m_right_speed = doc["motor_right"]["speed"];
  Serial.println(m_right_direction);

  // Motor control logic for left motor
  if (m_left_direction == "forward") {
    digitalWrite(PIN_BACKWARD_MOTOR_LEFT, LOW);
    digitalWrite(PIN_FORWARD_MOTOR_LEFT, HIGH);
  } else if (m_left_direction == "backward") {
    digitalWrite(PIN_BACKWARD_MOTOR_LEFT, HIGH);
    digitalWrite(PIN_FORWARD_MOTOR_LEFT, LOW);
  }
  analogWrite(PIN_ENABLE_MOTOR_LEFT, map(m_left_speed, 0, 100, 0, 255));

  // Motor control logic for right motor
  if (m_right_direction == "forward") {
    digitalWrite(PIN_BACKWARD_MOTOR_RIGHT, LOW);
    digitalWrite(PIN_FORWARD_MOTOR_RIGHT, HIGH);
  } else if (m_right_direction == "backward") {
    digitalWrite(PIN_BACKWARD_MOTOR_RIGHT, HIGH);
    digitalWrite(PIN_FORWARD_MOTOR_RIGHT, LOW);
  }
  analogWrite(PIN_ENABLE_MOTOR_RIGHT, map(m_right_speed, 0, 100, 0, 255));
}

// Callback function for general MQTT messages
void callbacks(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // LED control based on MQTT message
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);
  } else {
    digitalWrite(BUILTIN_LED, HIGH);
  }
}

// Function to reconnect to MQTT broker
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.subscribe(TOPIC);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

// Setup function
void setup() {
  setup_pins();
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

// Main loop
void loop() {
  if (!client.connected()) { // Reconnect if connection is lost
    reconnect(); 
  }
  client.loop(); // Check for new messages
}
