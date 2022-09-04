# BUILD USE PYTHON 3.6
# INSTALL
python3 setup.py install

# BUILD TO .rpm
python3 setup.py bdist --format=rpm

# CHECK BEFORE BUILD
python3 beapicrawling.py start

# CREATE SYSTEMED
    1. nano /etc/systemd/system/nama.service
    2. chomod 640 /etc/systemd/system/nama.service
    3. systemctl status nama
    4. systemctl start nama
    5. systemctl stop nama

# [nama.SERVICE]



# UBUNTU (.DEB)
[Unit]
Description=API SERVICE CRAWLING

Wants=network.target
After=syslog.target network-online.target

[Service]
Type=simple
ExecStart=fakhrilak start
Restart=on-failure
RestartSec=10
KillMode=process

[Install]
WantedBy=multi-user.target

# CENTOS 7 (.RPM)
Description=API SERVICE CRAWLING

Wants=network.target
After=syslog.target network-online.target

[Service]
Type=simple
ExecStart= /bin/bash /path/to/start
Restart=on-failure
RestartSec=10
KillMode=process

[Install]
WantedBy=multi-user.target