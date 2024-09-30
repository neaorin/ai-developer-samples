# Laborator #1

Acest laborator vă va ajuta să vă familiarizați cu următoarele concepte:

- Utilizarea Azure Open AI Service prin apeluri REST și prin intermediul SDK-ului
- Crearea de interfețe grafice în Python folosind Streamlit
- Folosirea librăriei LangChain pentru dezvoltarea de aplicații bazate pe LLM-uri

## Setup

### Componente necesare

- Python 3.10+
- O subscripție de Azure ([free trial](https://azure.microsoft.com/en-in/pricing/offers/ms-azr-0044p))
- Un deployment de [Azure Open AI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal) în această subscripție
- Un deployment de [Azure AI Search Service](https://learn.microsoft.com/en-us/azure/search/search-create-service-portal) în această subscripție
- (opțional) un IDE sau editor de text

### Python virtual environment (opțional)

Se recomandă utilizarea unui [Python virtual environment](https://docs.python.org/3/library/venv.html) pentru a ține separate librăriile folosite în acest laborator de instalarea default de Python.

Pentru crearea unui virtual environment, urmați acești pași:

- asigurați-vă că sunteți în directorul `lab-01`:

```
cd lab-01
```

- creați environmentul:

```
python -m venv .venv
```

- activați environmentul:

Windows:
```
.venv\Scripts\activate.bat
```

OSX / Linux:
```
source .venv/bin/activate
```

Dacă ați făcut totul corect, ar trebui să aveți un prompt care indică faptul că environmentul a fost activat:

```
(.venv) C:\...\lab-01>
```

### Instalați librăriile necesare

Pentru a instala librăriile folosite de exemplele din acest laborator folosiți comanda:

```
pip install -r requirements.txt
```

### Faceți deployment-uri de modele în Azure Open AI
Din portalul de Azure Open AI, creați deployment-uri de modele:
- un model de chat (de exemplu `gpt-4o`)
- un model de embeddings (de exemplu `text-embedding-ada-002`)

### Configurați parametrii de acces la serviciile Azure

Faceți o copie a fișierului `.env.sample` și denumiți-o `.env`.

În fișierul `.env` completați parametrii de acces la serviciile Azure. Puteți găsi în [portalul Azure](https://portal.azure.com/) informațiile relevante (endpoint, access key) pentru fiecare serviciu.

```
# Setari de acces la serviciile Azure

# Azure Open AI Service
AZURE_OPENAI_API_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME=

# Azure AI Search Service
AZURE_SEARCH_API_ENDPOINT=
AZURE_SEARCH_API_KEY=
```

![Finding Azure Open AI Service Endpoint and Key](https://user-images.githubusercontent.com/26411726/225185239-6d1f3058-531c-4c7e-9496-8c2956d23f5d.png)

## Laborator

Continuați cu primul exemplu din acest laborator, `01-demo-azure-openai-rest-api.py`

```
python 01-demo-azure-openai-rest-api.py
```