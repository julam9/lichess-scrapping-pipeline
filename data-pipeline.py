from functions import *
import time 
import datetime

print("Starting data pipeline at", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("-------------------------------------------------")
      
# Get record of top 10 classic players
t0 = time.time() 
getrecord_classical()
t1 = time.time()
print("Classical players record done")
print("----> Classical players record collected in", str(t1-t0), "seconds", "\n")

# Get record of top 10 rapid players
t0 = time.time() 
getrecord_rapid()
t1 = time.time()
print("Rapid players record done")
print("----> Rapid players record collected in", str(t1-t0), "seconds", "\n")

# Get record of top 10 blitz players
t0 = time.time() 
getrecord_blitz()
t1 = time.time()
print("Blitz players record done")
print("----> Blitz players record collected in", str(t1-t0), "seconds", "\n")

# Get record of top 10 bullet players
t0 = time.time() 
getrecord_bullet()
t1 = time.time()
print("Bullet players record done")
print("----> Bullet players record collected in", str(t1-t0), "seconds", "\n")

# Get record of top 10 ultra bullet players
t0 = time.time() 
getrecord_ultrabullet()
t1 = time.time()
print("Ultra bullet players record done")
print("----> Ultra bullet players record collected in", str(t1-t0), "seconds", "\n")