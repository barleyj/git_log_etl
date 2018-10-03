import datetime
from itertools import izip_longest
import os

from pyparsing import *

def parse_date(t):
    date_parts = [int(p) for p in t[0]]
    return datetime.datetime(*date_parts)

sha = Word(alphanums)
sha.setParseAction(lambda t: t[0])
date = Group(Word(nums) + Suppress('-') + Word(nums) + Suppress('-') + Word(nums))
date.setParseAction(parse_date)
name = Word(alphanums + ' ')
name.setParseAction(lambda t: t[0])
header_def = OneOrMore(Suppress('--') + sha('sha') + Suppress('--') + date('date') + Suppress('--') + name('commiter'))

additions = Word(nums)
additions.setParseAction(lambda t: int(t[0]))
subtractions = Word(nums)
subtractions.setParseAction(lambda t: int(t[0]))
file_name = SkipTo(lineEnd)
file_changes = OneOrMore(additions('additions') + subtractions('sutractions') + file_name('file_name'))

commit = header_def('header') + file_changes('changes')


def grouper(iterable):
    "grouper('ABCDEF') --> ABC DEF"
    args = [iter(iterable)] * 3
    return izip_longest(*args)


REPOS = {
    'puppetlabs-puppet_enterprise',
    'puppetlabs-pe_accounts',
    'puppetlabs-pe_hocon',
    'puppetlabs-pe_inifile',
    'puppetlabs-pe_nginx',
    'puppetlabs-pe_staging',
    'puppetlabs-pe_java_ks',
    'puppetlabs-pe_postgresql',
    'puppetlabs-pe_puppet_authorization',
    'puppetlabs-pe_puppetdbquery',
    'puppetlabs-pe_manager',
    'puppetlabs-pe_infrastructure',
    'puppetlabs-pe_razor',
    'puppetlabs-pe_concat',
    'puppetlabs-pe_repo',
    'puppetlabs-pe_install',
    }

    
for r in REPOS:
    file_path = os.path.join('/tmp', r, 'git.log')
    for param in commit.searchString(file('output.test').read()):
        for commit_sha,commit_date,committer in grouper(param['header']):
            print('--{}--{}--{}'.format(commit_sha,commit_date.date(),committer))
        for add,sub,f in grouper(param['changes']):
            file_path = os.path.join(r, f)
            print('{:<}\t{:<}\t{}'.format(add,sub,file_path))
            #    print param.dump()
        print ''

