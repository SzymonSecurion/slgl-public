import os
import ansible_runner
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.playbook import Playbook
from ansible.template import Templar
from ansible.parsing.dataloader import DataLoader
from pytest import config

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

def ansible_syntax_check():
    # templ = """{{ lookup(
    #           'template', '%s/ansible/roles/sigia/templates/ansible_extra_vars.j2')
    #            }}""" % ( config.rootdir )
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources='local,')
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    pb = Playbook.load(config.rootdir + "/infrastructure/ansible/aws-security.yml", variable_manager=variable_manager, loader=loader)
    plays = pb.get_plays()
    localhost = inventory.get_host("local")
    for play in plays:
        variable_manager.set_host_facts(localhost, variable_manager.get_vars(play))
    # local_vars = variable_manager.get_vars(host=localhost)
    # templar = Templar(loader=loader, variables=local_vars)
    # extra_vars = templar.template(templ)
    # if extra_vars:
    #     variable_manager.extra_vars = extra_vars
    r = ansible_runner.run(
            private_data_dir=TEST_DIR,
            inventory='local,',
            playbook=str(config.rootdir) + '/infrastructure/ansible/aws-security.yml',
            # extravars=extra_vars,
            artifact_dir="/tmp/ansible",
            rotate_artifacts=5
        )
    return r


def test_ansible_cloud_init_sigia():
    ra = ansible_syntax_check()
    assert ra.status == "successful"
    print("apps: {}, StatusCode: {}".format(ra.status, ra.rc))

