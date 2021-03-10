import deploy.client as slgl
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

slgl.private_key = "sk_live_mwUCDbuyCyv1xXANBWOrM5PG"
user = "admin"

def handler(event, context):
    verify_domain = "aaa.test.com"
    slgl.link("http://sigia.com/users/{}#verified_domains".format(user),
              "https://types.sigia.com/verified_domain",
              verify_domain)

    main_id = "http://{}/it/1584452827889-MOE9Wz/".format(verify_domain)

    type = {
        "@type": {
            "anchors": [{
                "@id": "#child",
                "@type": "http://example.com/it/1584452827889-MOE9Wz/1/child-type"
            }]
        }
    }
    slgl.post(main_id + "3/parent", type)

    type_id = main_id + "1/type_with_state_property"

    type_request = {
        "state_properties": ["value"]
    }

    slgl.post(type_id, "https://types.sigia.com/type", type_request)

    state_request = {
        "value": "foo",
        "xxx": "zzz"
    }
    slgl.post(main_id + "it/1584452827889-MOE9Wz/test",type_id, state_request)

    state = slgl.get(main_id + "it/1584452827889-MOE9Wz/test")
    state_json = state.json()
    print(state_json["@state"]["value"])
