#!/usr/bin/env python
"""
Utility functions for python in unix shell.
"""

import os,sys,logging

class CommandPathCache(list):
    """
    Class to represent commands on user's search path.
    """
    def __init__(self):
        self.paths = None
        self.update()

    def update(self):
        """
        Updates the commands available on user's PATH
        """
        self.paths = []
        self.__delslice__(0,len(self))
        for path in os.getenv('PATH').split(os.pathsep):
            if self.paths.count(path) == 0:
                self.paths.append(path)
        for path in self.paths:
            for cmd in [os.path.join(path,f) for f in os.listdir(path)]:
                if os.path.isdir(cmd) or not os.access(cmd,os.X_OK):
                    continue
                self.append(cmd)

    def versions(self,name):
        """
        Returns all commands with given name on path, ordered by PATH search
        order.
        """ 
        if len(self) == 0:
            self.update()
        return filter(lambda x: os.path.basename(x) == name, self)

    def which(self,name):
        """
        Return first matching path to command given with name, or None if 
        command is not on path
        """
        if len(self) == 0:
            self.update()
        try:
            return filter(lambda x: os.path.basename(x) == name, self)[0]
        except IndexError:
            return None

TERM_TITLE_SUPPORTED = [ 'xterm','xterm-debian']

def xterm_title(value,max_lenght=74):
    """
    Set title in xterm titlebar to given value. 
    Protect ancient xterms from crashes by cutting length of message 
    to 74 characters.
    """ 
    TERM=os.getenv('TERM')
    if TERM not in TERM_TITLE_SUPPORTED:
        return
    sys.stdout.write('\033]2;'+value[:max_length]+'',)
    sys.stdout.flush()
