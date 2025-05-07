**RAG Chatbot**
This project is a Retrieval-Augmented Generation (RAG) chatbot that uses PDF documents as a knowledge base to answer user questions. The chatbot is built using Streamlit and various LangChain components.

**Requirements**
Python 3.8+
Streamlit
LangChain Core
LangChain Community
LangChain MistralAI
PDFPlumber
LangChain Chroma

**Installation**
Clone the repository:

```bash
git clone <repository-url>
cd rag-chatbot
```
Install the required packages:
```bash
pip install -r requirements.txt
```
**Usage**
Set up your Mistral AI API key:
```bash
export MISTRAL_API_KEY=<your-api-key>
```

Run the Streamlit app:
```bash
streamlit run app.py
```

Upload a PDF document using the file uploader in the Streamlit interface.Once the document is indexed, you can ask questions based on the content of the uploaded PDF.

**Project Structure**
app.py: Main application file.
requirements.txt: List of required Python packages.
pdf/: Directory to store uploaded PDF files.
Chroma-DB/: Directory to store the Chroma vector store.

**License**
This project is licensed under the MIT License.
