# 🚀 DataPulse

Welcome to **DataPulse**, a decentralized **peer-to-peer file-sharing** platform that allows users to share and download files securely using **AES & RSA encryption**. DataPulse operates with a **tracker-server** that coordinates active peers, while each client can both **download and serve files**.

---

## 🌍 Project Overview

### 🔹 **How DataPulse Works?**
- **Client UI (Angular)** 🖥️ – The frontend user interface.
- **Client Backend (Python - Flask & Sockets)** ⚡ – Handles file requests, uploads, and peer communication.
- **Tracker (FastAPI & MongoDB)** 📡 – Keeps track of available files and peers.

### 🔹 **Key Features**
✅ **Multi-peer downloading** – Download from **up to 5 peers in parallel** to maximize speed.  
✅ **Peer-server mechanism** – Each client opens a separate thread to listen for incoming file requests.  
✅ **AES & RSA Encryption** – Files are encrypted before transmission for security.  
✅ **MongoDB Database** – The tracker stores peer & file information efficiently.  
✅ **FastAPI & Flask** – Backend services for both client and tracker.  
✅ **Automatic Port Assignment** – Clients use an available port and register it with the tracker.  

---

## 🏗️ **Tech Stack**
| Component        | Technology Used |
|-----------------|----------------|
| **Frontend**    | Angular        |
| **Client Backend** | Flask, Python, Sockets |
| **Tracker**     | FastAPI, MongoDB |
| **Encryption**  | RSA & AES (PyCryptodome) |
| **Database**    | MongoDB (NoSQL) |
| **Concurrency** | Multithreading (for handling downloads) |

---

## 🚀 Getting Started

### 📥 Clone the Repository
```bash
git clone https://github.com/OfekBenAvraham/DataPulse.git
cd DataPulse
```

### 🔧 **Tracker Setup (FastAPI)**
```bash
cd tracker
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### ⚡ **Client Backend Setup (Flask & Sockets)**
```bash
cd client-backend
pip install -r requirements.txt
python main.py
```

### 🖥️ **Client UI Setup (Angular)**
```bash
cd client-ui
npm install
ng serve
```

---

## 🔄 **How the Download Process Works?**
1️⃣ **User selects a file** 🗂️  
2️⃣ **Tracker returns available peers** 🤝  
3️⃣ **Download starts using multi-threaded connections** ⚡  
4️⃣ **Client backend decrypts received chunks** 🔐  
5️⃣ **Files are merged and verified** ✅  

---

## 🎯 Future Improvements
- [ ] **Improve Peer-to-Peer Discovery** 🔍  
- [ ] **Support for Additional File Types** 📁  
- [ ] **Enhanced Encryption & Security** 🔐  
- [ ] **GUI Enhancements for Better UX** 🎨  

---

## 📜 License
This project is licensed under the **MIT License**.

💡 _Contributions are welcome! Feel free to fork and submit PRs._ 🚀
