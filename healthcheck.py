import argparse
import sqlite3
import time
import requests

DEFAULT_INTERVAL = 60
DEFAULT_TIMEOUT = 5

HEADER_TITLE = r"""
  _    _            _ _   _      _____ _               _    
 | |  | |          | | | | |    / ____| |             | |   
 | |__| | ___  __ _| | |_| |__ | |    | |__   ___  ___| | __
 |  __  |/ _ \/ _` | | __| '_ \| |    | '_ \ / _ \/ __| |/ /
 | |  | |  __/ (_| | | |_| | | | |____| | | |  __/ (__|   < 
 |_|  |_|\___|\__,_|_|\__|_| |_|\_____|_| |_|\___|\___|_|\_\

"""

def create_db():
    conn = sqlite3.connect('healthcheck.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS servers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 url TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS checks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 server_id INTEGER NOT NULL,
                 timestamp INTEGER NOT NULL,
                 status INTEGER NOT NULL,
                 FOREIGN KEY (server_id) REFERENCES servers(id))''')
    conn.commit()
    conn.close()

def add_server(name, url):
    conn = sqlite3.connect('healthcheck.db')
    c = conn.cursor()
    c.execute("INSERT INTO servers (name, url) VALUES (?, ?)", (name, url))
    conn.commit()
    conn.close()
    print("Server added {0}:{1}".format(name, url))

def remove_server(name):
    conn = sqlite3.connect('healthcheck.db')
    c = conn.cursor()
    c.execute("DELETE FROM servers WHERE name=?", (name,))
    conn.commit()
    conn.close()
    print("Server Removed {0}:{1}".format(name, url))

def list_servers():
    conn = sqlite3.connect('healthcheck.db')
    c = conn.cursor()
    c.execute("SELECT * FROM servers")
    servers = c.fetchall()
    conn.close()
    if servers:
        print("Servers:")
        for server in servers:
            print("- %s (%s)" % (server[1], server[2]))
    else:
        print("No servers have been added.")

def check_server(url):
    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            print("[+] Health check Passed : {0}".format(url))
            return 1  # server is healthy
    except:
        pass
    print("[x] Health check Failed : {0}".format(url))
    return 0  # server is not healthy

def perform_check(server):
    status = check_server(server[2])
    timestamp = int(time.time())
    conn = sqlite3.connect('healthcheck.db')
    c = conn.cursor()
    c.execute("INSERT INTO checks (server_id, timestamp, status) VALUES (?, ?, ?)", (server[0], timestamp, status))
    conn.commit()
    conn.close()

def check_all_servers():
    conn = sqlite3.connect('healthcheck.db')
    c = conn.cursor()
    c.execute("SELECT * FROM servers")
    servers = c.fetchall()
    conn.close()
    for server in servers:
        perform_check(server)

def main():
    parser = argparse.ArgumentParser(description='Web server health check tool')
    parser.add_argument('--add', metavar=('name', 'url'), nargs=2, help='Add a new server')
    parser.add_argument('--remove', metavar='name', help='Remove a server')
    parser.add_argument('--list', action='store_true', help='List all servers')
    parser.add_argument('--interval', metavar='seconds', type=int, default=DEFAULT_INTERVAL,
                        help='Interval in seconds to check server health (default: %d)' % DEFAULT_INTERVAL)
    parser.add_argument('--timeout', metavar='seconds', type=int, default=DEFAULT_TIMEOUT,
                        help='Timeout in seconds to wait for health response (default: %d)' % DEFAULT_TIMEOUT)
    args = parser.parse_args()

    create_db()

    if args.add:
        add_server(args.add[0], args.add[1])
    elif args.remove:
        remove_server(args.remove)
    elif args.list:
        list_servers()
    else:
        print(HEADER_TITLE)
        while True:
            check_all_servers()
            time.sleep(args.interval)

if __name__ == '__main__':
    main()