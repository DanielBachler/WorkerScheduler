from lib import object

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

# Send object (User, Project, UserProject) to db
def update_user(eid, name, role, rate, mentor, rank):
    """Update a user in database

    :param user: Updated uer

    """

    exists = base.db_query("SELECT count(*) FROM employee WHERE eid = %d;" % int(eid))
    print(exists)
    if exists[0][0] == 0:
        if mentor is None:
            mentor = "NULL"
        base.create_user(eid, name, rank=rank, rate=rate, role=role, mentor=mentor)
    else:
        pass
        # TODO: Update

def update_project(proj):
    """Update a project in database

    :param proj: Updated project

    """

    pass

def update_userproj(uproj):
    """Update a user project in database

    :param uproj: Updated user project

    """

    pass

# Have projects be given unique ID in database upon creation (in here or elsewhere)
## FIXME: Database gives IDs to rows automatically upon insertion. Do we really need this function?
# TODO: No, all we need is the ability to get and reference IDs if they are made by db good enough

# Check if logged in user is admin return (bool)
def is_admin(eid):
    """ Check if user is an admin given an EID

    :param eid: Employee ID to check
    :return: Boolean True if user is an admin

    """

    return True

# Push all changes to DB? (May not be needed due to the way we are refactoring
## FIXME: More specific
# TODO: After looking at how the refactor will go, this function is most likely not needed.
#       Since all changes are pushed to db at time of change

# Delete user or project by ID, return None if it fails/object is already deleted
def rm_proj(proj_id):
    """ Remove project from database

    :param proj_id: Project ID of target project

    """

    pass

def rm_user(user_id):
    """ Remove user from database

    :param user_id: Employee ID of target user

    """

    pass

# Push new rank to DB
## TODO: Is this redundant with `update_ranks()`?
#        Dan: No, this function adds a new rank to the db, 'update_ranks()' pulls the master rank list from db
def add_rank(rank):
    pass