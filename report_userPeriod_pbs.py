import sys
import os
import re
from datetime import timedelta

#argv[1] : user name in name.surname
#argv[2] : name filelog - period to start
#argv[3] : name filelog - period to stop

all_files = os.listdir("/var/spool/pbs/server_logs")
files_period = []

name_ = sys.argv[1]
token=name_.split(".")
name=token[0]
surname=token[1]
time_start = sys.argv[2]
time_stop =sys.argv[3]

#the output file is in LOGS directory
if not os.path.exists("LOGS"):
    os.makedirs("LOGS")
output = open("LOGS/logs_"+time_start+"_"+time_stop+".txt", "w")

year_start=time_start[0]+time_start[1]+time_start[2]+time_start[3]
month_start=time_start[4]+time_start[5]
day_start=time_start[6]+time_start[7]

year_stop=time_stop[0]+time_stop[1]+time_stop[2]+time_stop[3]
month_stop=time_stop[4]+time_stop[5]
day_stop=time_stop[6]+time_stop[7]


output.write("REPORT from "+day_start+"/"+month_start+"/"+year_start+" to "+day_stop+"/"+month_stop+"/"+year_stop+"\n\n")

for file in all_files:
    if(file >= time_start) and (file<=time_stop):
        files_period.append(file)

cputime_total = []
walltime_total = []
total_n_jobs = 0

for file in files_period:
    print("Reading file "+str(file)+"...\n")
    output.write("\nLOG FILE: " + str(file)+"\n")
    year=file[0]+file[1]+file[2]+file[3]
    month=file[4]+file[5]
    day=file[6]+file[7]
    lines = []
    jobs = []
    jobs_and_queue = []
    with open("/var/spool/pbs/server_logs/"+file, "r") as f:
        tmp = f.read().split('\n')
        regex = r"(.*(\d{6}).*("+name+"\."+surname+").*)"
        for t in tmp:
            matches = re.finditer(regex, t)
            for matchNum, match in enumerate(matches):
                matchNum = matchNum + 1
                jobs.append(match.group(2))
    unique_jobs = sorted(list(set(jobs)))
    if unique_jobs.__len__() != 0:
        output.write("Number of jobs: " + str(unique_jobs.__len__()) + ", list of jobs: ")
        for job in unique_jobs:
            output.write(str(job)+" ")
        output.write("\n")
        flag=0
        for job in unique_jobs:
            cputime=""
            walltime=""
            with open("/var/spool/pbs/server_logs/"+file, "r") as f:
                tmp = f.read().split("\n")
                for t in tmp:
                    if job in t:
                        print("read each line\n")
                        lines.append(t)
                        tokens_line = t.split(" ")
                        if tokens_line.__len__() == 8:
                            if tokens_line[6] != "hop":
                                flag = 1
                                cputime_total.append(tokens_line[3])
                                cputime = tokens_line[3]
                                walltime = tokens_line[7]
                                walltime_total.append(walltime)
                                status_line = tokens_line[1]
                                status_tokens = status_line.split(";")
                                status = status_tokens[5]
                                status_token_val = status.split("=")
                                value = status_token_val[1]
                                # output.write("Value job " + str(value) + "\n")
                                resp = "value not defined"
                                if value == "0":
                                    resp = "job completed with success"
                                elif value == "1":
                                    resp = "job contains an error code"
                                elif value == "271":
                                    output.write("Il valore è 271\n")
                                    resp = "job has been killed manually"
                                right_queue = ""
                                for jobQ, queueQ in jobs_and_queue:
                                    if jobQ == job:
                                        right_queue = queueQ
                                output.write(
                                    "DATE " + day + "/" + month + "/" + year + ", " + "JOB: " + job + ", QUEUE: " + right_queue + ", " + str(
                                        cputime) + ", " + str(
                                        walltime) + ", status job " + status + ". It means: " + resp + "\n")
            total_n_jobs = total_n_jobs + unique_jobs.__len__()
            if flag == 0:
                output.write("There are no job that finished in current file\n")
        else:
            output.write("There are no jobs in current file\n")
        output.write("\n\nList of all jobs: ")
        for job in unique_jobs:
            output.write(job + " ")

        print("Cputime total elements " + str(cputime_total.__len__()) + "  walltime total elements  " + str(
            walltime_total.__len__()) + "\n")
        final_cputime = timedelta(hours=0, minutes=0, seconds=0)
        final_walltime = timedelta(hours=0, minutes=0, seconds=0)
        for time in cputime_total:
            token = time.split("=")
            singles = token[1].split(":")
            time_delta = timedelta(hours=int(singles[0]), minutes=int(singles[1]), seconds=int(singles[2]))
            final_cputime = final_cputime + time_delta

        for time in walltime_total:
            token = time.split("=")
            singles = token[1].split(":")
            time_delta = timedelta(hours=int(singles[0]), minutes=int(singles[1]), seconds=int(singles[2]))
            final_walltime = final_walltime + time_delta

        output.write("\nTOTAL CPU TIME = " + str(final_cputime) + ", TOTAL WALLTIME = " + str(
            final_walltime) + ",  TOTAL NUMBER OF JOBS = " + str(total_n_jobs) + "\n")

        output.close()
