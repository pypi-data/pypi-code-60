
import os
import time
import distutils.spawn

import click
import psutil


class UwsgiController(object):
    def __init__(self, project, base_dir, web_root=None, uwsgi_ini_file=None, logs_root=None, pidfile=None, uwsgi_bin=None):
        self.project = project
        self.base_dir = base_dir
        os.chdir(self.base_dir)
        self.uwsgi_ini_file = uwsgi_ini_file or self.get_default_wsgi_ini_file(project, base_dir)
        self.pidfile = pidfile or self.get_default_pidfile(base_dir)
        self.web_root = web_root or self.get_default_web_root(base_dir)
        self.logs_root = logs_root or self.get_default_logs_root(base_dir)
        self.uwsgi_bin = uwsgi_bin or self.get_default_uwsgi_bin()

    @classmethod
    def get_default_uwsgi_bin(cls):
        for path in [distutils.spawn.find_executable('uwsgi'), "/usr/local/bin/uwsgi", "/usr/bin/uwsgi", "/bin/uwsgi"]:
            if path and os.path.isfile(path) and os.access(path, os.X_OK):
                return path
        return "uwsgi"

    @classmethod
    def get_default_web_root(cls, base_dir):
        return os.path.abspath(os.path.join(base_dir, "./web"))

    @classmethod
    def get_default_logs_root(cls, base_dir):
        return os.path.abspath(os.path.join(base_dir, "./logs"))

    @classmethod
    def get_default_wsgi_ini_file(cls, project, base_dir):
        paths = []
        paths.append(os.path.abspath(os.path.join(os.path.dirname(project.__file__), "wsgi.ini")))
        paths.append(os.path.abspath(os.path.join(base_dir, "./etc/wsgi.ini")))
        paths.append(os.path.abspath("wsgi.ini"))
        for path in paths:
            if os.path.isfile(path):
                return path
        print("Can not find wsgi.ini file in paths: {0}".format(",".join(paths)))
        os.sys.exit(1)

    @classmethod
    def get_default_pidfile(cls, base_dir):
        return os.path.abspath(os.path.join(base_dir, "./uwsgi.pid"))

    def get_server_pid(self):
        if not os.path.isfile(self.pidfile):
            return 0
        with open(self.pidfile, "r", encoding="utf-8") as fobj:
            return int(fobj.read().strip())

    def is_server_running(self):
        if not os.path.exists(self.pidfile):
            return False
        with open(self.pidfile, "r", encoding="utf-8") as fobj:
            pid = int(fobj.read().strip())
        return psutil.pid_exists(pid)

    def start(self):
        print("Start uwsgi server...")
        cmd = "{0} {1}".format(self.uwsgi_bin, self.uwsgi_ini_file)
        print(cmd)
        os.system(cmd)
        print("Uwsgi server started!")

    def stop(self):
        print("Stop uwsgi server...")
        cmd = "{0} --stop {1}".format(self.uwsgi_bin, self.pidfile)
        print(cmd)
        os.system(cmd)
        print("Uwsgi server stopped!")

    def reload(self):
        print("Reload uwsgi server...")
        cmd = "{0} --reload {1}".format(self.uwsgi_bin, self.pidfile)
        print(cmd)
        os.system(cmd)
        print("Uwsgi server reloaded!")

    def get_controller(self):
        @click.group()
        def controller():
            pass

        @controller.command()
        def start():
            """Start uwsgi server.
            """
            os.chdir(self.web_root)
            if self.is_server_running():
                pid = self.get_server_pid()
                print("Uwsgi service is running: {0}....".format(pid))
                os.sys.exit(1)
            else:
                self.start()

        @controller.command()
        def stop():
            """Stop uwsgi server.
            """
            if not self.is_server_running():
                print("Uwsgi service is NOT running!")
                os.sys.exit(1)
            else:
                self.stop()

        @controller.command()
        @click.option("-w", "--wait-seconds", type=int, default=2, help="Sleep some seconds after server stopped!")
        def restart(wait_seconds):
            """Restart uwsgi server.
            """
            print("Restart uwsgi server...")
            wait_seconds_flag = False
            if self.is_server_running():
                self.stop()
                wait_seconds_flag = True
            else:
                print("Uwsgi service is NOT running!")
            if wait_seconds_flag:
                print("Sleep {} seconds...".format(wait_seconds))
                time.sleep(wait_seconds)
            self.start()
            print("Uwsgi server started!")

        @controller.command()
        def reload():
            """Reload uwsgi server.
            """
            if not self.is_server_running():
                print("Uwsgi service is NOT running, just start it...")
                self.start()
            else:
                self.reload()

        @controller.command()
        def status():
            """Get uwsgi server status.
            """
            if self.is_server_running():
                pid = self.get_server_pid()
                print("Uwsgi server is running: {0}.".format(pid))
            else:
                print("Uwsgi server is NOT running.")
    
        return controller

