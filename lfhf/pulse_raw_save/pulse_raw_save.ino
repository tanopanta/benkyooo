#include <M5Stack.h>
#include <Ticker.h>
#include <vector>


#include <drawPulse.h>
// https://github.com/tanopanta/drawPulse

const int PIN_INPUT = 36;
const int SAMPLE_PER_SECOND = 250; //Hz
const int SAVE_INTERVAL_SEC = 120; // セーブする周期
const char* FILE_NAME = "/out_pulsewave.csv";

Ticker tickerSensor; // センサの値を読んでバッファリング
Ticker tickerWriteData; // バッファをCSVに書き込み
DrawPulse drawPulse;

volatile bool readFlg = false;
std::vector<uint16_t> sensorBuff;

void setup() {
    M5.begin();
    dacWrite(25, 0); // Speaker OFF(スピーカーノイズ対策)
    drawPulse.init();

    // 2ミリ秒ごと(500Hz)にセンサーリード
    tickerSensor.attach_ms((int)(1000 / SAMPLE_PER_SECOND), _readSensor);
    
    // バッファを確保しておく
    sensorBuff.reserve(SAVE_INTERVAL_SEC * SAMPLE_PER_SECOND + 1);
}


void loop() {
    delay(10);
    
    if(!readFlg) {
        M5.lcd.setCursor(0,0);
        M5.lcd.println("SD write...");
        File file = SD.open(FILE_NAME, FILE_APPEND);
        if(!file) {
            M5.lcd.println("\nSD card naiyo~~~");
            delay(10000);
            return;
        } 
        int buffSize = sensorBuff.size();
        if(buffSize > 0) {
          for(int i = 0; i < buffSize; i++) {
            file.println(sensorBuff[i]);
          }
          file.close();
          sensorBuff.clear();
        }
        delay(100);
        readFlg = true;
        // SAVE_INTERVAL_SEC後にセンサーリードを止める
        tickerWriteData.once(SAVE_INTERVAL_SEC, []{
          readFlg = false;
        });
    }
}

//ハンドラ－１（センサーを読んでバッファリング）

int loopcount = 0;
void _readSensor() {
    if(!readFlg) {
      return;
    }
    
    uint16_t y = analogRead(PIN_INPUT);
    sensorBuff.push_back(y);
    if(loopcount++ % (SAMPLE_PER_SECOND / 20) == 0) {
      drawPulse.addValue(y);
    }
}
