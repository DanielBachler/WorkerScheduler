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

    return []

# Search project and user by ID, return full row (as object?)
## FIXME: Get project by ID or user by iD? (this should be 2 different functions if so)

# Return current rank list
def get_ranks():
    """Fetch ranks from database

    :return: List of ranks

    """
    return []

# Push current rank list
def update_ranks(ranks):
    """Update ranks

    :param ranks: List of ranks

    """

    pass

# Send object (User, Project, UserProject) to db
def update_user(user):
    """Update a user

    :param user: Updated uer

    """

    pass

def update_project(proj):
    """Update a project

    :param proj: Updated project

    """

    pass

def update_userproj(uproj):
    """Update a user project

    :param uproj: Updated user project

    """

    pass

# Have projects be given unique ID in database upon creation (in here or elsewhere)
## FIXME: Database gives IDs to rows automatically upon insertion. Do we really need this function?

# Check if logged in user is admin return (bool)
def is_admin(eid):
    """ Check if user is an admin given an EID

    :param eid: Employee ID to check
    :return: Boolean True if user is an admin

    """

    return True

# Push all changes to DB? (May not be needed due to the way we are refactoring
## FIXME: More specific

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

# Update object in DB with a passed in object (not sure if needs to be separate from send object to DB
#   This does not really need to be a new method with current implementation, as objects get deleted, remade then put in
#   May want to make it a new method for clarity, not sure how database prefers ops to be
## FIXME: Not sure what this means

# Push new rank to DB
## TODO: Is this redundant with `update_ranks()`?
def add_rank(rank):
    pass