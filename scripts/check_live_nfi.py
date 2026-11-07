import sys
import paramiko

sys.stdout.reconfigure(encoding="utf-8")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("160.187.147.95", port=22, username="root", password="tiendien9X@@", timeout=15)

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    return out + err

print("=== LS /home/tibi/NostalgiaForInfinity ===")
print(run("ls -la /home/tibi/NostalgiaForInfinity"))

print("=== GIT STATUS IN /home/tibi/NostalgiaForInfinity ===")
print(run("su - tibi -c 'cd /home/tibi/NostalgiaForInfinity && git status && git log -3 --oneline'"))

print("=== USER_DATA CONTENTS ===")
print(run("ls -la /home/tibi/NostalgiaForInfinity/user_data/"))

print("=== SQLITE DATABASES ===")
print(run("find /home/tibi/NostalgiaForInfinity -name '*.sqlite*' -ls"))

ssh.close()

