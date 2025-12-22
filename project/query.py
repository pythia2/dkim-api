import asyncio

import dns.asyncresolver
from dkim_selectors import SELECTORS


NAMESERVERS = ["8.8.8.8", "1.1.1.1"]
TIMEOUT = 2


async def gather_dns_results(domain):
    resolver = dns.asyncresolver.Resolver(configure=False)
    resolver.nameservers = NAMESERVERS
    resolver.timeout = TIMEOUT

    tasks = [async_resolve_dkim(selector, domain, resolver) for selector in SELECTORS]
    results = await asyncio.gather(*tasks)

    return results


async def async_resolve_dkim(selector, domain, resolver):
    qname = f"{selector}._domainkey.{domain}"
    try:
        answer = await resolver.resolve(qname, "TXT")
        if answer:
            if answer.chaining_result.cnames:
                record = []
                for item in answer:
                    remove_quotes = item.to_text().replace('" "', "")
                    remove_space = remove_quotes.replace('"', "")
                    record.append(remove_space)
                return {
                    "selector": selector,
                    "rdtype": "CNAME",
                    "query_name": qname,
                    "canonical_name": answer.canonical_name.to_text(),
                    "record": record,
                }

            else:
                record = []
                for item in answer:
                    remove_quotes = item.to_text().replace('" "', "")
                    remove_space = remove_quotes.replace('"', "")
                    record.append(remove_space)
                return {
                    "selector": selector,
                    "rdtype": "TXT",
                    "query_name": qname,
                    "canonical_name": answer.canonical_name.to_text(),
                    "record": record,
                }

    except Exception as e:
        return None
