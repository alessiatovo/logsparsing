import sys
import os
import re
from datetime import timedelta

#argv[1] : name filelog - period to start
#argv[2] : name filelog - period to stop

all_files = os.listdir("/var/spool/pbs/server_logs")
files_period = []

#walltime format in format hour:minutes:seconds
walltime_input = sys.argv[3]

#nome file log di inizio
time_start = sys.argv[1]
#nome file log di fine
time_stop =sys.argv[2]

print("walltime input "+str(walltime_input)+", start period "+str(time_start)+", stop period "+str(time_stop))

if not os.path.exists("LOGS_Walltime"):
    os.makedirs("LOGS_Walltime")
output = open("LOGS_Walltime/logs_"+time_start+"_"+time_stop+".txt", "w")


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

for file in files_period:
    print("file: "+str(file)+"\n")

total_jobs = []
pair = []
for file in files_period:
    total_jobs_file = []
    pair_file = []
    with open("/var/spool/pbs/server_logs/" + file, "r") as f:
        output.write("File "+str(file)+"\n")
        print("Opened file "+str(f)+"\n")
        tmp = f.read().split('\n')
        regex = r"(\d{6}).*"+"resources_used.walltime"+"=(\d{2}:\d{2}:\d{2})"
        for t in tmp:
            matches = re.finditer(regex, t)
            for matchNum, match in enumerate(matches):
                matchNum = matchNum + 1
                walltime_entire =match.group(2)
                if walltime_entire >= walltime_input:
                    total_jobs_file.append(match.group(1))
                    total_jobs.append(match.group(1))
                    couple = (match.group(1), match.group(2))
                    pair_file.append(couple)
                    pair.append(couple)
    output.write("Jobs in file "+str(file)+" that have a walltime greater or equal than "+str(walltime_input)+" are "+str(total_jobs_file.__len__())+". List of job is: \n")
    for job in pair_file:
        output.write("Job: "+str(job[0])+", walltime: "+str(job[1])+"\n")
    output.write("\n\n")

output.write("Total number of jobs with walltime greeter or euqal than "+str(walltime_input)+" = "+str(total_jobs.__len__()))
output.write("\nList of jobs:\n")
for job in pair:
    output.write("Job: "+str(job[0])+", walltime: "+str(job[1])+"\n")


