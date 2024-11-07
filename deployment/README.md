
# Deployment of the web application in a web server

### Requirements
- [Python 3.9+](https://www.python.org/)
- [nginx](https://nginx.org/en/)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [Flamapy](https://www.flamapy.org/)
- [D3.js](https://d3js.org/)

### Download and install
1. Install [Python 3.9+](https://www.python.org/)
2. Install [nginx](https://nginx.org/en/)
3. Create a folder `/var/www/fmfactlabel/`
4. Clone this repository and enter into the main directory:

    `git clone https://github.com/jmhorcas/fm_characterization`

5. Create a virtual environment: 
   
   `python -m venv env`

6. Activate the environment: 
   
   `. env/bin/activate`
   
7. Install the dependencies: 
   
   `pip install -r requirements.txt`

   `sudo apt install build-essential`
   
   `sudo apt install libgmp3-dev`


8. Create a configuration file for the virtual website:
Create the following file `/etc/nginx/sites-available/fmfactlabel.conf`:

```
server {
        listen 80;
        server_name _;

        access_log /var/log/nginx/fmfactlabel.access.log;
        error_log /var/log/nginx/fmfactlabel.error.log;

        location / {
                include proxy_params;
                proxy_pass http://unix:/var/www/fmfactlabel/fm_characterization/fmfactlabel.sock;
        }
}
```

9. Activar el sitio web:

9.1. Crear enlace simbólico: `sudo ln -s /etc/nginx/sites-available/fmfactlabel /etc/nginx/sites-enabled/`
9.2. Verificar la configuración de nginx: `sudo nginx -t`
9.3. Reiniciar nginx: `sudo systemctl reload nginx` 

1.  Create a service to run the application:
Create the following file `/etc/systemd/system/fmfactlabel.service`:

```
[Unit]
Description=fmfactlabel.service - A Flask application run with Gunicorn.
After=network.target

[Service]
User=usuario
Group=usuario
Environment="PATH=/var/www/fmfactlabel/env/bin"
WorkingDirectory=/var/www/fmfactlabel/fm_characterization/
ExecStart=/var/www/fmfactlabel/env/bin/gunicorn --workers 3 --bind unix:/var/www/fmfactlabel/fm_characterization/fmfactlabel.sock run:app --error-logfile /home/usuario/fmfactlabel/gunicorn.error.log --capture-output --log-level debug

[Install]
WantedBy=multi-user.target
```

### Execution
To manange the service use the following commands:

- To start the service: `sudo systemctl start fmfactlabel`
- To restart the service `sudo systemctl restart fmfactlabel`
- To stop the service `sudo systemctl stop fmfactlabel`
- To check the status of the service `systemctl status fmfactlabel`

Access to the web application:

https://fmfactlabel.adabyron.uma.es/
