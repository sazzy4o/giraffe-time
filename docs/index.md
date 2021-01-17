# Giraffe Time Docs

## Commands

| Command               | Usage                             | Description                                                                                                  | Aliases                     | Requires Admin |
| --------------------- |:-------------:                    |:----------------------:                                                                                      | :-----:                     | -----:|
| `/help`               | `/help`                           | List commands and usage                                                                                      | [`/add`, `/add_role`]       | ✔️ |
| `/role_add`           | `/role_add <role>`                | If the role exists, add it to the list of self-assignable roles. Otherwise create a self-assignable role.    | [`/add`, `/add_role`]       | ✔️ |
| `/role_remove`        | `/role_remove <role>`             | Remove a role from the list of self-assignables. Does not delete the role.                                   | [`/remove`, `/remove_role`] | ✔️ |
| `/start_new_season`   | `/start_new_season`               | Remove roles from all                                                                                        | [`/start_new_semester`]     | ✔️ |
| `/role_join`          | `/role_join <role>`               | Join a self-assignable role                                                                                  | [`/join`]                   | ❌ |
| `/role_leave`         | `/role_leave <role>`              | Leave a self-assignable role                                                                                 | [`/leave`]                  | ❌ |
| `/list_roles`         | `/list_roles`                     | List all self-assignables roles                                                                              | [`/list`, `/roles`]         | ❌ |
| `/remind`             | `/remind <role> <time> <message>` | Set a reminder                                                                                               | [`/create_reminder`]        | ✔️ |
| `/delete_reminder`    | `/delete_reminder <reminder_id>`  | Delete a reminder                                                                                            | [`/delete_reminder`]        | ✔️ |
| `/list_reminders`     | `/list_reminders`                 | List all reminders                                                                                           |                             | ✔️ |
| `/clear`              | `/clear`                          | Clear chat                                                                                                   | [`/prune`, `/purge`]        | ✔️ |
| `/set_timeout`        | `/set_timeout <timeout>`          | Change timeout setting                                                                                       |                             | ✔️ |
| `/remove_caller`      | `/remove_caller <boolean>`        | Change remove caller setting                                                                                 |                             | ✔️ |
| `/create_missing_role`| `/create_missing_role <boolean>`  | Change create missing role setting                                                                           |                             | ✔️ |
