
### J'ai essayé de monter un noeud eth sur ma raspberry pi, par ici il y a un peu de note

Mais! Mais.. Ça n'a pas marché, mon intuition du pourquoi du comment c'est:  
    le pi avait 2GB de mémoire et il semblerait que la configuration minimal requise soit 4GB
    


```zsh
diskutil list  
...
/dev/disk2 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *15.9 GB    disk2
   1:             Windows_FAT_32 system-boot             268.4 MB   disk2s1
   2:                      Linux                         15.7 GB    disk2s2

```

```zsh
diskutil unmountDisk /dev/disk2
Unmount of all volumes on disk2 was successful
```

```zsh
sudo sh -c 'gunzip -c ~/Downloads/ubuntu-20.04.1-preinstalled-server-arm64+raspi.img.xz | sudo dd of=/dev/disk2 bs=32m'
0+49844 records in
0+49844 records out
3250824192 bytes transferred in 735.012126 secs (4422817 bytes/sec)
```
