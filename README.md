# Local machine requirements
- ansible
- sshpass
- python3
- python3-pip

# Running tests
```
make test
```

# Deploy to RaspberryPi
1. Provide your secrets into `secrets.json`. 
1. Configure target url in `Makefile`
1. Adjust configuration variables in `ansible/roles/provision/vars/main.yml`
1. Start deployment using: 
```
make deploy
```

# File structure

```
/opt/energymeter
├── data
│   ├── main-2021-07-06.csv
│   └── solar-2021-07-06.csv
├── energymeter
│   ├── backup
│   ├── handlers
│   ├── sensor
│   └── shelly
├── logs
│   └── energymeter.log
└── requirements.txt
```

# Setup

1. Flash RaspiOS to SD card
1. Create a file named `ssh` with no content in disk root
1. Create a file named `wpa_supplicant.conf` in disk root
    ```
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=DE

    network={
    ssid="siegNetz 2,4GHz"
    psk="***"
    }
    ```