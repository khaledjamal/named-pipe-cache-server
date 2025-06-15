# Named Pipe Cache Server

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-blue)](https://microsoft.com)
[![Python](https://img.shields.io/badge/python-3.8+-yellow)](https://www.python.org/)

A lightweight, high-performance key-value cache server using **Windows Named Pipes** for inter-process communication (IPC). This project complements my machine learning and software development work by showcasing my ability to build robust system-level tools using Python. It demonstrates my skills in **thread-safe server architecture**, **Windows inter-process communication**, and **cross-language data coordination** — essential capabilities for building performant infrastructure and automation tools.

---

## 🚀 Overview

This project enables real-time, in-memory data sharing between different processes or scripts running on the same Windows machine using a **simple text-based protocol** over a **named pipe**.

- **Language:** Python (server + client)
- **Platform:** Windows
- **License:** MIT

---

## ✨ Features

- ⚡ High Performance: Low-latency communication using in-memory storage
- 🔐 Thread-Safe: Each client is handled in an isolated thread
- 🔄 Cross-Language Ready: Designed to work with any language that supports Windows named pipes
- 📦 Simple API: Minimal `SET`/`GET` commands
- 🔥 Zero Dependencies: Uses only Python standard library and `pywin32`
- 🛠️ Robust Logging: Timestamped logs for easy debugging
- 📉 No Overhead: Lightweight and efficient for real-world use

---

## 🔧 Technologies Used

| Category              | Tools & Libraries          |
|------------------------|----------------------------|
| Programming Language   | Python                     |
| IPC Mechanism          | Windows Named Pipes        |
| Concurrency            | Python threading, Win32 API|
| Platform Integration   | pywin32, Windows OS        |

---

## 🧠 Skills Demonstrated

- Windows Named Pipe and IPC Programming
- Multi-threaded Server Architecture
- Real-Time Data Handling
- Error Isolation and Recovery
- Cross-Language System Integration
- Performance Optimization (thread-per-client model)
- Low-level OS Programming using Python

---

## 📐 Architecture

```text
┌───────────────┐     Named Pipe     ┌──────────────┐
│ Python Client ├───Communication───► Python Server │
└───────────────┘  (\\.\pipe\...) └──────────────┘
       ▲                                  │
       │                                  │
┌──────┴──────┐                    ┌──────┴──────┐
│ Other Clients│                   │ In-Memory   │
│ or Scripts   │                   │ Key-Value   │
└─────────────┘                    │   Store     │
                                   └─────────────┘
```

---

## ▶️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/khaledjamal/named-pipe-cache-server.git
   cd named-pipe-cache-server
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:
   ```bash
   python pipe-cache-server.py
   ```

4. In another terminal, run the example client:
   ```bash
   python simple-python-client.py
   ```

---

## 🐍 Python Client Example

```python
import win32file
import win32pipe
import pywintypes

PIPE_NAME = r"\\.\pipe\KeyValuePipe"

def send_command(command):
    handle = None
    try:
        handle = win32file.CreateFile(
            PIPE_NAME,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None,
        )
        win32file.WriteFile(handle, command.encode('utf-8'))
        result, data = win32file.ReadFile(handle, 4096)
        return data.decode('utf-8')
    except pywintypes.error as e:
        if e.winerror == 2:  # ERROR_FILE_NOT_FOUND
            return "Error: Cache server not running"
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if handle:
            win32file.CloseHandle(handle)

if __name__ == "__main__":
    print("SET city dubai ->", send_command("SET city dubai"))
    print("GET city ->", send_command("GET city"))
    print("G city ->", send_command("G city"))
```

---

## 📦 Requirements

Install using `pip install -r requirements.txt`

```
pywin32
```

---

## 📡 Command Protocol

| Command        | Description                     |
|----------------|---------------------------------|
| `SET key value`| Stores a value under the key    |
| `GET key`      | Retrieves the value for the key |
| `G key`        | Optimized short form of `GET`   |

---

## 🏗️ Project Structure

```
.
├── pipe-cache-server.py       # Multi-threaded Named Pipe server
├── simple-python-client.py    # Example Python client
├── requirements.txt           # Python dependencies
├── LICENSE                    # MIT License
└── README.md                  # Project documentation
```

---

## 🧪 Use Cases

- Inter-process communication for coordinating automation or scripts
- Shared configuration/state across local apps
- Real-time monitoring or messaging layer for local scripts
- Cross-language local integration

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for more details.

---

## 👤 Author

**Khaled Jamal**  
Senior Software Engineer | Machine Learning & Backend Development  
📧 Email: javaobjects@gmail.com  
🔗 LinkedIn: [khaledjamal1](https://www.linkedin.com/in/khaledjamal1)

---

## 🤝 Hire Me

If you're looking for a developer who understands both **low-level system internals** and **high-level architecture**, with practical experience in **cross-language systems** and **thread-safe server implementations**, [connect with me on LinkedIn](https://www.linkedin.com/in/khaledjamal1) or reach out directly!
