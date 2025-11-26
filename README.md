# Blackjack 2

**Blackjack 2** is a minimalist, single‑player web blackjack game built with Flask. It allows a player to play up to three hands versus an AI dealer. The app runs without a database, using Flask sessions to maintain game state. It is deployable with Gunicorn + nginx on a Linux server (an Ubuntu laptop in my case).

Note: sessions are ephemeral. Game state is lost on server restarts or if cookies/sessions expire.


<!--TOC-->

- [Blackjack 2](#blackjack-2)
  - [Features](#features)
  - [Running Locally (Development)](#running-locally-development)
    - [Deployment with Gunicorn and nginx](#deployment-with-gunicorn-and-nginx)
    - [Deployment Notes](#deployment-notes)
  - [Configuration](#configuration)
  - [Roadmap](#roadmap)
    - [TODO](#todo)
    - [Later features (after MVP deployment)](#later-features-after-mvp-deployment)
  - [Contributing & License](#contributing--license)

<!--TOC-->

---

## Features

- Start a new game immediately from the static homepage
- Play up to **three hands** in parallel
- Standard blackjack rules: hit, stand, dealer hits until 17+
- No external database or long‑term persistence
- Simple, clean UI with HTML/CSS
- Lightweight architecture suitable for running on modest hardware

---

## Running Locally (Development)

1. **Clone** the repository
  ```bash
git clone https://github.com/bitnathan/blackjack2.git
cd blackjack2
```

2. Create Virtual Environment
```bash
python3 -m venv env
source env/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set Environmental Variables
5. Run in development mode
```bash
flask run
```
6. Run Tests
```bash
./test.sh
```

### Deployment with Gunicorn and nginx
1. Install and set up project as above.
2. Set up Gunicorn service
```ini
[Unit]
Description=Gunicorn instance for Blackjack2
After=network.target

[Service]
User=youruser
Group=www-data
WorkingDirectory=/path/to/blackjack2
Environment="PATH=/path/to/blackjack2/env/bin"
ExecStart=/path/to/blackjack2/env/bin/gunicorn --config gunicorn_config.py wsgi:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start blackjack2
sudo systemctl enable blackjack2
```


3. Configure nginx
*this depends on your deployment setup, for example https is generally hosted on port 443 as opposed to http on port 80*

```nginx
server {
    listen 80;
    server_name your.domain.com;  # or your IP if exposing

    location / {
        proxy_pass http://127.0.0.1:8000;  # or the port Gunicorn listens on
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/blackjack2/app/web/static;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/blackjack2 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

4. Firewall / port forwarding
Ensure port 80 (HTTP) is open on your server/laptop. If hosting behind NAT/router, forward external port to your laptop’s internal IP.


### Deployment Notes

Logs: you can examine Gunicorn logs, systemd logs (journalctl -u blackjack2), and nginx logs for errors.

You may configure SSL (Let’s Encrypt) later if you expose publicly.

## Configuration

In environment variables (inserted via app/config.py) you may define:

- SECRET_KEY — used to sign session cookies

- SESSION_PERMANENT / PERMANENT_SESSION_LIFETIME — controlling cookie/session expiration

- DEBUG, TESTING flags

- Gunicorn configuration (workers, bind address) in gunicorn_config.py

- You can add a sample .env or .flaskenv file (excluded via .gitignore) for local development.

## Roadmap

### TODO

1. game logic, playable via terminal localy 
3. local flask api hosting to play game via postman as needed
4. create static home / new game homepage (could also design to use SPA, design decision)
5. create views / templates for web use
6. deploy via gunicorn / nginx

##### Current status / immediate todos
_create service layer to call game actions and set up api blueprint to call service layer, providing full local API playability_

After that we'll be able to have a single player play blackjack over an API... next step will be using some sort of game id stored in service layer to save active game states and allow several people to play simultaneously

### Later features (after MVP deployment)
Allow splitting (when player’s two cards are same rank)

Allow double down, insurance, surrender

Github Actions CI/CD integration

Track statistics via JSON file or SQLite persistence

Improve UI/UX with JavaScript (AJAX actions, dynamic hand updates)

Add theming, mobile responsiveness, better visuals

Configure logging, monitoring, error reporting

Deploy to a cloud and/or Docker container for portability and easier deployment

## Contributing & License

Contributions are welcome!
Please fork and submit pull requests.
Include tests for new logic, ensure code style consistency.

