##Coding

the file ClientMachine, ServerMachine in ir.sharif.ce.partov.machine is for you to place your code.
you can add or change all files in ir.sharif.ce.partov.machine package.
do not change files in other packages.

## Installation

change your directory to here.
and then just run **make** to compile the code. The CF does not have any special dependency and should be compilable on most Linux systems.

## Usage

change your directory to here
put your information into **info.h**

to prevent any access by other users. Then you can use three other scripts as follows:

  - The **new.sh** for instantiating a new topology,
  - The **free.sh** for releasing the previously assigned topology instance,
    * Do not forget to free the instance when your simulation finished (required for log files flushing).
  - The **run.sh** for connecting your program to configured virtual node (if any).

## Resources

You can read **CFManual.pdf** for a more complete guide to CF.

## Archive
to make an archive, run **make archive** and this make a zip file of your codes.
please double check this zip to contains all of your important files.
