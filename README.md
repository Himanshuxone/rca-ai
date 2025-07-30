## System analysis
```shell
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
```

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

### Install Grafana
```shell
himanshu@himanshu-ThinkPad-E15:~$ sudo apt-get install grafana
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following NEW packages will be installed:
  grafana
0 upgraded, 1 newly installed, 0 to remove and 281 not upgraded.
Need to get 0 B/175 MB of archives.
After this operation, 649 MB of additional disk space will be used.
Selecting previously unselected package grafana.
(Reading database ... 302884 files and directories currently installed.)
Preparing to unpack .../grafana_12.0.2-01_amd64.deb ...
Unpacking grafana (12.0.2-01) ...
Setting up grafana (12.0.2-01) ...
### NOT starting on installation, please execute the following statements to configure grafana to start automatically using systemd
 sudo /bin/systemctl daemon-reload
 sudo /bin/systemctl enable grafana-server
### You can start grafana-server by executing
 sudo /bin/systemctl start grafana-server

```
### Grafana

nstall Grafana
Grafana can be installed on many different operating systems. For a list of the minimum hardware and software requirements, as well as instructions on installing Grafana, refer to Install Grafana.

Sign in to Grafana
To sign in to Grafana for the first time:

Open your web browser and go to http://localhost:3000/.

The default HTTP port that Grafana listens to is 3000 unless you have configured a different port.

On the sign-in page, enter admin for both the username and password.

Click Sign in.

If successful, you’ll see a prompt to change the password.

Click OK on the prompt and change your password.

### Creating tables 
From the backend run create_tables.py
```shell
python create_tables.py
```

### Stopping all containers
docker-compose down -v
docker container prune -f
docker network prune -f
docker-compose up --build
Restart the services:
docker-compose up -d

### Killing a container
sudo systemctl restart docker.socket docker.service
sudo docker image rm -f $(sudo docker image ls -q)
