import sys
import paramiko

sys.stdout.reconfigure(encoding="utf-8")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("160.187.147.95", port=22, username="root", password="tiendien9X@@", timeout=15)

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.read().decode("utf-8", errors="replace") + stderr.read().decode("utf-8", errors="replace")

script = """
import sqlite3
import pandas as pd

conn = sqlite3.connect('/home/tibi/NostalgiaForInfinity/user_data/tibi_binance_futures-tradesv3.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Read trades
df = pd.read_sql_query("SELECT * FROM trades", conn)
print("Total trades in DB:", len(df))
print("Columns:", df.columns.tolist())

# Summary of trades
if not df.empty:
    print("\\n--- TRADES SUMMARY ---")
    print("Is short column exists:", 'is_short' in df.columns)
    if 'is_short' in df.columns:
        print("Trades count by position:")
        print(df['is_short'].value_counts(dropna=False))
    
    print("\\nTrades count by is_open:")
    print(df['is_open'].value_counts(dropna=False))
    
    # Analyze closed trades
    closed = df[df['is_open'] == 0].copy()
    print("\\nTotal closed trades:", len(closed))
    if not closed.empty:
        closed['win'] = closed['close_profit'] > 0
        print("Closed trades winrate:", closed['win'].mean() * 100, "%")
        print("Total closed profit (close_profit_abs):", closed['close_profit_abs'].sum() if 'close_profit_abs' in closed.columns else "N/A")
        print("Total closed profit (close_profit):", closed['close_profit'].sum())
        
        # Breakdown by is_short
        if 'is_short' in closed.columns:
            for is_s, g in closed.groupby('is_short'):
                pos_str = "SHORT" if is_s else "LONG"
                wins = (g['close_profit'] > 0).sum()
                losses = (g['close_profit'] <= 0).sum()
                wr = (g['close_profit'] > 0).mean() * 100
                p_abs = g['close_profit_abs'].sum() if 'close_profit_abs' in g.columns else 0
                print(f"\\n[{pos_str}] Trades: {len(g)}, Wins: {wins}, Losses: {losses}, Winrate: {wr:.2f}%, Profit Abs: {p_abs:.2f}")

conn.close()
"""

# Run query inside VPS
stdin, stdout, stderr = ssh.exec_command(f"python3 -c \"{script}\"")
print(stdout.read().decode("utf-8", errors="replace"))
print(stderr.read().decode("utf-8", errors="replace"))

ssh.close()

