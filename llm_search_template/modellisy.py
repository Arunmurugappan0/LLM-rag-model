import google.generativeai as genai

# Configure Gemini with your API key
genai.configure(api_key="AIzaSyDzAePkx5rKlU86KoxQvjhr72UGjrMJVpQ")

# Get a list of available models
models = genai.list_models()

# Print the available models
for model in models:
    print(model)
