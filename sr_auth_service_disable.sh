#!/bin/sh
sudo systemctl daemon-reload
sudo systemctl stop sr_auth.service
sudo systemctl disable sr_auth.service

