# lightning-cube
Code associate with the Lightning Cube art project.

Installation on Raspian
---

Copy the code down to the device. Careful the code currently assume the
location of audio files so this needs to go in /home/pi/lightning-cube. The
following command in the home dir should accomplish this.

   git clone https://github.com/mmachenry/lightning-cube.git

Copy the init script and initialize it to start on boot.

   sudo cp lightning-cube/lightning-cube.sh /etc/init.d/
   sudo update-rc.d lightning-cube.sh defaults

Citations
---
We adapted code from [OneGuyOneBlog](https://oneguyoneblog.com/2017/11/01/lightning-thunder-arduino-halloween-diy/) when starting this project. We also added audio by [Daniel Simion](http://soundbible.com/2217-Heavy-Rain-Wind.html). We also followed a simple startup script by [SCPhillips](http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/)
This library from [99sounds](http://99sounds.org/rain-and-thunder/) has some good stuff.
