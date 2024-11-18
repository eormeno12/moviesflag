
# Movie API with MongoDB Cache

This project demonstrates a Flask application for fetching movie data from the OMDB API, caching results in MongoDB, and testing performance with Locust.

---

## Requirements

- Python 3.10+
- Docker and Docker Compose
- OMDB API Key (Free) from [OMDB API](https://www.omdbapi.com/apikey.aspx)

---

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/eormeno12/moviesflag.git
cd moviesflag
git checkout cache-db
```

### Step 2: Configure OMDB API Key
1. Go to [OMDB API](https://www.omdbapi.com/apikey.aspx) and sign up for a free API key.
2. Replace the placeholder `apikey` in line 6 of `app.py`:
   ```python
   apikey = "your-api-key-here"
   ```

### Step 3: Set up MongoDB with Docker Compose
1. Start MongoDB using Docker Compose:
   ```bash
   docker compose up -d
   ```
2. Verify MongoDB is running:
   - Visit `http://localhost:8081` to access Mongo Express (admin panel).
   - Login credentials:
     - **Username**: `root`
     - **Password**: `example`

---

### Step 4: Install Dependencies
Install the required Python dependencies using `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### Step 5: Run the Flask App
Start the Flask application:
```bash
python app.py
```

Access the app in your browser:
- Example URL: [http://127.0.0.1:5000/?filter=transformers](http://127.0.0.1:5000/?filter=transformers)

---

## Performance Testing with Locust

### Step 1: Start Locust
1. Run Locust:
   ```bash
   locust
   ```
2. Open Locust UI at [http://localhost:8089](http://localhost:8089).
3. Configure:
   - **Number of users**: Number of simulated users (e.g., `50`).
   - **Ramp up**: Users spawned per second (e.g., `5`).
   - **Host**: `http://127.0.0.1:5000`

4. Click **Start** to begin the stress test.

---

## Cleanup
To stop the services:
- **MongoDB**:
  ```bash
  docker compose down
  ```
- **Flask app**:
  Press `Ctrl+C`.
  
- **Locust**:
  Press `Ctrl+C`.
