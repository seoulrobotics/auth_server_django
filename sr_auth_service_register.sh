#!/bin/sh
BASEDIR=$(dirname "$0")
sudo cp $BASEDIR/sr_auth.service /etc/systemd/system/sr_auth.service
sudo systemctl daemon-reload
sudo systemctl stop sr_auth.service
sudo systemctl start sr_auth.service

