import asyncio

import dns.asyncresolver
from dkim_selectors import SELECTORS


async def async_resolve_dkim(selector, domain, resolver):
    qname = f"{selector}._domainkey.{domain}"
    try:
        # Resolver is pre-configured with nameservers
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

        # return None
    except Exception as e:
        return None  # return f"Error for {qname}: {e}"
        # If this list is not empty, a CNAME was followed


# domain = "kalf.me"
nameservers = ["8.8.8.8", "1.1.1.1"]


async def bulk_lookup_resolver(domain):
    # Configure the resolver once
    resolver = dns.asyncresolver.Resolver(configure=False)
    resolver.nameservers = nameservers  # e.g., ['8.8.8.8', '1.1.1.1']
    resolver.timeout = 2

    tasks = [async_resolve_dkim(selector, domain, resolver) for selector in SELECTORS]
    results = await asyncio.gather(*tasks)

    return results


# print("==============================================================")
# print("==============================================================")
# print(f"answer.canonical_name = {answer.canonical_name}")
# print(
#     f"answer.chaining_result.answer = {answer.chaining_result.answer}"
# )
# print(
#     f"answer.chaining_result.canonical_name = {answer.chaining_result.canonical_name}"
# )
# print(
#     f"answer.chaining_result.cnames = {answer.chaining_result.cnames}"
# )
# print(
#     f"answer.chaining_result.minimum_ttl = {answer.chaining_result.minimum_ttl}"
# )
# # print(f"answer.expiration = {answer.expiration}")
# print(f"answer.nameserver = {answer.nameserver}")
# # print(f"answer.port = {answer.port}")
# print(f"answer.qname = {answer.qname}")
# # print(f"answer.rdclass = {answer.rdclass}")
# # print(f"answer.rdtype = {answer.rdtype}")
# # print(f"answer.response = {answer.response}")
# # print(f"answer.rrset = {answer.rrset}")
# print("==============================================================")
