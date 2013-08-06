obj-m += system_timer.o

all:
	make -C /lib/modules/3.6-trunk-rpi/build M=$(PWD) modules

clean:
	make -C /lib/modules/3.6-trunk-rpi/build M=$(PWD) clean
