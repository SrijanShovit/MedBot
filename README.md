# PubMed Q&A App 📚🔍

PubMed Q&A App is a project designed to provide a user-friendly interface for querying biomedical literature using PubMed and Haystack. It leverages advanced natural language processing techniques to generate high-quality answers to medical-related questions.

---

## Features 🚀

- **Web UI**: 🌐 Gradio UI for users to input their questions.
- **Smooth Pipeline**: 📚 Utilizes Haystack as coordinator and PubMed as database to fetch and summarize relevant articles.
- **Response Generation**: 💭 Mistral-7B-Instruct-v0.2 model generates response to the best of its capability surprising users.
- **Prompt Templating**: ✍️ Guides the model to answer queries based on some generic keywords, enhancing the accuracy.
- **Cache/Data Persistence/Optimization**: 💾 Implements caching to store recent queries for faster response times and reduced API calls to PubMed.

***Cache Optimization***

Model API calls can be resource-intensive. To optimize performance and reduce API usage, the app implements a caching mechanism. Recent queries and their corresponding responses are cached. This significantly improves response times, especially for frequently asked questions, and reduces the load on the Model.

## Performance Comparison

Response Time in seconds is used as the metric.

First time request  | Second time request served by cache
------------- | -------------
8-25   | <<< 1 (almost negligible)

---

## Technologies Used 🛠️

- **PubMed**: 📚 A free search engine accessing primarily the MEDLINE database of references and abstracts on life sciences and biomedical topics
- **Haystack**: 🔍 A Python library that offers ready-made pipelines for most common tasks, such as question answering, document retrieval, or summarization.
- **Gradio**: 🌐 A Python library for building interactive web applications, used here to create the user interface.
- **Mistral-7B-Instruct-v0.2**: 🔐 The Mistral-7B-Instruct-v0.2 Large Language Model (LLM) is an improved instruct fine-tuned version of Mistral-7B-Instruct-v0.1.
---

## Usage 🖥️

To use the PubMed Q&A App:

1. **Clone the repository**: 📁 Clone this repository to your local machine.
2. **Install dependencies**: 💻 Install the required dependencies using pip:

   ```
   pip install -r requirements.txt
   ```

3. **Run the app**: ▶️ Run the Streamlit app:

   ```
   streamlit run med_app.py
   ```

4. **Access the app**: 🌐 Access the Gradio app in your web browser.

---
## Screenshots 📸

![Home Screen](https://github.com/SrijanShovit/MedBot/blob/main/img/home_screen.png)

---

![Q1](https://github.com/SrijanShovit/MedBot/blob/main/img/q1.png)

Response Time: 19.254008 s

![Q1 resp](https://github.com/SrijanShovit/MedBot/blob/main/img/q1_response.png)

---

![Q2](https://github.com/SrijanShovit/MedBot/blob/main/img/q2.png)

Response Time: 13.050238 s

![Q2 resp](https://github.com/SrijanShovit/MedBot/blob/main/img/q2_response.png)

Cached Response Time: 0.000000 s

![Q2_resp2](https://github.com/SrijanShovit/MedBot/blob/main/img/q2_resp2.png)

---

![Q3](https://github.com/SrijanShovit/MedBot/blob/main/img/q3.png)

Response Time: 8.883399 s

![Q3 resp](https://github.com/SrijanShovit/MedBot/blob/main/img/q3_resp.png)

---

## Contributing 🤝

Contributions to MedBot are always welcome! If you'd like to contribute, please fork the repository and submit a pull request.
