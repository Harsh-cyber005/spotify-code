# Spotify Playlist Application

This guide explains how to set up and run the Spotify Playlist application. Follow the steps below to install the dependencies, configure Playwright, and run the application.

---

## Prerequisites

- **Python**: Ensure Python 3.7 or later is installed.
- **Virtual Environment (Optional but Recommended)**: Set up a virtual environment to isolate dependencies.

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Harsh-cyber005/spotify-code
cd spotify-code
```

### 2. Set Up Virtual Environment (Optional)

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Use the following command to install the required Python libraries:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Run the application using the following command:

```bash
python app.py
```

---

## Entering the Spotify Playlist Link

You can enter the Spotify playlist link when prompted by the application. It will download the playlist and store the songs in your downloads folder inside a folder named `getspotify`.


---