import os
import ansible_runner
from pytest import config
import cfnlint.core
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def run_cfn_lint(filename):
    template = cfnlint.decode.cfn_yaml.load(filename)
    cfnlint.core.configure_logging(None)
    # W1020: Sub isn't needed if it doesn't have a variable defined
    ignore_rules = ["W1020", "E3010"]
    rules = cfnlint.core.get_rules([], ignore_rules, [])
    regions = ['eu-west-1']
    matches = cfnlint.core.run_checks(
        filename,
        template,
        rules,
        regions)
    for line in matches:
        logger.warning(str(line).replace(filename, "\n" + filename))
    assert len(matches) == 0
    logger.info("Linting finished for:{}".format(filename))


def test_generate_and_lint_template():
    r = ansible_runner.run(
        private_data_dir=TEST_DIR,
        # inventory='local,', # Supplied in env/cmdline directly
        playbook=str(config.rootdir) + '/infrastructure/ansible/aws-security.yml',
        artifact_dir="/tmp/ansible",
        rotate_artifacts=5,
        quiet=False
    )
    for each_host_event in r.events:
        tasks_to_be_validated = [
                                'Generate CloudFormation AWS Security templates'
                               ]
        try:
            if each_host_event['event_data']['task'] in tasks_to_be_validated:
                for result in each_host_event['event_data']['res']['results']:
                    print("Changed: {}, Failed: {} \t{}".format(result['changed'], result['failed'], result['item']))
                    assert result['failed'] == False
                    print(result)
                    if result['dest'].endswith('.yml'):
                        result_file_path = os.path.abspath(result['dest'])
                        print(result_file_path)
                        run_cfn_lint(result_file_path)
        except KeyError:
            pass
    assert r.status == "successful"
    print("Ansible playbook run status: {}".format(r.status))
