import os
import re
import configparser
import sys,os,time,getopt
from context import resource_manager
from context.resource_manager import Properties
from parse import config_parser_extender
from tools import  logger
log=logger.getLogger()

class ConfigParser:

    def __init__(self):
        self.configParse=config_parser_extender.CapitalCaseConfigParser()

    def __init__(self,type):
        self.configParse=config_parser_extender.CapitalCaseConfigParser()
        self.type=type
        if type == 'D':
            self.configParse.read(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'directory.ini')
            # self.f = open(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'directory.ini', 'w+')
        elif type == 'F':
            self.configParse.read(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'document.ini')
            # self.f = open(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'document.ini', 'w+')

    def reload(self):
        if type == 'D':
            self.configParse.read(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'directory.ini')
            # self.f = open(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'directory.ini', 'w+')
        elif type == 'F':
            self.configParse.read(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'document.ini')
            # self.f = open(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'document.ini', 'w+')

    def setPath(self,path):
        self.path=path

    def addValue(self,section,key,value):
        try:
            self.configParse.set(section,key,value)
        except:
            self.configParse.add_section(section)
            self.configParse.set(section,key,value)

    @classmethod
    def removeConfigFiles(cls):
        if os.path.isfile(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'directory.ini'):
            os.remove(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'directory.ini')

        if os.path.isfile(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'document.ini'):
            os.remove(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'document.ini')

    def save(self):
        if self.type == 'D':
            f=open(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'directory.ini', 'w+')
            self.configParse.write(f)
            f.close()
            # self.f = open(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'directory.ini', 'w+')
        elif self.type == 'F':
            f=open(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'document.ini', 'w+')
            self.configParse.write(f)
            f.close()
            # self.f = open(Properties.getRootPath()+'conf' + resource_manager.getSeparator() + 'document.ini', 'w+')



    def getValue(self,section,key):

        try:
           return self.configParse.get(section,key)
        except:
            self.configParse.set(section,key,"why")
            log.error("Error there is no section in config file."+str(section)+" - "+str(key))
            self.save()
