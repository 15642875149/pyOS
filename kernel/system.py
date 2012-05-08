from kernel import filesystem
from kernel import shell

class System(object):
    """
    Handles all of the low level stuff.
    PIDs, startup, shutdown, events

    System States:
    -2: reboot
    -1: shutting down
    0:  idle
    1:  running shell


    """
    _state = {}
    def __init__(self):
        self.__dict__ = self._state
        self.display = None#Display()
        self.output = None
        self.pids = []
        self.state = 0

    def run(self):
        self.startup()
        self.state = 0
        while self.state >= 0:
            current = self.new_shell()
            current.run()
        if self.state <= -1:
            self.shutdown()
            if self.state == -2:
                self.run()

    def startup(self):
        try:
            program = filesystem.open_program('kernel/startup')
            program.run()
        except:
            raise IOError

    def shutdown(self):
        try:
            program = filesystem.open_program('kernel/shutdown')
            program.run()
        except:
            raise IOError

    def new_shell(self, parent=None, program="interpreter", args="",
                 stdin='', path="/"):
        y = shell.Shell(len(self.pids), parent, program, args, stdin, path)
        self.new_pid(y)
        self.state = 1
        return y

    def get_pid(self, item):
        try:
            x = self.pids.index(item)
        except:
            x = None
        return x

    def get_process(self, pid):
        try:
            x = self.pids[pid]
        except:
            x = None
        return x

    def new_pid(self, item):
        x =  len(self.pids)
        self.pids.append(item)
        return x

    def get_events(self, _type=None):
        if _type is None:
            return "all"
        else:
            return "some"

System = System()