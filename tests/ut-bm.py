#!/usr/bin/python
#coding:utf-8

import unittest,configparser


# customized module
import store



class Test_store(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print('UnitTest store')
        global dbfile 
        dbfile = 'E:\\UT\\test.db'
        

    @classmethod
    def tearDownClass(self):
        print('Test complete')

    def test_create(self):
        db = store.db()
        db.create(dbfile)


if __name__ == '__main__':
	unittest.main()
