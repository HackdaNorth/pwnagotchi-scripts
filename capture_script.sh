sudo mkdir /home/pi/handshakes
root@Sandori:~# sudo cp ~/handshakes/* /home/pi/handshakes/
scp -o IdentitiesOnly=yes -r -i ./id_ed25519 pi@10.0.0.2:/home/pi/handshakes/*  ./handshakes/pcap
