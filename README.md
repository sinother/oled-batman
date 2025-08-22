# OLED Batman Interface 🦇

Proyecto para mostrar información en una pantalla OLED SSD1306 (128x64 píxeles) conectada a una Raspberry Pi 1 B mediante I2C.

## 📦 Requisitos

- Raspberry Pi con Python 3
- Pantalla OLED SSD1306 (I2C)
- Librerías:
  - luma.oled
  - Pillow

Instala dependencias con:

pip install -r requirements.txt

### 🔌 Conexión de Pines (Raspberry Pi 1 B ↔ OLED SSD1306)

La pantalla OLED se conecta mediante el protocolo I2C. Aquí están los pines recomendados para una Raspberry Pi 1 B:

| Función OLED | Pin Raspberry Pi | Descripción         |
|--------------|------------------|----------------------|
| VCC          | Pin 1            | 3.3V Power           |
| GND          | Pin 6            | Ground               |
| SCL          | Pin 5            | GPIO 3 (I2C SCL)     |
| SDA          | Pin 3            | GPIO 2 (I2C SDA)     |

> 💡 *Nota:* Asegúrate de que el bus I2C esté habilitado en tu Raspberry Pi. Puedes hacerlo ejecutando `sudo raspi-config` y activando la interfaz I2C en el menú de configuración.


