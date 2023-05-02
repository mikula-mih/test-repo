
# Systemd, nginx, gunicorn.

```bash
./install.sh
# set up `src/config/settings.py`
sudo systemctl status gunicorn
# gunicorn/access.log
# gunicorn/error.log
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```
