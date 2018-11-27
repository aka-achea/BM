#!/usr/bin/python
#coding:utf-8
#Python3


import poplib

M = poplib.POP3_SSL('pop.163.com')
M.set_debuglevel(2)
print(M.getwelcome())
# M.user('akaachea@163.com')
# M.pass_('orz163')

# MS = M.stat()
# print(MS)

# #Get the number of mail messages
# numMessages = len(M.list()[1])

# print("You have %d messages." % numMessages)
# print("Message List:")

# #List the subject line of each message
# for mList in range(numMessages) :
#     for msg in M.retr(mList+1)[1]:
#         if msg.startswith('Subject'):
#             print('\t' + msg)
#             break

# M.quit()