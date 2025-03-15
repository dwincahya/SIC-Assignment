#include <Adafruit_Fingerprint.h>
#include <HardwareSerial.h>

HardwareSerial mySerial(2);  // UART2 (TX = GPIO17, RX = GPIO16)
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

#define BUTTON_MODE 4  // Tombol untuk ganti mode

bool mode = false;   // false = Pendaftaran, true = Verifikasi
unsigned long lastPress = 0; // Debounce tombol
int fingerID = 1;    // ID awal pendaftaran
const int maxFingerprints = 2;  // Maksimal 2 sidik jari
bool scanPromptShown = false;   // Status untuk mencegah pesan berulang

// Daftar nama sesuai ID
const char* names[] = {
    "UNKNOWN",                   // ID 0 (Tidak digunakan)
    "Juandito Yefta Priatama",    // ID 1
    "Dwi Nur Cahya"               // ID 2
};

void setup() {
    Serial.begin(115200);
    mySerial.begin(57600, SERIAL_8N1, 16, 17);  // UART2 untuk sensor AS608
    pinMode(BUTTON_MODE, INPUT_PULLUP);  // Tombol pakai pull-up internal

    finger.begin(57600);  // Inisialisasi sensor

    if (finger.verifyPassword()) {
        Serial.println("✅ Sensor sidik jari terdeteksi!");
    } else {
        Serial.println("❌ Sensor tidak ditemukan! Periksa koneksi.");
        while (1);
    }
}

void loop() {
    // Jika tombol ditekan, ubah mode
    if (digitalRead(BUTTON_MODE) == LOW && millis() - lastPress > 500) {
        mode = !mode;  // Toggle mode
        lastPress = millis();
        scanPromptShown = false; // Reset status pesan
        Serial.print("Mode berubah ke: ");
        Serial.println(mode ? "Verifikasi Sidik Jari" : "Pendaftaran Sidik Jari");
    }

    if (mode == false) {
        if (fingerID <= maxFingerprints) {
            enrollFingerprint();  // Mode 1: Pendaftaran
        } else {
            Serial.println("📌 Pendaftaran selesai, tekan tombol untuk verifikasi.");
        }
    } else {
        verifyFingerprint();  // Mode 2: Verifikasi
    }
    delay(500);
}

// =========================[ Mode 1: Pendaftaran Sidik Jari ]=========================
void enrollFingerprint() {
    Serial.print("Mendaftarkan sidik jari ID "); Serial.println(fingerID);
    Serial.print("Nama: "); Serial.println(names[fingerID]);
    Serial.println("Letakkan jari Anda...");

    while (finger.getImage() != FINGERPRINT_OK);
    if (finger.image2Tz(1) != FINGERPRINT_OK) return;
    
    Serial.println("Angkat jari dan letakkan kembali...");
    delay(2000);

    while (finger.getImage() != FINGERPRINT_OK);
    if (finger.image2Tz(2) != FINGERPRINT_OK) return;

    if (finger.createModel() != FINGERPRINT_OK) return;

    if (finger.storeModel(fingerID) == FINGERPRINT_OK) {
        Serial.print("✅ Sidik jari ID "); Serial.print(fingerID);
        Serial.print(" ("); Serial.print(names[fingerID]); Serial.println(") berhasil disimpan!");
        fingerID++;  // Naikkan ID untuk pendaftaran berikutnya
    } else {
        Serial.println("❌ Gagal menyimpan sidik jari.");
    }
}

// =========================[ Mode 2: Verifikasi Sidik Jari ]=========================
void verifyFingerprint() {
    if (!scanPromptShown) {
        Serial.println("Silakan letakkan jari Anda...");
        scanPromptShown = true;
    }

    if (finger.getImage() != FINGERPRINT_OK) return;
    if (finger.image2Tz(1) != FINGERPRINT_OK) return;

    if (finger.fingerFastSearch() == FINGERPRINT_OK) {
        int foundID = finger.fingerID;
        Serial.print("✅ Sidik jari cocok dengan ID: "); Serial.print(foundID);
        
        // Cek apakah ID ada dalam daftar nama
        if (foundID <= maxFingerprints) {
            Serial.print(" ("); Serial.print(names[foundID]); Serial.println(")");
        } else {
            Serial.println(" (UNKNOWN)");
        }
    } else {
        Serial.println("❌ Sidik jari tidak cocok!");
    }

    scanPromptShown = false;  // Reset status agar pesan muncul lagi setelah verifikasi selesai
}
