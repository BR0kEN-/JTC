# JTC

PHP and JS task relations with JIRA issue tracker for Sublime Text 3.

## Installation

- Open the `Sublime Text` editor, go to `Preferences` => `Browse Packages...` and open the `User` directory in opened window.
- Put the `*.py` file into the `User` catalog.
- Go to `Preferences` => `Key Bindings - User` and add the following line to file:
```javascript
{"keys": ["super+t"], "command": "ask_task_id"}
```
- Go to `Preferences` => `Settings - User`, and set the username and password from your account in JIRA in `propeople_task_comments` settings block.

## Usage

Press your keyboard shortcut, enter the task ID from JIRA (e.g. COWI-37) and see the result.

```php
/**
 * COWI - Upload FB share to Live server
 *
 * @copyright Propeople Ukraine, July 22, 2014
 * @author Sergey Bondarenko <broken@propeople.com.ua>
 * @link http://jira.propeople.com.ua/browse/COWI-37
 */
```
