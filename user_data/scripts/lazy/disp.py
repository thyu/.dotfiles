from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import time
import threading

from . import constants
from . import termcolor

START_TIMESTAMP = time.time()

def printTag(txt, opts):
    availableLen = opts['width'] - 2
    txtLen = min(len(txt), availableLen)
    margin = (availableLen - txtLen) // 2
    tagTxt = opts['closure'][0] + ' ' * margin + txt[0:txtLen] + ' ' * (availableLen - margin - txtLen) + opts['closure'][1]
    coloredTagTxt = termcolor.colored(tagTxt, opts['color'], 'on_' + opts['background'], opts['attrs'])
    print(coloredTagTxt, end = '')

def printMessage(txt, opts = None):
    leftClosure = ''
    rightClosure = ''
    width = opts['width'] 
    if 'closure' in opts and len(opts['closure']) > 1:
        width = width - 2
        leftClosure = opts['closure'][0]
        rightClosure = opts['closure'][1]
    txtLen = min(len(txt), width)
    if 'align' not in opts:
        opts['align'] = 'center'
    if opts['align'] == 'left':
        leftMargin = 0
        rightMargin = width - txtLen
    elif opts['align'] == 'right':
        leftMargin = width - txtLen
        rightMargin = 0
    else:
        rightMargin = (width - txtLen) // 2
        leftMargin = width - txtLen - leftMargin
    dots = '...' if 'dots' not in opts else opts['dots']
    if len(txt) < width:
        msgTxt = leftClosure + leftMargin * ' ' + txt[0:txtLen] + rightMargin * ' '  + rightClosure
    else:
        msgTxt = leftClosure + txt[0:txtLen - len(dots)] + dots + rightClosure
    coloredMsgTxt = termcolor.colored(msgTxt, opts['color'], 'on_' + opts['background'], opts['attrs'])
    print(coloredMsgTxt, end = '')

def log(tags, txts, lineEnd = '\n'):
    tagOpts = {
        'width' : 10,
        'align' : 'center',
        'color' : 'white',
        'background' : 'blue',
        'attrs' : ['bold'],
        'closure' : '[]'
    }
    tag2Opts = {
        'width' : 10,
        'align' : 'center',
        'color' : 'red',
        'background' : 'yellow',
        'attrs' : ['bold'],
        'closure' : '[]'
    }
    timeOpts = {
        'width' : 15,
        'align' : 'right',
        'color' : 'grey',
        'background' : 'white',
        'attrs' : ['bold'],
        'closure' : '[]'
    }
    msgOpts = {
        'width' : 70,
        'align' : 'left',
        'color' : 'white',
        'background' : 'grey',
        'attrs' : [],
        'dots' : '...'
    }
    if not isinstance(tags, list):
        tags = [tags]
    if not isinstance(txts, list):
        txts = [txts]
    for txt in txts:
        timeTxt = '{:>10.5f}s'.format((time.time() - START_TIMESTAMP))
        printTag(timeTxt, timeOpts)
        for tag in tags:
            printTag(tag, tagOpts)
        printMessage(' ' + txt, msgOpts)
        print('', end = lineEnd)

# NOTE: for async printing, perhaps useful later?
def printProgressTag(txt, opts = None):
    if not opts:
        opts = {
            'width' : 12,
            'closure' : '[]',
            'color' : 'white',
            'background' : 'blue',
            'attrs' : ['bold']
        }
    printTag(txt, opts)

def asyncShowText(done, text):
    count = 0
    while not done.wait(0.1):
        printProgressTag('RUNNING')
        print(text + str(count), end = '\r')
        count = count + 1
    printProgressTag('DONE')
    print(text + str(count), end = '\n')

class AsyncProgressLog(object):
    def __init__(self, action, text):
        self.action = action
        self.text = text
    def show(self):
        done_event = threading.Event()
        t = threading.Thread(target = asyncShowText, args = (done_event, self.text))
        t.start()
        self.action()
        done_event.set()
        t.join()
