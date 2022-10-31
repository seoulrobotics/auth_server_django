#!/bin/sh
sudo cp sr_auth.service /etc/systemd/system/sr_auth.service
sudo systemctl daemon-reload
sudo systemctl stop sr_auth.service
sudo systemctl start sr_auth.service

