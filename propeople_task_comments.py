# Copyright: Propeople Ukraine, July 22, 2014
# License: MIT, <https://raw.githubusercontent.com/BR0kEN-/JTC/master/LICENSE>
# Author: Sergey Bondarenko, <broken@firstvector.org>
import datetime, sublime, sublime_plugin, urllib, base64, json, time, pprint

class AskTaskIdCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel('Enter the task ID:', '', self.stdin, None, None)

  def stdin(self, user_input):
    self.window.run_command('make_comment', {'task_id': user_input})

class MakeCommentCommand(sublime_plugin.TextCommand):
  ENCODING = 'utf8'
  SETTING = 'propeople_task_comments'
  TYPE = 'application/json'

  def run(self, edit, **args):
    # The next string is necessary for the next plugin versions.
    # session = sublime.active_window().active_view().settings()

    if not args['task_id']:
      self.message(['You need specify the task ID from JIRA.'])
    else:
      params = self.params()
      auth = '%s:%s' % (params['username'], params['password'])
      auth = bytes(auth, __class__.ENCODING).rstrip()
      auth = base64.encodestring(auth)
      auth = auth.rstrip().decode(__class__.ENCODING)

      request = urllib.request.Request(
        '%s/rest/api/2/search?%s' % (
          params['jira_url'],
          urllib.parse.urlencode({
            'jql': 'key=%s' % args['task_id'],
            'fields': 'assignee,summary,project',
          })
        ),
        headers = {
          'Authorization': 'Basic %s' % auth,
          'Content-Type': __class__.TYPE,
          'Accept': __class__.TYPE,
        },
        method = 'GET'
      )

      try:
        request = urllib.request.urlopen(request)
      except urllib.request.HTTPError as e:
        if e.code == 400:
          self.message([
            'Incorrect task ID: %s does not exists.' % args['task_id'],
          ])
        elif e.code == 401:
          self.message([
            'Incorrect username or password from JIRA account.',
          ])
        else:
          self.message([
            '%s: %s\n\n' % (e.code, e.msg),
            'This may be due to too frequent requests to the',
            'API: wait for some time or login to JIRA again.',
          ])
      else:
        request = json.loads(request.read().decode(__class__.ENCODING))
        request = request['issues'][0]['fields']

        if request['assignee']['name'] != params['username']:
          return self.message([
            'Specified task assigned to %s' % request['assignee']['displayName'],
            'and before start working on it you',
            'should reassign task to yourself.',
          ])

        self.view.run_command('insert_snippet', {
          'contents': self.string([
            '/**',
            '* %s - %s\n *' % (
              request['project']['name'],
              request['summary']
            ),
            '* @copyright %s, %s' % (
              params['company'],
              datetime.datetime.now().strftime("%B %d, %Y")
            ),
            '* @author %s <%s>' % (
              request['assignee']['displayName'],
              request['assignee']['emailAddress']
            ),
            '* @link %s/browse/%s' % (
              params['jira_url'],
              args['task_id']
            ),
            '*/'
          ], '\n ')
        })

  @staticmethod
  def string(strings, separator = ' '):
    return separator.join(strings)

  @staticmethod
  def message(string):
    sublime.message_dialog(__class__.string(string))

  @staticmethod
  def params():
    filename = 'Preferences.sublime-settings'
    settings = sublime.load_settings(filename)
    was_save = settings.get(__class__.SETTING)
    defaults = {
      'company': 'Propeople Ukraine',
      'jira_url': 'http://jira.propeople.com.ua',
      'username': 'JIRA ACCOUNT USERNAME',
      'password': 'JIRA ACCOUNT PASSWORD',
    }

    if was_save:
      return was_save

    settings.set(__class__.SETTING, defaults)
    sublime.save_settings(filename)

    return defaults

