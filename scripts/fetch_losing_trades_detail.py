import sys
import paramiko

sys.stdout.reconfigure(encoding="utf-8")

vps_script = """import sqlite3
import json

conn = sqlite3.connect('/home/tibi/NostalgiaForInfinity/user_data/tibi_binance_futures-tradesv3.sqlite')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all closed losing trades and current open trades
cursor.execute("SELECT * FROM trades WHERE (is_open = 0 AND close_profit <= 0) OR is_open = 1 ORDER BY open_date")
trades = cursor.fetchall()

print(f"Total trades to deep-dive: {len(trades)}")

results = []
for t in trades:
    tid = t['id']
    cursor.execute("SELECT * FROM orders WHERE ft_trade_id = ? ORDER BY order_date", (tid,))
    orders = [dict(o) for o in cursor.fetchall()]
    
    t_dict = dict(t)
    t_dict['orders'] = orders
    results.append(t_dict)

conn.close()

with open('/tmp/deep_dive_data.json', 'w') as f:
    json.dump(results, f, default=str, indent=2)

print("Saved /tmp/deep_dive_data.json successfully with", len(results), "trades.")
"""

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("160.187.147.95", port=22, username="root", password="tiendien9X@@", timeout=15)

sftp = ssh.open_sftp()
with sftp.file("/tmp/dump_losing_trades.py", "w") as f:
    f.write(vps_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("python3 /tmp/dump_losing_trades.py")
print(stdout.read().decode("utf-8", errors="replace"))
print(stderr.read().decode("utf-8", errors="replace"))

# Now let's download /tmp/deep_dive_data.json to local machine
sftp = ssh.open_sftp()
sftp.get("/tmp/deep_dive_data.json", "user_data/deep_dive_losing_trades.json")
sftp.close()
ssh.close()
print("Downloaded to local user_data/deep_dive_losing_trades.json")

