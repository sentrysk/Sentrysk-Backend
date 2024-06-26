#!/usr/bin/env python3

# Libraries
##############################################################################

from SystemUsers.models import SystemUsers, ChangeLogSystemUsers
from SystemLastLogons.models import SystemLastLogons
from Agents.models import Agent
from SystemInstalledApps.models import SystemInstalledApps
from SystemServices.models import SystemServices
from PipPackages.models import InstalledPipPackages
from NpmPackages.models import InstalledNpmPackages
from DockerInfo.models import DockerInfo

##############################################################################


# Functions

# Get Agent Count
##############################################################################
def get_agent_count():
    try:
        # Get Agent Count & Return
        return Agent.objects.count()
    except Exception as e:
        return 0
##############################################################################

# Get User Count By Agent ID
##############################################################################
def get_sys_user_count_by_agent_id(agent_id):
    try:
        # Get System Users
        sys_users = SystemUsers.objects(agent=agent_id).first()
        # If exist
        if sys_users:
            return len(sys_users.users)
        return 0
    except Exception as e:
        return 0
##############################################################################
    
# Get All System Users Count
##############################################################################
def get_all_sys_user_count():
    try:
        # Get All Agents
        agents = Agent.objects()
        # Installed Apps
        all_sys_user_count = 0
        for agent in agents:
            agnt_sys_usr_cnt = get_sys_user_count_by_agent_id(agent.id)
            all_sys_user_count = all_sys_user_count + agnt_sys_usr_cnt

        return all_sys_user_count
    except Exception as e:
        return 0
##############################################################################
    
# Get User ChangeLog Count By Agent ID
##############################################################################
def get_sys_user_changelog_entry_count_by_agent_id(agent_id):
    chlg_count = 0
    try:
        # Get System Users
        sys_users = SystemUsers.objects(agent=agent_id).first()
        # If exist
        if sys_users:
            # Get ChangeLogs
            sys_users_chlg = ChangeLogSystemUsers.objects(sys_users=sys_users)
            # If any ChangeLog exists
            if sys_users_chlg:
                # Iterate over ChangeLogs
                for chlg in sys_users_chlg:
                    if chlg.changes.get('new_users'):
                        chlg_count = chlg_count + len(chlg.changes.get('new_users'))
                    
                    if chlg.changes.get('deleted_users'):
                        chlg_count = chlg_count + len(chlg.changes.get('deleted_users'))
                    
                    if chlg.changes.get('updated_users'):
                        chlg_count = chlg_count + len(chlg.changes.get('updated_users'))

        return chlg_count
    except Exception as e:
        print(e)
        return chlg_count
##############################################################################
    
# Get Last Logons Count by Agent ID
##############################################################################
def get_last_logons_by_agent_id(agent_id):
    try:
        # Get System Last Logons
        sys_last_logons = SystemLastLogons.objects(agent=agent_id).first()

        # If exist, return count
        if sys_last_logons:
            return len(sys_last_logons.last_logons)
        return 0
    except Exception as e:
        return 0
##############################################################################
    
# Get Installed Apps Count By Agent ID
##############################################################################
def get_sys_installed_apps_count_by_agent_id(agent_id):
    try:
        # Get System Users
        sys_installed_apps = SystemInstalledApps.objects(agent=agent_id).first()
        # If exist
        if sys_installed_apps:
            return len(sys_installed_apps.apps)
        return 0
    except Exception as e:
        return 0
##############################################################################
    
# Get All Installed Apps
##############################################################################
def get_all_installed_apps_count():
    try:
        # Get All Agents
        agents = Agent.objects()
        # Installed Apps
        all_installed_apps_count = 0
        for agent in agents:
            agnt_inst_app_cnt = get_sys_installed_apps_count_by_agent_id(agent.id)
            all_installed_apps_count = all_installed_apps_count + agnt_inst_app_cnt

        return all_installed_apps_count
    except Exception as e:
        return 0
##############################################################################
    
# Get Services Count By Agent ID
##############################################################################
def get_sys_services_count_by_agent_id(agent_id):
    try:
        # Get System Services
        sys_srvcs = SystemServices.objects(agent=agent_id).first()
        # If exist
        if sys_srvcs:
            return len(sys_srvcs.services)
        return 0
    except Exception as e:
        return 0
##############################################################################
    
# Get All Services Count (System Wide)
##############################################################################
def get_all_services_count():
    try:
        # Get All Agents
        agents = Agent.objects()
        # Installed Services
        all_services_count = 0
        for agent in agents:
            agnt_srvcs_cnt = get_sys_services_count_by_agent_id(agent.id)
            all_services_count = all_services_count + agnt_srvcs_cnt

        return all_services_count
    except Exception as e:
        return 0
##############################################################################
    
# Get Installed Pip Packages Count By Agent ID
##############################################################################
def get_sys_pip_pkgs_count_by_agent_id(agent_id):
    try:
        # Get System Users
        sys_pip_pkgs = InstalledPipPackages.objects(agent=agent_id).first()
        # If exist
        if sys_pip_pkgs:
            return len(sys_pip_pkgs.pip_packages)
        return 0
    except Exception as e:
        return 0
##############################################################################
    
# Get All Pip Packages
##############################################################################
def get_all_pip_pkgs_count():
    try:
        # Get All Agents
        agents = Agent.objects()
        # Pip Packages
        all_pip_pkgs_count = 0
        for agent in agents:
            agnt_inst_app_cnt = get_sys_pip_pkgs_count_by_agent_id(agent.id)
            all_pip_pkgs_count = all_pip_pkgs_count + agnt_inst_app_cnt

        return all_pip_pkgs_count
    except Exception as e:
        return 0
##############################################################################
    
# Get Installed NPM Packages Count By Agent ID
##############################################################################
def get_sys_npm_pkgs_count_by_agent_id(agent_id):
    try:
        # Get System Users
        sys_npm_pkgs = InstalledNpmPackages.objects(agent=agent_id).first()
        # If exist
        if sys_npm_pkgs:
            return len(sys_npm_pkgs.npm_packages)
        return 0
    except Exception as e:
        return 0
##############################################################################

# Get All NPM Packages
##############################################################################
def get_all_npm_pkgs_count():
    try:
        # Get All Agents
        agents = Agent.objects()
        # NPM Packages
        all_npm_pkgs_count = 0
        for agent in agents:
            agnt_inst_app_cnt = get_sys_npm_pkgs_count_by_agent_id(agent.id)
            all_npm_pkgs_count = all_npm_pkgs_count + agnt_inst_app_cnt

        return all_npm_pkgs_count
    except Exception as e:
        return 0
##############################################################################
    
# Get Installed Docker Count
##############################################################################
def get_installed_docker_count():
    try:
        # Get Docker Info Count
        return DockerInfo.objects(is_installed=True).count()
    except Exception as e:
        return 0
##############################################################################