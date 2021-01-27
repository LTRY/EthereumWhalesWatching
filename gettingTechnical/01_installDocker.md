# 01 . Installation de docker sur MacOS

### Objectifs

- Comprendre pourquoi Docker est-il si important pour notre projet
- Installer docker sur MacOS

---

## 1. Why Docker?

Docker est un outil qui peut empaqueter une application et ses dépendances dans un ou plusieurs conteneurs isolés, qui pourrait être exécuté sur n'importe quel serveur, de n'importe quelle distribution.
On parle de conteneurisation, une machine virtuelle très légère qui s'appuie sur certaines parties de la machine hôte pour son fonctionnement.
Ainsi, faire fonctionner notre solution avec Docker voudrait dire la rendre flexible et portative. La blockchain ethereum et les données associées peuvent être stockées sur un disque dur qui peut être branché, débranché et rebranché sur n'importe quelle machine, et la solution continuerait de fonctionner. C'est aussi une facon à faire de sorte que le projet puisse être repris par d'autres plus facilement. 


## 2. Docker on Mac

Le but ici n'est pas forcément de montrer comment installer docker sur sa machine locale, je note juste les commandes qui m'ont permis d'obtenir le résultat qui fait fonctionner la solution du projet sur mon ordinateur. 
Le guide suivant se trouve ici: https://medium.com/crowdbotics/a-complete-one-by-one-guide-to-install-docker-on-your-mac-os-using-homebrew-e818eb4cfc3

```shell script
~ docker-machine create --driver virtualbox default
Creating CA: /Users/louistiercery/.docker/machine/certs/ca.pem
Creating client certificate: /Users/louistiercery/.docker/machine/certs/cert.pem
Running pre-create checks...
(default) Image cache directory does not exist, creating it at /Users/louistiercery/.docker/machine/cache...
(default) No default Boot2Docker ISO found locally, downloading the latest release...
(default) Latest release for github.com/boot2docker/boot2docker is v19.03.12
(default) Downloading /Users/louistiercery/.docker/machine/cache/boot2docker.iso from https://github.com/boot2docker/boot2docker/releases/download/v19.03.12/boot2docker.iso...
(default) 0%....10%....20%....30%....40%....50%....60%....70%....80%....90%....100%
Creating machine...
(default) Copying /Users/louistiercery/.docker/machine/cache/boot2docker.iso to /Users/louistiercery/.docker/machine/machines/default/boot2docker.iso...
(default) Creating VirtualBox VM...
(default) Creating SSH key...
(default) Starting the VM...
(default) Check network to re-create if needed...
(default) Found a new host-only adapter: "vboxnet0"
(default) Waiting for an IP...
Waiting for machine to be running, this may take a few minutes...
Detecting operating system of created instance...
Waiting for SSH to be available...
Detecting the provisioner...
Provisioning with boot2docker...
Copying certs to the local machine directory...
Copying certs to the remote machine...
Setting Docker configuration on the remote daemon...
Checking connection to Docker...
Docker is up and running!
To see how to connect your Docker Client to the Docker Engine running on this virtual machine, run: docker-machine env default
```

```shell script
~ docker-machine ls
NAME      ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER      ERRORS
default   -        virtualbox   Running   tcp://192.168.99.100:2376           v19.03.12   
```

```shell script
~ docker-machine env default
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.100:2376"
export DOCKER_CERT_PATH="/Users/louistiercery/.docker/machine/machines/default"
export DOCKER_MACHINE_NAME="default"
# Run this command to configure your shell: 
# eval $(v2-machine env default)
Creating CA: /Users/louistiercery/.docker/machine/certs/ca.pem
```

```shell script
~ eval $(docker-machine env default)
```

`CONCLUSION`: nous avons docker sur notre machine et allons pouvoit monter un container geth afin de récupérer la blockchain ethereum. 



`NOTE`:
- A noté que ceci est l'ancienne facon d'installer Docker, depuis une installation par UI est proposé par Docker

`SOURCE`:
- https://docs.cancergenomicscloud.org/docs/mount-a-usb-drive-in-a-docker-container
- https://www.tecmint.com/run-docker-container-in-background-detached-mode/
- https://www.maketecheasier.com/copy-move-docker-container-to-another-host/
- https://blog.container-solutions.com/understanding-volumes-docker
