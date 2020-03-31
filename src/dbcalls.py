base = None

def init_dbwrapper(db):
    """ Initialize this wrapper

    :param db: Instance of database connection

    """

    global base
    base = db

# Pull user names and IDS, return both in form (name, id)
def db_get_ids():
    """Get all users and IDs in DB

    :return: List of (name, ID) tuples

    """

    result = []

    all_users = base.list_users()

    for emp in all_users:
        result.append((emp[1], emp[0]))

    return result

# Search project and user by ID, return full row (as object?)
## FIXME: Get project by ID or user by iD? (this should be 2 different functions if so)
# TODO: Seperate functions then, need one for each

def get_user(eid):
    user = base.db_query('''SELECT * FROM employee WHERE eid=%d;''' % eid)
    if user is None:
        return user
    return user[0]

def get_project(name):
    proj = base.db_query('''SELECT * FROM project WHERE project_name="%s"''' % name)
    if proj is None:
        return proj
    return proj[0]

# Return current rank list
def get_ranks():
    """Fetch ranks from database

    :return: List of ranks

    """
    return []

# Push current rank list
def update_ranks(ranks):
    """Update ranks in database

    :param ranks: List of ranks

    """

    pass

def associate_billing_code(pid, code):
    base.add_billing_code(code)
    base.add_billing_code_for_project(pid, code)

def check_user_exists(eid):
    exists = base.db_query("SELECT count(*) FROM employee WHERE eid = %d;" % int(eid))
    return exists[0][0] > 0

def check_project_exists(name):
    exists = base.db_query('''SELECT count(*) FROM project WHERE project_name = "%s";''' % str(name))
    return exists[0][0] > 0

def check_uproj_exists(eid, code):
    exists = base.db_query('''SELECT count(*) FROM user_project WHERE eid = %d AND billing_code = %d;''' % (eid, code))
    return exists[0][0] > 0

# Send object (User, Project, UserProject) to db
def update_user(eid, name, role, rate, mentor, rank):
    """Update a user in database

    :param user: Updated uer

    """

    exists = check_user_exists(eid)
    if not exists:
        if mentor is None:
            mentor = "NULL"
        base.create_user(eid, name, rank=rank, rate=rate, role=role, mentor=mentor)
    else:
        pass
        # TODO: Update

def update_project(name, description, exp_hours, last_update, rpt=False, start_mo="NULL", start_yr="NULL", end_mo="NULL",
                    end_yr="NULL"):
    """Update a project in database

    :param proj: Updated project

    """

    exists = check_project_exists(name)
    if not exists:
        base.create_project(name, description, exp_hours, start_yr, start_mo, end_yr, end_mo, rpt)
    else:
        # TODO: update
        pass

def get_pid(name):
    pid = base.db_query('''SELECT pid FROM project WHERE project_name="%s"''' % name)
    return pid[0][0]

def update_userproj(code, owner, proj_hrs, des_hrs, act_hrs):
    """Update a user project in database

    :param uproj: Updated user project

    """

    exists = check_uproj_exists(owner, code)
    if not exists:
        base.add_userproj(code, owner, proj_hrs, des_hrs, act_hrs)
    else:
        # TODO: Update
        pass

# Check if logged in user is admin return (bool)
def is_admin(eid):
    """ Check if user is an admin given an EID

    :param eid: Employee ID to check
    :return: Boolean True if user is an admin

    """

    return True

# Delete user or project by ID, return None if it fails/object is already deleted
def rm_proj(proj_id):
    """ Remove project from database

    :param proj_id: Project ID of target project

    """

    base.delete_project(proj_id)

def rm_user(user_id):
    """ Remove user from database

    :param user_id: Employee ID of target user

    """

    base.del_user(user_id)

# Push new rank to DB
## TODO: Is this redundant with `update_ranks()`?
#        Dan: No, this function adds a new rank to the db, 'update_ranks()' pulls the master rank list from db
def add_rank(rank):
    pass