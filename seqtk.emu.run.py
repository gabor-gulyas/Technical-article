import pandas as pd
import os
import subprocess

workdir = "/mnt/d/guly/gemini/"
table = pd.read_csv("{}grouped.files.tsv".format(workdir), sep='\t')

table["greater_than"] = table["greater_than"].astype('int')

values = [20000, 50000, 100000, 250000, 500000, 1000000, 2000000]
command = []

for row in range(1, len(table)):
    find = table.iloc[row, 2]
    path = os.path.dirname(table.iloc[row, 0]).replace("D:/", "/mnt/d/")
    filename = os.path.basename(table.iloc[row, 0]).split('.')[0]
    commands = [value for value in values if value <= find]
    if not os.path.exists(os.path.join(path, str(find))):
        os.mkdir(os.path.join(path, str(find)))
    for command in commands:
        sub = "seqtk sample -s100 {}/{}.fastq {} > {}/{}/{}_{}.fastq".format(path, filename, command, path, find,
                                                                             filename, command)
        print(sub)
        subprocess.run(sub, shell=True)
    if not os.path.exists(os.path.join(path, "full")):
        os.mkdir(os.path.join(path, "full"))
    os.rename(os.path.join(path, os.path.basename(table.iloc[row, 0])), os.path.join(path, "full", os.path.basename(table.iloc[row, 0])))




data = "{}/downsample".format(workdir)
if not os.path.exists(os.path.join(workdir, "emu_output")):
    os.mkdir(os.path.join(workdir, "emu_output"))


emudb = "/mnt/d/guly/database/emu-v3.0.0/emu_database/"
for folder in os.listdir(data):
    if os.path.isdir(os.path.join(data, folder)):
        if not os.path.exists(os.path.join(workdir, "emu_output", folder)):
            os.mkdir(os.path.join(workdir, "emu_output", folder))
            output = os.path.join(workdir, "emu_output", folder)
        for file in os.listdir(os.path.join(data, folder)):
            if file.endswith('.fastq'):
                if "minion" in file:
                    input = os.path.join(data, folder, file)
                    command = "emu abundance --type map-ont {} --keep-counts --threads 48 --db {} --output-dir {}".format(input, emudb, output)
                    subprocess.run(command, shell=True)
                elif "pacbio" in file:
                    input = os.path.join(data, folder, file)
                    command = "emu abundance --type map-pb {} --keep-counts --threads 48 --db {} --output-dir {}".format(input, emudb, output)
                    subprocess.run(command, shell=True)
                elif "illumina" in file:
                    if 'R1' in file:
                        r1_file = os.path.join(data, folder, file)
                        r2_file = os.path.join(data, folder, file.replace('R1', 'R2'))
                        command = "emu abundance --type sr {} {} --keep-counts --threads 48 --db {} --output-dir {}".format(r1_file, r2_file, emudb, output)
                        subprocess.run(command, shell=True)
                    if 'R2' in file:
                        pass





