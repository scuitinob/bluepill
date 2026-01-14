
<p align="center">
  <img src="img/logo.png" alt="BluePill logo" width="300">
</p>

# BluePill

**BluePill** es un script simple en Python inspirado en *The Matrix*.  
Su único propósito es mantener el sistema “despierto” simulando actividad mínima del usuario.

> *“You take the blue pill — the story ends.”*

---

## 🧠 ¿Qué hace?

- Mueve ligeramente el cursor del mouse
- Presiona la tecla **SHIFT**
- Repite la acción en intervalos configurables
- Evita que el sistema entre en reposo o bloquee la sesión

No espía, no persiste, no hace nada más.

---

## ⚙️ Requisitos

- Python 3.x
- `pyautogui`

Instalación de dependencias:
```bash
pip install pyautogui
```

## ▶️ Uso
Ejecutar desde la raíz del proyecto:
```bash
python main.py
```

Para detener el script:
 - CTRL + C
 - Stop desde el IDE

La salida está manejada para cerrarse de forma limpia, sin errores ruidosos.

## 📁 Estructura del proyecto

bluepill/

├── banner.py     # ASCII banner (estético)

├── bluepill.py   # Lógica principal

└── main.py       # Punto de entrada

## 🟦 Filosofía
 - Pequeño.
 - Simple.
 - Sin fricción.
 - 
BluePill no intenta hackear el sistema.

Solo lo mantiene despierto.

## 👤 Author

**Sergio Cuitiño**  

GitHub: [@scuitinob](https://github.com/scuitinob)



