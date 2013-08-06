#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

#define DRIVER_AUTHOR "Radu Traian Jipa, <radu.t.jipa@gmail.com>"
#define DRIVER_DESC   "A simple driver to expose the RPi system timer to /dev"


static int hello_init (void)
{
	printk(KERN_ALERT "Hello world!\n") ;
	return 0 ;
}


static void hello_exit (void)
{
	printk(KERN_ALERT "Goodbye, cruel world!\n") ;
}

module_init(hello_init) ;
module_exit(hello_exit) ;


/*  */
//MODULE_LICENCE ("GPL") ;

/*  */
MODULE_AUTHOR (DRIVER_AUTHOR) ;
MODULE_DESCRIPTION (DRIVER_DESC) ;
