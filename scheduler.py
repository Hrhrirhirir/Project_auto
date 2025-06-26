import schedule
import time
import subprocess

def job():
    subprocess.run(["python3", "main.py"])

schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)