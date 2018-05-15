import sys
import os
import re
from datetime import datetime
from datetime import timedelta
from collections import OrderedDict


#argv[1] : user name in name.surname
#argv[2] : name filelog - period to start
#argv[3] : name filelog - period to stop

all_files = os.listdir("/home/alessia/UNI/150ore/ScriptFinale/logs")
files_period = []




#nome utente formato nome.cognome
name_ = sys.argv[1]
token=name_.split(".")
name=token[0]
surname=token[1]
#nome file log di inizio
time_start = sys.argv[2]
#nome file log di fine
time_stop =sys.argv[3]

#creation of folder to save the report
if not os.path.exists("LOGS_UserPeriod"):
    os.makedirs("LOGS_UserPeriod")
output = open("LOGS_UserPeriod/logs_"+time_start+"_"+time_stop+".txt", "w")

#extraction of element of period start
year_start=time_start[0]+time_start[1]+time_start[2]+time_start[3]
month_start=time_start[4]+time_start[5]
day_start=time_start[6]+time_start[7]

#extraction of element of period end
year_stop=time_stop[0]+time_stop[1]+time_stop[2]+time_stop[3]
month_stop=time_stop[4]+time_stop[5]
day_stop=time_stop[6]+time_stop[7]


output.write("REPORT from "+day_start+"/"+month_start+"/"+year_start+" to "+day_stop+"/"+month_stop+"/"+year_stop+"\n\n")

#obtain all the files into the directory in the indicated period
for file in all_files:
    if(file >= time_start) and (file<=time_stop):
        files_period.append(file)

cputime_total = []
walltime_total = []
total_n_jobs = 0

jobs = []
jobs_and_queue = []
#looking into each file log
for file in files_period:
    output.write("\nLOG FILE: " + str(file)+"\n")
    year=file[0]+file[1]+file[2]+file[3]
    day=file[4]+file[5]
    month=file[6]+file[7]
    lines = []
    cputime_file = []
    walltime_file = []
    job_file = []

    with open("logs/"+file, "r") as f:
        tmp = f.read().split('\n')
        #regex to search all the jobs of the user
        regex = r"(.*(\d{6}).*("+name+"\."+surname+").*)"
        for t in tmp:
            matches = re.finditer(regex, t)
            print("read line\n")
            for matchNum, match in enumerate(matches):
                matchNum = matchNum + 1
                print("write in file\n")
                jobs.append(match.group(2))
                job_file.append(match.group(2))
                tmp_queue = t.split()
                if tmp_queue.__len__() >= 16:
                    queue = tmp_queue[16]
                    pair = (match.group(2),queue)
                    jobs_and_queue.append(pair)


    unique_jobs = list(set(jobs))
    unique_jobs.sort()
    unique_jobs_file = list(set(job_file))
    unique_jobs_file.sort()



    if unique_jobs_file.__len__() != 0:
        #write on file the list of jobs for each file log
        output.write("Number of jobs: " + str(unique_jobs_file.__len__()) + ", list of jobs: ")
        for job in unique_jobs_file:
            output.write(str(job)+" ")
        output.write("\n")
        flag=0
        for job in unique_jobs_file:
            cputime=""
            walltime=""
            with open("logs/"+file, "r") as f:
                tmp = f.read().split("\n")
                for t in tmp:
                    if job in t:
                        print("read each line\n")
                        lines.append(t)
                        tokens_line = t.split(" ")
                        if tokens_line.__len__() == 8:
                            tk = tokens_line[1].split(";")
                            if tk[5].split("=")[0] == "Exit_status":
                                flag=1
                                cputime_total.append(tokens_line[3])
                                cputime=tokens_line[3]
                                cputime_file.append(cputime)
                                walltime=tokens_line[7]
                                walltime_total.append(walltime)
                                walltime_file.append(walltime)
                                status_line = tokens_line[1]
                                status_tokens = status_line.split(";")
                                status = status_tokens[5]
                                status_token_val = status.split("=")
                                value = "-1"
                                if (status_token_val[0] == "Exit_status"):
                                    value = status_token_val[1]

                                resp="value not defined"
                                if value == "0":
                                    resp = "job completed with success"
                                elif value == "1":
                                    resp = "job contains an error code"
                                elif value == "271":
                                    resp = "job has been killed manually"
                                right_queue = ""
                                for jobQ, queueQ in jobs_and_queue:
                                    if jobQ == job:
                                        right_queue = queueQ
                                output.write("JOB: "+job+", date: "+day+"/"+month+"/"+year+", queue: "+right_queue+", "+str(cputime)+", "+str(walltime)+", status job "+status+". It means: "+resp+"\n")
        total_n_jobs = total_n_jobs+unique_jobs_file.__len__()
        if flag==0:
            output.write("There are no job that finished in current file\n")
        else:
            total_cputime_file = timedelta(hours=0, minutes=0, seconds=0)
            for time in cputime_file:
                token = time.split("=")
                singles = token[1].split(":")
                time_delta = timedelta(hours=int(singles[0]), minutes=int(singles[1]), seconds=int(singles[2]))
                total_cputime_file = total_cputime_file + time_delta

            total_walltime_file = timedelta(hours=0, minutes=0, seconds=0)
            for time in walltime_file:
                token = time.split("=")
                singles = token[1].split(":")
                time_delta = timedelta(hours=int(singles[0]), minutes=int(singles[1]), seconds=int(singles[2]))
                total_walltime_file = total_walltime_file + time_delta

            output.write("\nTotal cputime of file " + day + "/" + month + "/" + year + ": " + str(total_cputime_file) + ". Total walltime of file is: " + str(total_walltime_file) + "\n\n\n")

    else:
        output.write("There are no jobs in current file\n")

output.write("\n\nList of all jobs: ")
for job in unique_jobs:
    output.write(job+" ")


print("Cputime total elements "+str(cputime_total.__len__())+"  walltime total elements  "+str(walltime_total.__len__())+"\n")
final_cputime = timedelta(hours=0, minutes=0, seconds=0)
final_walltime = timedelta(hours=0, minutes=0, seconds=0)
for time in cputime_total:
    token = time.split("=")
    singles = token[1].split(":")
    time_delta= timedelta(hours=int(singles[0]), minutes=int(singles[1]), seconds=int(singles[2]))
    final_cputime=final_cputime+time_delta

for time in walltime_total:
    token = time.split("=")
    singles = token[1].split(":")
    time_delta = timedelta(hours=int(singles[0]), minutes=int(singles[1]), seconds=int(singles[2]))
    final_walltime = final_walltime + time_delta

output.write("\nTOTAL CPU TIME = "+str(final_cputime)+", TOTAL WALLTIME = "+str(final_walltime)+",  TOTAL NUMBER OF JOBS = "+str(unique_jobs.__len__())+"\n")

output.close()
