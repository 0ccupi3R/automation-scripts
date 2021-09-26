## Curated list of `bash scripts` to make your life easy while working on AWS resources (soon other Cloud Providers will be added).


### 1. To update your `Security Group` ingress rules
Majority of us do not have static ip configured on our Router, which means it keeps getting updated dynamically (auto-assigned). So, with traditional approach, it is bit time consuming process to manually IP in Security Groups ingress rules.

:astonished: Now what ? Why don't we make it simple for us or even automate it !

#### Prequisites :
1. AWS Cli configured (with/without SSO). Generate the credentails (using Key-pairs / STS) and validate if it is saved in `~/.aws/credentials`
2. [A Script](https://github.com/0ccupi3R/automation-scripts/blob/main/aws-scripts/aws-sg-update.sh), obviously 

#### Steps :
1. Copy script in your system, say `/opt/aws-sg-update.sh`
2. Replace `home-router` with your sg-group-name, if possible then use same sg-group-name for mutiple AWS accounts.
3. To configure it as a command, add an alias in `~/.bashrc`
```bash
alias sg-update="sh /opt/aws-sg-update.sh"
```
4. Then reload your profile using command `source ~/.bashrc`
5. Finally, you are good to go to execute your command
```bash
aws-sg-update.sh udp 53 dev
```
**Note:** `dev` is a aws profile name (use if you have multiple accounts)

**Commandline Output**
```json
{
    "Return": true,
    "SecurityGroupRules": [
        {
            "SecurityGroupRuleId": "sgr-01234567890123456",
            "GroupId": "sg-01234567890123456",
            "GroupOwnerId": "012345678901",
            "IsEgress": false,
            "IpProtocol": "udp",
            "FromPort": 53,
            "ToPort": 53,
            "CidrIpv4": "1.2.4.5/32"
        }
    ]
}
```
**AWS Console Output**
![ DNS Port (53) Added in Security Group](https://github.com/0ccupi3R/automation-scripts/blob/main/aws-scripts/aws-sg-update-snapshot-1.png)

**Note:** Few tweaks that can be done :
* Adding more arguments in `aws` command
* To automate, configure `CRONTAB` for your script (with hardcoded parameters)
* Add your slack/telgram `webhook` to get message when SG gets updated
