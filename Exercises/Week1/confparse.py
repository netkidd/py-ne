#!/usr/bin/env python
'''

ciscoconfparse
8. Write a Python program using ciscoconfparse that parses this config file.
Note, this config file is not fully valid (i.e. parts of the configuration
are missing). The script should find all of the crypto map entries in the file
(lines that begin with 'crypto map CRYPTO') and for each crypto map entry
print out its children.

9. Find all of the crypto map entries that are using PFS group2

10. Using ciscoconfparse find the crypto maps that are not using AES (based-on
the transform set name). Print these entries and their corresponding transform
set name.
'''
from ciscoconfparse import CiscoConfParse


cisco_cfg = CiscoConfParse("cisco_show_run_example")


crypto_maps = cisco_cfg.find_objects(r"^crypto map CRYPTO")


for cr_map in crypto_maps:
    print(cr_map.text)
    for child in cr_map.children:
        print(child.text)


crypto_maps_pfs2 = cisco_cfg.find_objects_w_child(parentspec=r"^crypto map CRYPTO", childspec=r"^\sset pfs group2")

print("\nSecond exercise\n")
for cr_map in crypto_maps_pfs2:
    print(cr_map.text)
    for child in cr_map.children:
        print(child.text)

crypto_maps_no_aes = cisco_cfg.find_objects_wo_child(parentspec=r"^crypto map CRYPTO", childspec=r".*AES.*")


print("\nThird exercise\n")
for cr_map in crypto_maps_no_aes:
    print(cr_map.text)
    transformset = cr_map.re_search_children(r".*transform-set.*")
    print(transformset[0].text)
