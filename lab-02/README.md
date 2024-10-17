# Laborator 2

Exercitii practice cu Function Calling, Autogen, Autogen Studio

## Setup

### Componente necesare

- Python 3.10+
- O subscripție de Azure ([free trial](https://azure.microsoft.com/en-in/pricing/offers/ms-azr-0044p))
- Un deployment de [Azure Open AI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal) în această subscripție
- (opțional) un IDE sau editor de text

### Python virtual environment (opțional)

Se recomandă utilizarea unui [Python virtual environment](https://docs.python.org/3/library/venv.html) pentru a ține separate librăriile folosite în acest laborator de instalarea default de Python.

Pentru crearea unui virtual environment, urmați acești pași:

- asigurați-vă că sunteți în directorul `lab-02`:

```
cd lab-02
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
(.venv) C:\...\lab-02>
```

### Instalați librăriile necesare

Pentru a instala librăriile folosite de exemplele din acest laborator folosiți comanda:

```
pip install -r requirements.txt
```

### Faceți deployment-uri de modele în Azure Open AI
Din portalul de Azure Open AI, creați deployment-uri de modele:
- un model de chat (de exemplu `gpt-4o`)

### Configurați parametrii de acces la serviciile Azure

Faceți o copie a fișierului `.env.sample` și denumiți-o `.env`.

În fișierul `.env` completați parametrii de acces la serviciile Azure. Puteți găsi în [portalul Azure](https://portal.azure.com/) informațiile relevante (endpoint, access key) pentru fiecare serviciu.

```
# Setari de acces la serviciile Azure

# Azure Open AI Service
AZURE_OPENAI_API_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=

# Bing Search API Key
BING_API_KEY=
```

![Finding Azure Open AI Service Endpoint and Key](https://user-images.githubusercontent.com/26411726/225185239-6d1f3058-531c-4c7e-9496-8c2956d23f5d.png)

## Open AI Functions

Continuați cu primul exemplu din acest modul, `01-exercise-functions.py`

```
streamlit run 01-exercise-functions.py
```

## Autogen Studio

Pentru a rula Autogen Studio, executați comanda

```
autogenstudio ui --port 8081
```

După pornirea aplicației o puteți accesa la adresa http://localhost:8081/