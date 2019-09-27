# close loop automation workflow based on Red Hat Ansible and Forward Enterprise

<aside class="notice">
DISCLAIMER: All the code in this repository is distributed with no warranty and
no support from Forward Networks
</aside>

This repository includes all the code used to demo a close loop automation
workflow based on Red Hat Ansible and Forward Enterprise.

[Forward Enterprise](https://www.forwardnetworks.com/network-automation-software/)
documents, searches, verifies, and predicts the behavior of your network by
creating an always-accurate software copy of your entire network infrastructure
for both on-prem and cloud.

## Demo use case
a customer is introducing a new service and wants to implement a completed automated workflow to Verify routing, Test new security rules, Deploy
security policies, Verify new service connectivity, Check for side effects,
Rollback on failure, Send start and final status notifications.

In this demo, Ansible is used for Network Configuration as well to interact
with Forward Enterprise, which provides the Network Verification component
of the close loop automation.

![Verification](./images/close_loop_verification.png?width=800px&classes=shadow)

## Demo framework
The framework is based on common practices like:
 * *Network as Code* using a GitHub repository to store all the Ansible
     playbooks, Python scripts, workflow description (pipeline) and documentation
 * *Continuous Integration and Continuous Deployments (CI/CD)* to streamline the
    entire process using Jenkins as orchestration server.

![CI-CD](images/CI-CD.png?width=800px&classes=shadow)

The pictures below shows the entire process:

![Jenkins](images/jenkins_pipeline.png?width=800px&classes=shadow)

The entire workflow, called pipeline in Jenkins, is split in several stages, each consisting of several steps:

1. Download code from GitHub and gather user inputs:

   * Download code from the GitHub repository (this repository)
   * Send a message to a ChatOps Slack channel to let the operation team know
     a new service deployment has started and providing a direct link to the
     Jenkins pipeline run
   * Gather user inputs about the new service like service name, ip and clients
     network

     ![User Inputs](images/user_inputs.png?width=800px&classes=shadow)

2. Check if change is needed using the Forward [Path Search](https://app.forwardnetworks.com/api-doc#path-search) APIs

    * Get the service Path Search  from the Forward platform using the Ansible
      URI module ([get_path.yml](get_path.yml))
    * run a Python script to verify if the routing and the security policies are ok.
      If the routing is not fine, exit with a message to fix routing   ([is_change_needed.yml](is_change_needed.yml))
      If both routing and security policies are ok, exit. No need to do anything.
      If routing is ok and security policies are not, proceed with the following stages.

3.    Verify change in Sandbox:

     * Build the new firewall configuration ([sandbox_config_build.yml](sandbox_config_build.yml)) by:
        * build new rule and address object configuration snippets for the new
          service using Ansible Jinja2 templates
        * downloading the current firewall configuration from the Forward platform
        * Merge the current config with the new configuration snippets using a Python
          script
      * Upload the new firewall configuration to the Forward Platform and reprocess
         all the platform data ([sandbox_save_changes.yml](sandbox_save_changes.yml))
      * Create a new Forward Intent Check for the new service ([intent_check_new_service.yml](intent_check_new_service.yml))
      * Get all the Forward Predefined and Intent Checks ([get_checks.yml](get_checks.yml))
      * Make sure all the checks are passing ([verify_checks.yml](verify_checks.yml)), otherwise fail
        the Pipeline

4. Apply network change to production

      * Deploy the new address object and security rule to a Palo Alto Networks
        firewall by running an Ansible playbook based on the panos module ([deploy_changes.yml](deploy_changes.yml))

5. Verify new connectivity and check for regressions

      * Collect config and state from the modified devices only and make sure
        collection and processing are over before proceeding ([take_partial_collection.yml](take_partial_collection.yml))
      * Get all Checks using Ansible URI module ([get_checks.yml](get_checks.yml))
      * Make sure all the checks are passing ([verify_checks.yml](verify_checks.yml))
        rollback firewall changes ([rollback_changes.yml](rollback_changes.yml))

6. Send a final message to the Slack channel with the final status and pipeline
   run link

   ![slack](images/slack.png?width=800px&classes=shadow)

# Prerequisites:
 1. A linux server with the following software:
   * Jenkins server
   * Red Hat Ansible
   * The Ansible Forward modules and the Forward APIs bindings following the instruction at [fwd-ansible](https://github.com/forwardnetworks/fwd-ansible)
 2. A Network environment that includes a Palo Alto Network firewall in between
    the server running the new service and the clients

<aside class="notice">
If you have a different firewall then a Palo Alto Network in your setup, you need to modify the
Jinja2 templates for the given firewall platform
</aside>

# Demo setup

To reproduce this demo you need to:

 * Create a fork if this repository
 * Clone the fork
 * If you are using a proxy server to connect to the Palo Alto Firewall,
   modify the proxy server access detail in the ([Jenkinsfile](Jenkinsfile)),
   otherwise replace the remote execution with a local execution.
 * Commit and push the changes to the fork
 * Create a new Jenkins Pipeline and connect it the GitHub fork
 * Run the pipeline. This will download all the code into the pipeline workspace
   Check the WORKSPACE environment variable for details
 * Move to the workspace directory and set up the properties file from the sample

```
   cp fwd-ansible.properties.sample fwd-ansible.properties
```

   Fill in the content to match your Forward instance and network
 * Run the pipeline again to test the demo
