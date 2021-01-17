def timeout(guild, session):
    rows = session.execute("SELECT msg_timeout FROM giraffetime.settings WHERE guild=%s", (guild.id,))
    if rows:
        timeout = rows[0].msg_timeout
        if not timeout:
            return None
        else:
            return float(timeout)
    return None

def delete_user_command(guild, session):
    rows = session.execute("SELECT delete_user_cmd FROM giraffetime.settings WHERE guild=%s", (guild.id,))
    if rows:
        return rows[0].delete_user_cmd
    return False

def create_new_role(guild, session):
    rows = session.execute("SELECT create_roles FROM giraffetime.settings WHERE guild=%s", (guild.id,))
    if rows:
        return rows[0].create_roles
    return True
