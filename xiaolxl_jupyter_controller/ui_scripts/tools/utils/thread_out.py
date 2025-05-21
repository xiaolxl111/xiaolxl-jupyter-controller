import signal
import subprocess as sp
import threading
import sys


class VerboseCalledProcessError(sp.CalledProcessError):
    def __str__(self):
        if self.returncode and self.returncode < 0:
            try:
                msg = "Command '%s' died with %r." % (
                    self.cmd, signal.Signals(-self.returncode))
            except ValueError:
                msg = "Command '%s' died with unknown signal %d." % (
                    self.cmd, -self.returncode)
        else:
            msg = "Command '%s' returned non-zero exit status %d." % (
                self.cmd, self.returncode)

        return f'{msg}\n' \
               f'Stdout:\n' \
               f'{self.output}\n' \
               f'Stderr:\n' \
               f'{self.stderr}'


def bash(cmd, out_,print_stdout=True, print_stderr=True):
    proc = sp.Popen(cmd, stderr=sp.PIPE, stdout=sp.PIPE, shell=True, universal_newlines=True,
                    executable='/bin/bash')

    all_stdout = []
    all_stderr = []
    while proc.poll() is None:
        for stdout_line in proc.stdout:
            if stdout_line != '':
                if print_stdout:
                    # print(stdout_line, end='')
                    out_.append_stdout(stdout_line)
                all_stdout.append(stdout_line)
        for stderr_line in proc.stderr:
            if stderr_line != '':
                if print_stderr:
                    # print(stderr_line, end='', file=sys.stderr)
                    out_.append_stdout(stderr_line,file=sys.stderr)
                all_stderr.append(stderr_line)

    stdout_text = ''.join(all_stdout)
    stderr_text = ''.join(all_stderr)
    if proc.wait() != 0:
        raise VerboseCalledProcessError(proc.returncode, cmd, stdout_text, stderr_text)

def thread_func(com,out):
    bash(com,out)
    
def run_thread_out(com,out):
    thread = threading.Thread(
        target=thread_func,
        args=(com,out,))
    thread.start()

