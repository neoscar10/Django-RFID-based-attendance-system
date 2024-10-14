#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <SPI.h>
#include <MFRC522.h>


#define SS_PIN D4    
#define RST_PIN D3   

MFRC522 mfrc522(SS_PIN, RST_PIN);  
String cardUID = "";  // Variable to store the card UID

const char* ssid = "Airtel 4G MiFi_7FEF";
const char* password = "50291613";
const char* serverAddress = "192.168.0.101"; 

void setup() {
  Serial.begin(115200);   
  SPI.begin();            
  mfrc522.PCD_Init();     
  WiFi.begin(ssid, password);
  
  Serial.println("Scan an RFID card to get its UID:");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Wifi connected");


  
}

void loop() {
  // Check for new cards
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    cardUID = "";  // Clear previous UID
    Serial.print("Card UID: ");
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
      Serial.print(mfrc522.uid.uidByte[i], HEX);
      cardUID += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
      cardUID += String(mfrc522.uid.uidByte[i], HEX);
    }
    
    if (sendCardUID(cardUID)) {
        Serial.println("Card UID sent successfully.");
      } else {
        Serial.println("Failed to send Card UID.");
      }  
    delay(1000);  
    Serial.println();
    mfrc522.PICC_HaltA();
  }


  
}

bool sendCardUID(String cardUID) {
  Serial.print("Sending Card UID....");
  WiFiClient client;

  HTTPClient http;
  http.begin(client, serverAddress, 8000, "/api/register-card/");

  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  // Convert the joined cardUID to uppercase HEX format with spaces
  String formattedCardUID = "";
  for (int i = 0; i < cardUID.length(); i += 2) {
    if (i > 0) {
      formattedCardUID += " "; // Add space only if not the first character
    }
    formattedCardUID += cardUID.substring(i, i + 2);
  }
  formattedCardUID.toUpperCase(); // Convert to uppercase
  Serial.print("The card UID is: ");
  Serial.println(formattedCardUID);

  String postData = "card_uid=" + formattedCardUID + "&timestamp=2023-08-15 13:00:00.000000";

  int httpResponseCode = http.POST(postData);

  http.end();

  if (httpResponseCode == 200) {
    return true;
  } else {
    return false;
  }
}


// bool sendCardUID(String cardUID) {
//   Serial.print("Sending Card UID....");
//   WiFiClient client;

//   HTTPClient http;
//   http.begin(client, serverAddress, 8000, "/api/register-card/");

//   http.addHeader("Content-Type", "application/x-www-form-urlencoded");

//   // Convert the joined cardUID to proper HEX format with spaces
//   String formattedCardUID = "";
//   for (int i = 0; i < cardUID.length(); i += 2) {
//     formattedCardUID += cardUID.substring(i, i + 2) + " ";
//   }
//   formattedCardUID.toUpperCase(); // Convert to uppercase

//   String postData = "card_uid=" + formattedCardUID + "&timestamp=2023-08-15 13:00:00.000000";
//   Serial.print("formattedCardUID: ");
//   Serial.println(formattedCardUID);
//   int httpResponseCode = http.POST(postData);
//   Serial.println(postData);



//   http.end();

//   if (httpResponseCode == 200) {
//     return true;
//   } else {
//     return false;
//   }
// }

    







