base = None


def init_dbwrapper(db):
    """ Initialize this wrapper

    :param db: Instance of database connection

    """

    global base
    base = db


# TODO: Make one of these for projects
def db_get_project_ids():
    res = base.db_query('''SELECT pid, project_name FROM project''')
    all = []
    for i in res:
        all.append((i[0], i[1]))
    return all


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


# Return a user object
def get_user(eid):
    user = base.db_query('''SELECT * FROM employee WHERE eid=%s;''' % eid)
    if user is None:
        return user
    return user[0]


# Return a user object
def is_user_admin(eid):
    user = base.db_query('''SELECT emp_role FROM employee WHERE eid=%s;''' % eid)
    if user is None:
        return False

    return user[0][0] > 0


# Return a project object and search by id
def get_project(pid):
    proj = base.db_query('''SELECT * FROM project WHERE pid="%s";''' % str(pid))
    if proj is None:
        return proj
    return proj[0]


# Gets a specific user project
# ARGS: billing_code (String), eid (String)
# RETURNS: uproj (List[]: A db row that contains information about a user project)
def get_user_project(billing_code, eid):
    uproj = base.db_query('''SELECT * FROM user_project WHERE eid="%s" && billing_code="%s";''' %
                          (str(eid), str(billing_code)))
    if uproj is None:
        return uproj
    return uproj[0]


# Gets a user's user project objects
# ARGS: eid (String): an employees ID's
# RETURNS: res (List[data_base_row]) a list of rows from the db table for user_projects
def get_users_projects(eid):
    res = base.db_query('''SELECT * FROM user_project WHERE eid="%s";''' % str(eid))
    return res


# get_projects_users:
# ARGS: pid (String)
# RETURNS: res (List[db rows containing user project])
def get_projects_users(pid):
    res = base.db_query('''SELECT * FROM user_project WHERE pid="%s"''' % str(pid))

    if res is None:
        return None
    return res


# Return current rank list
def get_bc_assignments():
    """Fetch billing code assignments from database

    :return: List of tuples (PID, code)

    """
    res = base.db_query('''SELECT * from billing_code_assignment;''')
    all = []

    for i in res:
        all.append((i[0], i[1]))

    return all


# Return current rank list
def get_ranks():
    """Fetch ranks from database

    :return: List of ranks

    """
    res = base.db_query('''SELECT * from emp_role;''')
    all = []

    for i in res:
        all.append(i[0])

    return all


# Push current rank list
def update_ranks(ranks):
    """Update ranks in database

    :param ranks: List of ranks

    """

    for rank in ranks:
        base.add_rank(rank)

def remove_rank(rank):
    base.remove_rank(rank)


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
    exists = base.db_query('''SELECT count(*) FROM user_project WHERE eid = %s AND billing_code = %s;''' % (eid, code))
    return exists[0][0] > 0


# Send object (User, Project, UserProject) to db
def update_user(eid, name, role, rate, mentor, rank):
    """Update a user in database

    :param user: Updated uer

    """

    exists = check_user_exists(eid)
    if mentor is None:
        mentor = "NULL"
    if not exists:
        base.create_user(eid, name, rank=rank, rate=rate, role=role, mentor=mentor)
    else:
        base.update_user(eid, name, rank=rank, rate=rate, role=role, mentor=mentor)


def update_project(pid, name, description, exp_hours, last_update="", rpt=False, start_mo="NULL", start_yr="NULL",
                   end_mo="NULL",
                   end_yr="NULL"):
    """Update a project in database

    :param proj: Updated project

    """

    exists = check_project_exists(name)
    if not exists:
        base.create_project(name, description, exp_hours, start_yr, start_mo, end_yr, end_mo, rpt)
    else:
        base.update_project(pid, name, description, exp_hours, start_yr, start_mo, end_yr, end_mo, rpt,
                            last_update=last_update)


def get_pid(name):
    pid = base.db_query('''SELECT pid FROM project WHERE project_name="%s"''' % name)
    return pid[0][0]


def update_userproj(pid, code, owner, proj_hrs="NULL", des_hrs="NULL", act_hrs="NULL"):
    """Update a user project in database

    :param uproj: Updated user project

    """

    exists = check_uproj_exists(owner, code)
    if not exists:
        base.add_userproj(pid, code, owner, proj_hrs, des_hrs, act_hrs)
    else:
        base.update_userproj(pid, code, owner, proj_hrs, des_hrs, act_hrs)


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

def rm_proj_object(eid, pid):
    """ Remove a project object from database

    @param pid: Project ID of target object
    @param eid: Employee ID of target user associated with object

    """
    base.rm_user_project(eid, pid)

def db_custom_query(stmt):
    """ Execute a custom query on the database

    :param stmt: A string containing an SQL statement
    :return: a 2-dimensional table containing the results of the query

    """

    return base.db_query(stmt)