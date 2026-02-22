# 🔐 Text Steganography Tool Inside Classical Cipher Streams

## 📌 Project Overview

This project implements a secure **Text Steganography System** where a secret message is first encrypted using a **classical cipher (Vigenère Cipher)** and then hidden inside a carrier text using formatting-based covert channels such as:

- Extra spaces
- Capitalization patterns
- Word variations (optional enhancement)

The system also supports extraction, decryption, and integrity verification of the hidden message.

---

## 🎯 Objective

To demonstrate how covert communication channels can be created using:
1. Classical cryptography
2. Text formatting manipulation
3. Statistical analysis for detection risk assessment

This project highlights how simple formatting changes can be used to secretly transmit information.

---

## 🧠 Core Concept

1️⃣ Secret message is encrypted using a classical cipher  
2️⃣ Ciphertext is converted into binary format  
3️⃣ Binary bits are embedded into a carrier paragraph  
4️⃣ Receiver extracts bits from formatting patterns  
5️⃣ Extracted ciphertext is decrypted  
6️⃣ Integrity is verified against original message  

---

## 🔑 Inputs

- Normal plaintext message
- Secret hidden message
- Carrier text paragraph (cover text)
- Encryption key (for Vigenère or similar cipher)

---

## 📤 Outputs

- Encrypted secret message
- Stego text (carrier text with hidden data)
- Extracted ciphertext
- Decrypted recovered secret
- Integrity verification result

---

## 🏗️ System Modules

### 1️⃣ Classical Cipher Module
- Encrypts secret message using Vigenère Cipher
- Converts ciphertext into binary format for embedding

### 2️⃣ Embedding Engine
- Maps binary bits to:
  - Extra spaces
  - Capital letters
  - Formatting features
- Generates stego text

### 3️⃣ Extraction Engine
- Detects formatting patterns
- Reconstructs binary stream
- Recovers encrypted secret

### 4️⃣ Decryption Module
- Applies Vigenère decryption
- Restores original hidden message

### 5️⃣ Consistency Checker
- Verifies recovered message against original
- Ensures integrity of transmission

### 6️⃣ GUI Highlighter
- Highlights characters carrying hidden bits
- Visual representation of covert channel

---

## 📊 Learning Component (Risk Analysis)

The system maintains statistics of carrier texts:
- Average number of spaces
- Capitalization frequency
- Formatting structure

If a new carrier text deviates significantly from learned statistics, the system flags it as **high suspicion risk**, demonstrating how steganalysis can work.

---

## ⚙️ Technologies Used

- Python
- Classical Cryptography (Vigenère Cipher)
- Text Processing Techniques
- GUI (if implemented using Tkinter / PyQt)
- Binary Encoding Methods

---

