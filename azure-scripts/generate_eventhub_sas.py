import time
import urllib.parse
import hmac
import hashlib
import base64
import re
import os


def get_auth_token(sb_name, eh_name, sas_name, sas_value):
    """
    Returns an authorization token dictionary
    for making calls to Event Hubs REST API.
    """
    uri = urllib.parse.quote_plus(
        "https://{}.servicebus.windows.net/{}".format(sb_name, eh_name)
    )
    sas = sas_value.encode("utf-8")
    expiry = str(int(time.time() + 7 * 24 * 60 * 60))
    string_to_sign = (uri + "\n" + expiry).encode("utf-8")
    signed_hmac_sha256 = hmac.HMAC(sas, string_to_sign, hashlib.sha256)
    signature = urllib.parse.quote(base64.b64encode(signed_hmac_sha256.digest()))
    return {
        "sb_name": sb_name,
        "eh_name": eh_name,
        "token": "SharedAccessSignature sr={}&sig={}&se={}&skn={}".format(
            uri, signature, expiry, sas_name
        ),
    }


if __name__ == "__main__":
    # Fluentd configuration file
    fluentd_config_file = "/home/azureuser/nsm/td-agent.conf"

    # Event Hub namespace
    sb_name = ""

    # Token for Zeek
    eh_name_zeek = ""
    sas_name_zeek = ""
    sas_value_zeek = ""
    token_zeek = get_auth_token(sb_name, eh_name_zeek, sas_name_zeek, sas_value_zeek)

    # Token for Suricata
    eh_name_suricata = ""
    sas_name_suricata = ""
    sas_value_suricata = ""
    token_suricata = get_auth_token(
        sb_name, eh_name_suricata, sas_name_suricata, sas_value_suricata
    )

    # Update td-agent.conf with new tokens
    with open(fluentd_config_file, "r") as file:
        config = file.read()
        pattern_zeek = re.compile(
            r'Authorization": "SharedAccessSignature sr=.*?&skn={}"'.format(
                sas_name_zeek
            )
        )
        pattern_suricata = re.compile(
            r'Authorization": "SharedAccessSignature sr=.*?&skn={}"'.format(
                sas_name_suricata
            )
        )

        config = pattern_zeek.sub(f'Authorization": "{token_zeek["token"]}"', config)
        config = pattern_suricata.sub(
            f'Authorization": "{token_suricata["token"]}"', config
        )

    with open(fluentd_config_file, "w") as file:
        file.write(config)

    # Restart Fluentd
    os.system("docker restart fluentd")
