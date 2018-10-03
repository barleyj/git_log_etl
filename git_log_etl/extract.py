import os
import re
import shutil

import git
from github import Github

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
    
g = Github(github_token)

org = g.get_organization('puppetlabs')

tickets = {}
for repo in org.get_repos():
    if repo.name in REPOS:
        git_dir = '/tmp/{}'.format(repo.name)
        shutil.rmtree(git_dir)
        git_repo = git.Repo.init(git_dir)
        remote = git_repo.create_remote('puppet', url='{}/{}.git'.format('git@github.com:puppetlabs', repo.name))
        remote.fetch()
#         log = git_repo.git.log('--all', '--numstat', '--date=short', "--pretty=format:'--%h--%ad--%aN'", '--no-renames', '--no-merges', "--since='2017-01-01'",  "--", ".", '":(exclude)spec"')
        log = git_repo.git.log('--all', '--oneline', "--no-renames", "--no-merges", "--since='2017-01-01'",  "--", "./manifests")
#         with open(os.path.join(git_dir, 'git.log'), 'w') as f:
#             f.write(log.encode('utf-8'))
        # 241fd2d (PE-24059) - Remove peadmin class from primary master replica
        match = re.findall('(PE\-[0-9]*)', log)
        if match:
#             ticket = match.group(0).upper()
            tickets[repo.name] = {t.upper() for t in match}
#             with open(os.path.join(git_dir, 'git.log'), 'w') as f:

unique_tickets = {t for r in tickets.values() for t in r}
coupled_tickets = set()
repos = tickets.keys()
for i,r in enumerate(repos):
    for repo in repos[i + 1:]:
        intersection = tickets[r] & tickets[repo]
        if intersection:
            coupled_tickets.update(intersection)
            for t in intersection:
                print('{},{},{}'.format(r,repo,t))


print('Unique tickets: {}'.format(len(unique_tickets)))
print('Coupled tickets: {}'.format(len(coupled_tickets)))
