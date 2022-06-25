#!/bin/bash
# Author: Sam Drobakha, sam.drobakha@gmail.com, https://github.com/SamDrobakha
set +x

REPO_LOCATION="/Users/sam/REPO"
KEYS_LOCATION=${REPO_LOCATION}/keys

# keys
snn_git_key=${KEYS_LOCATION}/smithnephew/sam-drobakha-smith-ssh-gitlab-key
myp_git_key=${KEYS_LOCATION}/myp/sam-drobakha-myp-ssh-gitlab-key
my_git_key=${KEYS_LOCATION}/my/github-SamDrobakha/sam_drobakha_personal_github_key


function set() {
    ssh-add -D
    ssh-add ${needed_key}
}


function main() {
    choose
    set
}


function main() {
    local param
    while [[ $# -gt 0 ]]; do
        param="$1"
        shift
        case $param in
            myp)
                needed_key=${myp_git_key}
                set
                ;;
            snn)
                needed_key=${snn_git_key}
                set
                ;;
            my)
                needed_key=${my_git_key}
                set
                ;;
            *)
                echo "Error: invalid parameter"
                ;;
        esac
    done
}

main $@
