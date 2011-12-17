# YUM Plugin that disallows an update of a package with a package
# from different vendor. Useful to keep packages compiled by yourself
# around while distribution pushes newer versions into repository.

# Copyright (c) 2011 Lubomir Rintel <lkundrak@v3.sk>
# Licensed under GNU GPL version 2 or later version at your
# option.

from yum.plugins import TYPE_CORE
import yum

requires_api_version = '2.1'
plugin_type = (TYPE_CORE,)

def exclude_hook (conduit):
	ts = conduit._base.rpmdb.readOnlyTS ()
	mi = ts.dbMatch ('name')
	rpms = {} 

	for rpm in mi:
		if not rpm.name in rpms:
			rpms[rpm.name] = []
		rpms[rpm.name].append (rpm.vendor)

	for po in conduit.getPackages ():
		if not po.name in rpms:
			continue
		if not po.vendor in rpms[po.name]:
			conduit.info (3, " --> %s from %s excluded (vendor)" % (po, po.repoid))
			conduit.delPackage (po)
