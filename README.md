
# Store Monitoring Backend

This project is a backend API for monitoring restaurant stores. It tracks the uptime and downtime of stores during business hours and generates reports for restaurant owners based on polling data.

## Features

- **Trigger Report**: API to trigger the generation of uptime/downtime reports.
- **Report Status**: API to check the status of the report (Running, Complete, Failed).
- **Download Report**: Once completed, the report can be downloaded as a CSV file.
- **Timezone Handling**: Converts timestamps from UTC to local store times using timezone data.
- **Background Processing**: Uses threading to process report generation in the background.

## Prerequisites

1. Python 3.x
2. MySQL (or any compatible database)
3. Flask
4. SQLAlchemy
5. `pytz` for timezone conversions
6. `uuid` for generating unique report IDs
7. `threading` for background report processing

## Setup

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd store_monitoring_backend
    ```

2. Set up a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your MySQL database:
   
   - Create a new database called `loopdatabase`.
   - Update your database connection string in `database.py` with your MySQL username and password.

5. Initialize the database:

    ```bash
    python
    >>> from database import init_db
    >>> init_db()
    >>> exit()
    ```

6. Load the CSV data into the database manually or through a custom script.

## Running the Application

1. Start the Flask app:

    ```bash
    python app.py
    ```

2. The app will start running at `http://127.0.0.1:5000/`.

3. Available API Endpoints:

    - **/trigger_report** (POST): Triggers the report generation and returns a `report_id`.
    - **/get_report** (GET): Checks the report status using `report_id`. If complete, downloads the CSV.

4. Health Check:

    ```bash
    curl http://127.0.0.1:5000/health
    ```

## Project Structure

- `app.py`: Main application file with the API endpoints.
- `calculations.py`: Contains logic for calculating uptime/downtime based on polling data.
- `database.py`: Manages database connections and initialization.
- `models.py`: Defines the database schema (StoreStatus, BusinessHours, StoreTimezone).
- `utils.py`: Utility functions, primarily for time zone conversion.
- `requirements.txt`: Lists Python dependencies.

## Ideas for Improvement

- Implement error handling for edge cases where data is incomplete or corrupted.
- Add unit tests for core functionalities like report generation and time conversion.
- Optimize the uptime/downtime calculation to handle large datasets efficiently.
- Consider using task queues (e.g., Celery) for background tasks instead of threading.

## Conclusion

This project demonstrates a backend solution for monitoring restaurant stores, handling time zone conversions, and efficiently generating reports in the background.
