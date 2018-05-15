import sys
import os
import re
from datetime import timedelta

#argv[1] : name filelog - period to start
#argv[2] : name filelog - period to stop

all_files = os.listdir("/var/spool/pbs/server_logs")
files_period = []

#nome file log di inizio
time_start = sys.argv[1]
#nome file log di fine
time_stop =sys.argv[2]

if not os.path.exists("LOGS_StatusPeriod"):
    os.makedirs("LOGS_StatusPeriod")
output = open("LOGS_StatusPeriod/logs_"+time_start+"_"+time_stop+".txt", "w")


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




#search all users
for file in files_period:
    users = []
    with open("/var/spool/pbs/server_logs/" + file, "r") as f:
        tmp = f.read().split('\n')
        regex = r".*owner = (.*)@"
        for t in tmp:
            matches = re.finditer(regex, t)
            print("read line\n")
            for matchNum, match in enumerate(matches):
                matchNum = matchNum + 1
                users.append((match.group(1)))

unique_users = sorted(list(set(users)))


for user in unique_users:

    total_n_jobs = 0
    jobs = []
    jobs_and_queue = []
    jobs_ok = []
    jobs_error = []
    jobs_killed = []
    jobs_not_status= []
    unique_jobs = []
    name_and_surname = user.split(".")
    name = name_and_surname[0]
    surname = name_and_surname[1]
    output.write("User "+name+" "+surname+"\n")
    for file in files_period:
        year=file[0]+file[1]+file[2]+file[3]
        month=file[4]+file[5]
        day=file[6]+file[7]
        lines = []
        jobs_of_file = []
        jobs_ok_file = []
        jobs_error_file = []
        jobs_killed_file = []
        jobs_notstatus_file = []
        job_file = []
        with open("/var/spool/pbs/server_logs/"+file, "r") as f:
            tmp = f.read().split('\n')
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
            # write on file the list of jobs for each file log
            output.write("Number of jobs: " + str(unique_jobs_file.__len__()) + ", list of jobs: ")
            for job in unique_jobs_file:
                output.write(str(job) + " ")
            output.write("\n")
            flag = 0
            for job in unique_jobs_file:
                with open("/var/spool/pbs/server_logs/" + file, "r") as f:
                    tmp = f.read().split("\n")
                    for t in tmp:
                        if job in t:
                            print("read each line\n")
                            lines.append(t)
                            tokens_line = t.split(" ")
                            if tokens_line.__len__() == 8:
                                tk = tokens_line[1].split(";")
                                if tk[5].split("=")[0] == "Exit_status":
                                    flag = 1
                                    status_line = tokens_line[1]
                                    status_tokens = status_line.split(";")
                                    status = status_tokens[5]
                                    status_token_val = status.split("=")
                                    value = "-1"
                                    if (status_token_val[0] == "Exit_status"):
                                        value = status_token_val[1]

                                    resp = "value not defined"
                                    if value == "0":
                                        resp = "job completed with success"
                                        jobs_ok_file.append(job)
                                        jobs_ok.append(job)
                                    elif value == "1":
                                        resp = "job contains an error code"
                                        jobs_error.append(job)
                                        jobs_error_file.append(job)
                                    elif value == "271":
                                        resp = "job has been killed manually"
                                        jobs_killed.append(job)
                                        jobs_killed_file.append(job)
                                    else:
                                        jobs_not_status.append(job)
                                        jobs_notstatus_file.append(job)
                                    right_queue = ""
                                    for jobQ, queueQ in jobs_and_queue:
                                        if jobQ == job:
                                            right_queue = queueQ
            total_n_jobs = total_n_jobs + unique_jobs_file.__len__()
            if flag == 0:
                output.write("There are no job that finished in current file\n")
            else:
                output.write("Number of jobs with Exit status = Ok (0) in current file : "+str(jobs_ok_file.__len__())+". Jobs are: ")
                for job in jobs_ok_file:
                    output.write(job+" ")
                output.write("\nNumber of jobs with Exit status = Error (1) in current file : "+str(jobs_error_file.__len__())+". Jobs are: ")
                for job in jobs_error_file:
                    output.write(job+" ")
                output.write("\nNumber of jobs with Exit status = Killed Manually (271) in current file : " + str(jobs_killed_file.__len__()) + ". Jobs are: ")
                for job in jobs_killed_file:
                    output.write(job + " ")
                output.write("\nNumber of jobs with Exit status not identified in current file : " + str(jobs_notstatus_file.__len__()) + ". Jobs are: ")
                for job in jobs_notstatus_file:
                    output.write(job + " ")
                output.write("\n\n")
        else:
            output.write("There are no jobs in current file\n")

    output.write("\nNumber of jobs for current period for user "+name+" "+surname+": "+str(unique_jobs.__len__()))
    output.write("\nNumber of all jobs for current period with Exit status = Ok (0): "+str(jobs_ok.__len__())+". The jobs are: ")
    for job in jobs_ok:
        output.write(job + " ")
    output.write("\nNumber of all jobs for current period with Exit status = Error (1): "+str(jobs_error.__len__())+". The jobs are: ")
    for job in jobs_error:
        output.write(job + " ")
    output.write("\nNumber of all jobs for current period with Exit status = Killed Manually (271): "+str(jobs_killed.__len__())+". The jobs are: ")
    for job in jobs_killed:
        output.write(job + " ")
    output.write("\nNumber of all jobs for current period with Exit status not identified: "+str(jobs_not_status.__len__())+". The jobs are: ")
    for job in jobs_not_status:
        output.write(job + " ")
    output.write("\n------------------------------------------------------------------------------------------------------------------------------------\n")


output.close()
