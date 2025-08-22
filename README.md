seu_dashboard/
├─ app.py
├─ pages/
│  ├─ 01_Visão_Geral.py
│  ├─ 02_Análises.py
│  └─ 99_Configurações.py
├─ src/
│  ├─ data/
│  │  ├─ loader.py
│  │  └─ transforms.py
│  ├─ services/
│  │  ├─ db.py
│  │  └─ config.py
│  ├─ charts/
│  │  ├─ lines.py
│  └─ ui/
│     ├─ layout.py            header, sidebar, containers
│     └─ widgets.py           filtros, inputs e formulários
├─ assets/                    logos, ícones, CSS opcional
├─ config.yml                 variáveis do app (ex.: datas padrão)
├─ requirements.txt
├─ README.md
└─ .streamlit/
   ├─ config.toml             tema/toolbar
   └─ secrets.toml            credenciais (NÃO versionar)