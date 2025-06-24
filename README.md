# 🛠️ BackEndAPI - Flask

A collection of modular Flask-based APIs built to handle various backend tasks including Excel file operations and MP3 file management. This project serves as a growing toolkit of RESTful services for data processing, media handling, and more.

---

## 📚 Included APIs

### 📊 Excel API

- Read and write `.xlsx` files
- Convert Excel data to JSON
- Upload and download Excel files

### 🔊 MP3 API

- Provide download links or stream MP3 files
- Serve MP3 metadata (e.g., title, artist, duration)

---

## 🧰 Tech Stack

- Python 3.8+
- Flask
- Flask-RESTful
- OpenPyXL or Pandas (for Excel support)
- Standard Python `os` and `io` for file handling

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/Maddy1107/BackEndAPI_Flask.git
cd BackEndAPI_Flask
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the App

```bash
flask run
```

> Flask app will run on `http://localhost:5000` by default.

---

## 📡 API Endpoints (Examples)

### Excel API

| Method | Endpoint           | Description                  |
|--------|--------------------|------------------------------|
| POST   | `/upload-excel`    | Upload and parse Excel file  |
| GET    | `/download-excel`  | Download a generated Excel   |

### MP3 API

| Method | Endpoint           | Description                  |
|--------|--------------------|------------------------------|
| GET    | `/convert`  | Convert to MP3    |
| GET    | `/title`    | Fetch title for MP3 files |

---

## 🧪 Testing

Manual API testing with tools like Postman or curl.

---

## 🙌 Contributing

Have an idea for another API module? Fork the repo, build your service, and open a pull request!

---

## 📜 License

MIT License – free to use and modify.

---

## 👤 Author

Made with ❤️ by Nilankar  
GitHub: [Maddy1107](https://github.com/Maddy1107)
