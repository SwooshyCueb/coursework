#!/bin/bash

#Parts of this script are adapted from the scripts in this blog post
#https://www.invisiblethreat.ca/2014/09/cve-2014-6271/

if [ "`whoami`" != "root" ]; then
	echo "Must run as root."
	exit 1
fi

if [ ! -e disk1.img ]; then

	if [ ! -e ubuntu-14.04-server-cloudimg-amd64-disk1.img ]; then
		wget http://cloud-images.ubuntu.com/releases/14.04.1/release-20140829/ubuntu-14.04-server-cloudimg-amd64-disk1.img
	fi

	qemu-img create -f qcow2 -b ubuntu-14.04-server-cloudimg-amd64-disk1.img disk1.img

fi


if [ ! -e cidisk.img ]; then

	if [ ! -e meta-data ]; then
		echo "instance-id: shellshock-55755" > meta-data
		echo "local-hostname: shellshock" >> meta-data
	fi

	if [ ! -e user-data ]; then
		echo "#cloud-config" > user-data
		echo "password: thispasswordissomewhatsecure" >> user-data
		echo "chpasswd: { expire: False }" >> user-data
		echo "ssh_pwauth: True" >> user-data
		echo "sudo: ALL=(ALL) NOPASSWD:ALL" >> user-data
		echo "ssh_import_id: SwooshyCueb" >> user-data
        echo "write_files:" >> user-data
        echo "  - path: /var/www/html/flag" >> user-data
        echo "    permissions: 0664" >> user-data
        echo "    owner: www-data" >> user-data
        echo "    content: |" >> user-data
        echo "        You should be able to remove this file if this system is succeptible to shellshock." >> user-data
        echo "        " >> user-data
        echo "  - path: /var/www/html/envvars.cgi" >> user-data
        echo "    permissions: 0774" >> user-data
        echo "    owner: www-data" >> user-data
        echo "    content: |" >> user-data
        echo "        #!/bin/bash" >> user-data
        echo '        echo "Content-type: text/html"' >> user-data
        echo '        echo ""' >> user-data
        echo "        echo '<html>'" >> user-data
        echo "        echo '<head>'" >> user-data
        echo "        echo '<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">'" >> user-data
        echo "        echo '<title>Environment variables</title>'" >> user-data
        echo "        echo '</head>'" >> user-data
        echo "        echo '<body>'" >> user-data
        echo "        echo '<pre>'" >> user-data
        echo "        /usr/bin/env" >> user-data
        echo "        echo '</pre>'" >> user-data
        echo "        echo '</body>'" >> user-data
        echo "        echo '</html>'" >> user-data
        echo "        exit 0" >> user-data
        echo "        " >> user-data
        echo "  - path: /etc/apache2/conf-available/cgi-everywhere.conf" >> user-data
        echo "    permissions: 0644" >> user-data
        echo "    owner: root:root" >> user-data
        echo "    content: |" >> user-data
        echo "        AddHandler cgi-script .cgi .pl" >> user-data
        echo "        <Directory /var/www/html>" >> user-data
        echo "            Options +ExecCGI" >> user-data
        echo "        </Directory>" >> user-data
        echo "        " >> user-data
        echo "runcmd:" >> user-data
        echo "  - [ apt-get, install, apache2, -y ]" >> user-data
        echo "  - [ ln, -s, /etc/apache2/mods-available/cgi.load, /etc/apache2/mods-enabled/cgi.load ]" >> user-data
        echo "  - [ chown, -R, www-data, /var/www ]" >> user-data
        echo "  - [ ln, -s, /etc/apache2/conf-available/cgi-everywhere.conf, /etc/apache2/conf-enabled/cgi-everywhere.conf ]" >> user-data
        echo "  - [ sleep, 30 ]" >> user-data
        echo "  - [ service, apache2, restart ]" >> user-data
	fi

	if [ ! -e cloud-localds ]; then
		wget http://bazaar.launchpad.net/~cloud-utils-dev/cloud-utils/trunk/download/head:/cloudlocalds-20120823015036-zkgo0cswqhhvener-1/cloud-localds
		chmod +x cloud-localds
	fi

	./cloud-localds cidisk.img user-data meta-data

fi

if [ ! -e qemu-ifup ]; then
	cp /etc/qemu-ifup qemu-ifup
	sed -i -e "s/awk '\/^default \/ {/awk '{/g" qemu-ifup
	sed -i -e "s/}'/}' \| sort \| uniq/g" qemu-ifup
fi




/usr/bin/qemu-system-x86_64 \
	-enable-kvm \
	-machine pc-i440fx-trusty,accel=kvm,usb=off \
	-cpu SandyBridge -m 1024 -realtime mlock=off \
	-smp 1,sockets=1,cores=1,threads=1 \
	-chardev socket,id=charmonitor,path=/var/lib/libvirt/qemu/linux.monitor,server,nowait \
	-mon chardev=charmonitor,id=monitor,mode=control \
	-rtc base=utc,driftfix=slew -global kvm-pit.lost_tick_policy=discard \
	-no-hpet -no-shutdown -global PIIX4_PM.disable_s3=1 -global PIIX4_PM.disable_s4=1 \
	-boot strict=on \
	-device virtio-serial-pci,id=virtio-serial0,bus=pci.0,addr=0x6 \
	-drive file=disk1.img,if=none,id=maindisk,format=qcow2 \
	-device virtio-blk-pci,scsi=off,bus=pci.0,addr=0x8,drive=maindisk,id=virtio-disk0,bootindex=1 \
	-drive file=cidisk.img,if=none,id=cidisk,format=raw \
	-device virtio-blk-pci,scsi=off,bus=pci.0,addr=0x9,drive=cidisk,id=virtio-disk1 \
	-netdev tap,ifname=vnet0,id=hostnet0,vhost=on,script=qemu-ifup \
	-device virtio-net-pci,netdev=hostnet0,id=net0,mac=52:54:00:4e:75:94,bus=pci.0,addr=0x3 \
	-device virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x7
