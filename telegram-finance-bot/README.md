
```
docker build -t tgfinance ./
docker run -d --name tg -v /local_project_path/db:/home/db tgfinance

docker exec -ti tg bash

docker exec -ti tg bash
sqlite3 /home/db/finance.db
```

```bash
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

```bash
source ./env/bin/activate

TG_API_ID=... \
    TG_API_HASH=... \
    TG_BOT_TOKEN=... \
    TG_CHANNEL_ID=... \
    python fix-donate-tg-chat.py
```


