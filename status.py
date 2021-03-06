from buildbot.status import html
from buildbot.status import words
from buildbot.status.web.auth import BasicAuth
from buildbot.status.web.authz import Authz

status = []

users = [
    ('dev', 'bbot!')    # it's not *that* secret..
]

authz = Authz(
    auth=BasicAuth(users),
    forceBuild='auth',
    forceAllBuilds='auth',
    gracefulShutdown='auth'
)

status.append(html.WebStatus(
    # localhost is not available in the jail
    http_port="tcp:8010:interface=192.168.80.239",
    authz=authz,
    order_console_by_time=True,
    revlink="http://github.com/buildbot/buildbot/commit/%s",
    changecommentlink=(r'\b#(\d+)\b', r'http://buildbot.net/trac/ticket/\1', r'Ticket \g<0>'),
    change_hook_dialects={
        'github': {}
    }))

status.append(words.IRC(
    host="irc.freenode.net",
    nick="bb-meta",
    notify_events={
        'successToFailure': 1,
        'failureToSuccess': 1
    },
    channels=["#buildbot"]))
