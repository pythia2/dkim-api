example_response = {
    "status": "success",
    "code": 200,
    "dkim_keys_found": 5,
    "domain": "kalf.me",
    "data": [
        {
            "selector": "fm1",
            "record_type": "CNAME",
            "original_query": "fm1._domainkey.kalf.me.",
            "cname_target": "fm1.kalf.me.dkim.fmhosted.com.",
            "records": [
                "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4zlu37P..."
            ],
        },
        {
            "selector": "default",
            "record_type": "TXT",
            "original_query": "default._domainkey.kalf.me.",
            "cname_target": None,
            "records": [
                "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4zlu37P..."
            ],
        },
    ],
    "meta": {"timestamp": "2023-10-27T10:00:00Z", "request_id": "req_8923749823"},
}
