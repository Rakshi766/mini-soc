file = open("../sample_logs/auth.log", "r")

for line in file:
    print(line.strip())

file.close()