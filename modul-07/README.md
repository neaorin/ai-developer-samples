# Modulul 7 - Extensibilitate

Extensibilitate pentru LLM-uri - Function Calling

## Setup

### Componente necesare

- Python 3.10+
- O subscripție de Azure ([free trial](https://azure.microsoft.com/en-in/pricing/offers/ms-azr-0044p))
- Un deployment de [Azure Open AI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal) în această subscripție
- (opțional) un IDE sau editor de text

### Python virtual environment (opțional)

Se recomandă utilizarea unui [Python virtual environment](https://docs.python.org/3/library/venv.html) pentru a ține separate librăriile folosite în acest laborator de instalarea default de Python.

Pentru crearea unui virtual environment, urmați acești pași:

- asigurați-vă că sunteți în directorul `modul-07`:

```
cd modul-07
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
(.venv) C:\...\modul-07>
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
```

![Finding Azure Open AI Service Endpoint and Key](https://user-images.githubusercontent.com/26411726/225185239-6d1f3058-531c-4c7e-9496-8c2956d23f5d.png)

## Exemple

Continuați cu primul exemplu din acest modul, `01-demo-functions.py`

```
streamlit run 01-demo-functions.py
```