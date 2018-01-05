import psycopg2
import csv
import sys
import time
import errno
import io
import os
import subprocess
import pexpect


def error(*args, **kwargs):
    args = list(args)
    args[0] = "!!!!!! [error] " + args[0]
    print(*args, **kwargs)
    raise Exception(args[0])

def env_bool_override(default, name):
    if name not in os.environ:
        return default
    envvar = os.environ[name]
    print("envvar override for {}: {}".format(name, envvar))
    if envvar.lower() == "false":
        return False
    elif envvar.lower() == "true":
        return True
    else:
        error("{} set to invalid value: {}".format(name, envvar))

PRODUCTION = env_bool_override(True, "PRODUCTION")

def trace(*args, **kwargs):
    args = list(args)
    args[0] = "[trace] " + args[0]
    print(*args, **kwargs)

def debug(*args, **kwargs):
    args = list(args)
    args[0] = "[debug] " + args[0]
    print(*args, **kwargs)

# may output sensitive information; disable in production
def sensitive_debug(*args, **kwargs):
    if PRODUCTION: return
    args = list(args)
    args[0] = "[SENSITIVE debug] " + args[0]
    print(*args, **kwargs)

def sensitive_stdout():
    if PRODUCTION: 
        return None
    else: 
        return sys.stdout.buffer

def info(*args, **kwargs):
    args = list(args)
    args[0] = "[info] " + args[0]
    print(*args, **kwargs)

def warn(*args, **kwargs):
    args = list(args)
    args[0] = "** [warn] " + args[0]
    print(*args, **kwargs)

def warn2(*args, **kwargs):
    args = list(args)
    args[0] = "**** [warn2] " + args[0]
    print(*args, **kwargs)

def assert_error(condition, error_msg):
    if not condition:
        error(error_msg)

def remote():
    assert "HEROKU_REMOTE" in os.environ
    return os.environ["HEROKU_REMOTE"]

def shell_expect(cmd):
    sensitive_debug("Running expect shell command: {}".format(cmd))
    child = pexpect.spawn('bash', ['-c', cmd])
    child.logfile = sensitive_stdout()
    return child

def shell_blocking(cmd, input=None):
    sensitive_debug("Running blocking shell command: {}".format(cmd))
    if input is not None:
        input = input.encode("utf8")
    ret = subprocess.check_output(cmd, shell=True, input=input).decode("utf8")
    sensitive_debug(ret)
    return ret

def sleep(t):
    og_t = t
    interval = 10
    while t > 0:
        debug("Sleep {}/{} sec...".format(t, og_t))
        time.sleep(min([interval, t]))
        t -= interval

def rm_file_if_exists(fname):
    try: 
        os.remove(fname)
    except OSError:
        pass

def ensure_dir(dirname):
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


class Database:

    def __init__(self):
        self.url = os.environ["DATABASE_URL"]
        debug("Opening database connection to url {}".format(self.url))
        self.connection = psycopg2.connect(self.url)
        self.cursor = self.connection.cursor()

    def __del__(self):
        debug("Closing database connection to url {}".format(self.url))
        self.rollback()
        self.connection.close()

    def mogrify(self, query, values):
        return self.cursor.mogrify(query, values).decode("utf8")
    
    def execute(self, query, values=None):
        debug(self.mogrify(query, values))
        return self.cursor.execute(query, values)
    
    def query(self, query, values=None):
        debug(self.mogrify(query, values))
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def commit(self):
        debug("Committing database connection with url {}".format(self.url))
        self.connection.commit()

    def rollback(self):
        debug("Rolling back database connection with url {}".format(self.url))
        self.connection.rollback()


