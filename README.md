# Vertex AI Generative Multimodal Example

# Description
This project provides a web application that allows users to generate text from images or videos using a Vertex AI generative model. The prompt text for the model is securely retrieved from Google Cloud Secret Manager.

Setup
1 Clone this repository to your local machine.

2 Create a Google Cloud project and enable the Vertex AI API.

3 Create a secret in Secret Manager containing the prompt text for the model and the alias "prod". An example prompt is included in secure-prompt-example.json and can be deployed using "gcloud secrets create my-prompt --data-file=secure-prompt-example.json && gcloud secrets update my-prompt --update-version-aliases=prod=1"

4 Install the required Python libraries using "pip install -r requirements.txt"


Run the application:
python -m uvicorn main:app --reload  
Open your browser and navigate to http://localhost:8000/.
Upload an image or video file.
Enter the project ID and secret name .
Click "Submit" to generate text from the media file.


Disclaimer
This project is intended for demonstration purposes only and should not be used in production environments.
