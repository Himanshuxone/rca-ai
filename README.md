## System analysis

techrca/
├── frontend/ # React + Tailwind
│ └── components/
│ └── pages/
│ └── utils/
├── backend/ # FastAPI app
│ └── api/
│ └── services/
│ └── models/
│ └── pipelines/ # RCA pipeline logic
├── ai_engine/ # Prompt, LLM, embeddings
│ └── prompts/
│ └── embedding.py
│ └── rca_analyzer.py
├── storage/ # S3 interface
├── infra/ # Docker, GitHub Actions, Terraform (optional)
└── docs/ # API docs, pitch deck, team info

### React Home Page
- A Home page to upload logs and get RCA summaries
- A Report page to fetch RCA reports by ID
- A reusable Dark Mode toggle that persists across sessions
- A styled UI using CSS with light/dark theme support

### Details of each component
🔧 What Each Part Does
🔸 backend/
FastAPI app logic
OpenAI API call
SQLAlchemy models
/analyze and /report/{id} endpoints
🔸 frontend/
React UI for uploading logs & viewing reports
Dark mode toggle
API calls to FastAPI backend via proxy
Dockerfile to serve React via Nginx
🔸 docker-compose.yml
Orchestrates backend, frontend, and Postgres
Ensures networked containers
🔸 nginx.conf
Enables SPA routing in production (e.g., /report, /dashboard won’t 404)
🔸 requirements.txt (backend)

### Build and run
```shell
docker build -t techrca-frontend .
docker run -p 3000:80 techrca-frontend
```

### Start node server
```shell
# 1. Install dependencies
npm install
# 2. Start the development server
npm start
```

### Using Database
```shell
sudo apt install postgresql
sudo apt install postgresql-client
```
