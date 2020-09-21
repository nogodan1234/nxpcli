nxpcli: Nutanix API client for devops(Prism Central)
#############################################

This readme file is specifically for the **nxcli** program.

The setup instructions are the same as all other python program in this repository.  This file is provided as additional/supplemental program for this specific user purpose.

Please see the `main <https://github.com/nutanixdev/code-samples/tree/master/python>`_ page for general instructions.

**Usage instructions are shown at the bottom of this page.**

Code Sample Details
...................

A quick intro, first.  The **nxpcli** program can be used for simple nutanix cluster operation from cli.  The expectation is that users wanting to do nutanix cluster operation without Prism Central UI access.  For example:

- Get various entity information - cluster,host,vm,image,network etc from remote
- Deploy Karbon cluster 

**nxpcli** has been provided for devopslish operation something similar awscli or azurecli against nutanix prism central:

- this program requires to have "nxapilibv3.py" file in same directory as a method library
- python3 and various optional python pkgs are required to install prior to execute, you can check from import sentence in source file - or error msg you get :)

Usage
-----

.. code-block:: bash

   usage: ./nxpcli

    Be aware you are in $YOUR_CLUSTER_NAME cluster($CLUSTR_VIP) as $CLUSTER_USER user
    What kind of operation do you want?

    #### MENU ####

    Type 1: Cluster info
    Type 2: Host info
    Type 3: Vm info
    Type 4: Image info
    Type 5: Project info
    Type 6: Network info
    Type 7: Directory Service info
    Type 8: Role info
    Type 9: Alert info
    Type 10: User info
    Type 11: New cluster setup - EULA,Pulse,NTP etc
    Type 12: Deploy Karbon Cluster(Not Working) - Flannel
    Type 13: Deploy Karbon Cluster - Calico
    Type 14: List Karbon Cluster
    Type 15: Delete Karbon Cluster
    Type q: Exit program

.. code-block:: bash
   if this was the first time executed, it will ask for cluster detail:
   or it will use saved cluster configuration under your home directory( ~/.nx/pcconfig)
   