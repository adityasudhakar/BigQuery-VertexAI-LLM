# Project: Connecting BigQuery with Vertex AI LLM

## Requirements

Ensure you have the following installed before running the application:

- Python 3.8 or later
- Required Python packages (see `requirements.txt`)

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Ahmadshahzad2/BigQuery-VertexAI-LLM.git
   cd BigQuery-VertexAI-LLM
   ```

2. **Create a conda environment:**

   ```bash
   conda create -n <env_name>
   conda activate <env_name>
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud credentials:**

   Ensure you have a Google Cloud project with BigQuery and Vertex AI enabled. Authenticate your Google Cloud account and set up your project:

   ```bash
   gcloud init
   gcloud auth application-default login
   ```

## Running the Application

1. **Start the Streamlit application:**

   ```bash
   streamlit run app.py
   ```

2. **Access the application:**

   Open your web browser and go to `http://localhost:8501`.

---
