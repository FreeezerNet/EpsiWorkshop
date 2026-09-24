/*
    SmartGrid Arduino Layer

    Responsibilities:
    - Read potentiometers
    - Send measurements to Python
    - Receive LED commands from Python
    - Update LEDs

    No SmartGrid logic here.
*/

const int CLK = A0;
const int DT = A1;

const int CLK2 = A3;
const int DT2 = A4;

int productionRatio = 50;
int storageRatio = 50;

const int SURVIVAL_LED = 13;
const int GREENHOUSE_LED = 3;
const int PROPULSION_LED = 5;
const int SERVER_LED = 6;
const int LIGHTING_LED = 9;
const int LEISURE_LED = 10;

const int GRID_RGB_R = 7; //Battery led
const int GRID_RGB_G = 12;
const int GRID_RGB_B = 2;

// Buzzer
const int BUZZER_PIN = 11;

unsigned long lastSend = 0;
const unsigned long SEND_INTERVAL = 500;

bool productionArme = true;
bool storageArme = true;

unsigned long productionDernierComptage = 0;
unsigned long storageDernierComptage = 0;

unsigned long productionDepuisRepos = 0;
unsigned long storageDepuisRepos = 0;

const int ANTI_REBOND_MS = 5;
const int STABLE_MS = 20;

// Buffer for incoming serial command
String incomingLine = "";

void updateSingleEncoder(
    int clkPin,
    int dtPin,
    int &value,
    bool &arme,
    unsigned long &dernierComptage,
    unsigned long &depuisRepos,
    int minValue,
    int maxValue
)
{
    int CLKactuel = digitalRead(clkPin);
    int DTactuel  = digitalRead(dtPin);

    bool auRepos =
        (CLKactuel == HIGH &&
         DTactuel == HIGH);

    if (arme)
    {
        if (
            CLKactuel == LOW &&
            (millis() - dernierComptage) > ANTI_REBOND_MS
        )
        {
            bool clkStableLow = true;

            for (int i = 0; i < 4; i++)
            {
                delayMicroseconds(500);

                if (digitalRead(clkPin) != LOW)
                {
                    clkStableLow = false;
                    break;
                }
            }

            if (clkStableLow)
            {
                DTactuel = digitalRead(dtPin);

                if (DTactuel == HIGH)
                {
                    value -= 5;
                }
                else
                {
                    value += 5;
                }

                if (value < minValue)
                    value = minValue;

                if (value > maxValue)
                    value = maxValue;

                dernierComptage = millis();
                arme = false;
            }
        }
    }
    else
    {
        if (!auRepos)
        {
            depuisRepos = millis();
        }

        if (
            auRepos &&
            (millis() - depuisRepos) >= STABLE_MS
        )
        {
            arme = true;
        }
    }
}

void setup()
{
    Serial.begin(9600);

    pinMode(SURVIVAL_LED, OUTPUT);
    pinMode(GREENHOUSE_LED, OUTPUT);
    pinMode(PROPULSION_LED, OUTPUT);
    pinMode(SERVER_LED, OUTPUT);
    pinMode(LIGHTING_LED, OUTPUT);
    pinMode(LEISURE_LED, OUTPUT);

    pinMode(GRID_RGB_R, OUTPUT);
    pinMode(GRID_RGB_G, OUTPUT);
    pinMode(GRID_RGB_B, OUTPUT);

    pinMode(BUZZER_PIN, OUTPUT);
    digitalWrite(BUZZER_PIN, LOW);

    pinMode(CLK, INPUT_PULLUP);
    pinMode(DT, INPUT_PULLUP);
    pinMode(CLK2, INPUT_PULLUP);
    pinMode(DT2, INPUT_PULLUP);

    Serial.println("SMARTGRID_READY");
}

void loop()
{
    updateEncoder();

    sendMeasurements();

    receiveCommands();
}

void sendMeasurements()
{
    if (millis() - lastSend < SEND_INTERVAL)
        return;

    lastSend = millis();

    Serial.print("P:");
    Serial.print(productionRatio);

    Serial.print(";S:");
    Serial.println(storageRatio);
}

void receiveCommands()
{
    while (Serial.available())
    {
        char c = Serial.read();

        if (c == '\n')
        {
            processCommand(incomingLine);
            incomingLine = "";
        }
        else
        {
            incomingLine += c;
        }
    }
}

void processCommand(String cmd)
{
    int survival   = getValue(cmd, "SUR:");
    int greenhouse = getValue(cmd, "GRN:");
    int propulsion = getValue(cmd, "PRO:");
    int server     = getValue(cmd, "SRV:");
    int lighting   = getValue(cmd, "LIG:");
    int leisure    = getValue(cmd, "LEI:");

    int batteryState = getValue(cmd, "BAT:");

    int rgbR   = getValue(cmd, "RGBR:");
    int rgbG   = getValue(cmd, "RGBG:");
    int rgbB   = getValue(cmd, "RGBB:");

    int buzzer = getValue(cmd, "BUZ:");

    if (survival >= 0)
        analogWrite(SURVIVAL_LED, survival);

    if (greenhouse >= 0)
        analogWrite(GREENHOUSE_LED, greenhouse);

    if (propulsion >= 0)
        analogWrite(PROPULSION_LED, propulsion);

    if (server >= 0)
        analogWrite(SERVER_LED, server);

    if (lighting >= 0)
        analogWrite(LIGHTING_LED, lighting);

    if (leisure >= 0)
        analogWrite(LEISURE_LED, leisure);

    if (batteryState >= 0)
    {
        setBatteryState(batteryState);
    }

    if (
        rgbR >= 0 &&
        rgbG >= 0 &&
        rgbB >= 0
    )
    {
        analogWrite(GRID_RGB_R, rgbR);
        analogWrite(GRID_RGB_G, rgbG);
        analogWrite(GRID_RGB_B, rgbB);
    }

    if (buzzer >= 0)
    {
        if (buzzer)
        {
            tone(
                BUZZER_PIN,
                1000
            );
        }
        else
        {
            noTone(
                BUZZER_PIN
            );
        }
    }
}

int getValue(String data, String key)
{
    int start = data.indexOf(key);

    if (start == -1)
        return -1;

    start += key.length();

    int end = data.indexOf(';', start);

    if (end == -1)
        end = data.length();

    return data.substring(start, end).toInt();
}

void updateEncoder()
{
    updateSingleEncoder(
        CLK,
        DT,
        productionRatio,
        productionArme,
        productionDernierComptage,
        productionDepuisRepos,
        0,
        100
    );

    updateSingleEncoder(
        CLK2,
        DT2,
        storageRatio,
        storageArme,
        storageDernierComptage,
        storageDepuisRepos,
        0,
        100
    );
}