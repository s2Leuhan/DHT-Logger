#include <Wire.h>
#include "RTClib.h"
#include "DHT.h"
#include <SD.h>

RTC_DS1307 RTC;

File logFile;
// Constantes para los pines
const int PULSADOR = 7;
const int chipSelect = 10;
char filename[16];

#define DHTPIN1 2 
#define DHTPIN2 3
//#define DHTPIN3 4
//#define DHTPIN4 5

DHT dht[] = {{DHTPIN1, DHT22},{DHTPIN2, DHT22},}; //,{DHTPIN3, DHT22},{DHTPIN4, DHT22}

void setup() {
  Serial.begin(9600);
  Serial.println("Iniciando programa...");

  Wire.begin();
  RTC.begin();

  
  Serial.print("Iniciando sincronizacion... ");
    if (! RTC.isrunning()) 
       {
          Serial.println("No es posible sincronizar el reloj");
          return;
          //RTC.adjust(DateTime(__DATE__, __TIME__)); //DESCOMENTAR PARA PONER EN HORA
       }else{
       Serial.println("Sincronizacion Completa.");
     }
     
  Serial.print(F("Iniciando SD... "));
      for (auto& sensor: dht) {
        sensor.begin();
      }
      if (!SD.begin(chipSelect))
        {
        Serial.println(F("Error al iniciar SD"));
        return;
        }
      Serial.println(F("SD Iniciada correctamente"));
  
  
  int n = 0;
  snprintf(filename, sizeof(filename), "log%04d.txt", n); // includes a three-digit sequence number in the file name
  while(SD.exists(filename)) {
    n++;
    snprintf(filename, sizeof(filename), "log%04d.txt", n);
  }
  File logFile = SD.open(filename,FILE_READ);
  Serial.println(filename);
  logFile.close();
  File archivo = SD.open(filename, FILE_WRITE);
  archivo.println("Tiempo,TInt,HInt,TExterio,HExt,Puerta");
  archivo.close(); 
  
  pinMode(PULSADOR,INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}


long tiempoUltimaLectura=0; //Para guardar el tiempo de la última lectura
float hi=0; //INICIA HumedadInterior
float he=0; //INICIA HumedadExterior
float ti=0; //INICIA TemperaturaInterior
float te=0; //INICIA TemperaturaExterior
int puerta=0; //INICIA PULSADOR

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)      
  if  (digitalRead(PULSADOR) == LOW){     // Si la lectura del pulsador es HIGH (pulsado)...
            // digitalWrite(13, HIGH);              // ... enciende el LED.
            puerta = 0;
            }
  
  //---------Lectura del Sensor--------------------------
  if(millis()-tiempoUltimaLectura>2000)
  {    
       hi = dht[0].readHumidity(); //Leemos la Humedad //PIN2
       ti = dht[0].readTemperature(); //Leemos la temperatura en grados Celsius
       he = dht[1].readHumidity(); //Leemos la Humedad //PIN3
       te = dht[1].readTemperature(); //Leemos la temperatura en grados Celsius
 
      //--------Enviamos las lecturas por el puerto serial-------------
      Serial.print("H Ext: ");
      Serial.print(he);
      Serial.print("% ");
      Serial.print("T Ext: ");
      Serial.print(te);
      Serial.print(" *C - ");
      Serial.print("H Int: ");
      Serial.print(hi);
      Serial.print("% ");
      Serial.print("T Int: ");
      Serial.print(ti);
      Serial.print(" *C - ");
      tiempoUltimaLectura=millis(); //actualizamos el tiempo de la última lectura
  //----Fin de la lectura---------------------------

                            if  (puerta == 10){     // Si la lectura del pulsador es LOW (ABIERTO)...
                              Serial.print("Puerta: ");
                              Serial.println(puerta);

                            } else {              // En caso contrario (no pulsado)... 
                              Serial.print("Puerta: ");
                              Serial.println(puerta);
                            }

 
  //----Inicio de escritura---------------------------
 
 File logFile = SD.open(filename, FILE_WRITE);
       DateTime now = RTC.now();
        if (logFile) { 
                logFile.print(now.year(), DEC);
                logFile.print('/');
                logFile.print(now.month(), DEC);
                logFile.print('/');
                logFile.print(now.day(), DEC);
                logFile.print(' ');
                logFile.print(now.hour(), DEC);
                logFile.print(':');
                logFile.print(now.minute(), DEC);
                logFile.print(':');
                logFile.print(now.second(), DEC);
              logFile.print(",");
              logFile.print(ti);
              logFile.print(",");
              logFile.print(hi);
              logFile.print(",");
              logFile.print(te);
              logFile.print(",");
              logFile.print(he);
              logFile.print(",");
              logFile.println(puerta);
              logFile.close(); 
        } 
        else {
          Serial.println("Error al abrir/crear el archivo en tarjeta SD");
        }

  puerta = 0;
 }
  //----Fin de escritura---------------------------

delay(250);
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED off (HIGH is the voltage level)
}
