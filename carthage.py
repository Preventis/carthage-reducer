from subprocess import call
import re
import json

# cache for `dependencies`
dependencies = dict()

# parses and represents a carthage dependency
class Dependency(object):
    def __init__(self, line, origin):
        self.line = line
        self.origin = origin
        match = re.match(r"^(?P<identifier>(github|git|binary)\s+\"[^/]+/(?:.+?)\")(?:\s+(?P<predicate>.+)?)?", line)
        self.identifier = match.group("identifier")
        self.predicate = match.group("predicate")
    
    def __str__(self):
        return "`{}` defined `{}`.".format(self.origin, self.predicate)

# function to cache one carthage dependency
def cache_dependency(line, origin):
    parsed_dependency = Dependency(line, origin)
    identifier = parsed_dependency.identifier
    if identifier in dependencies: # cache hit
        dependencies[identifier].append(parsed_dependency)
    else:
        dependencies[identifier] = [parsed_dependency]

# read in `CarthageConfig.json`
carthage_config = json.load(open("./Carthage/CarthageConfig.json"))

# 1. collecting all dependencies as specified in `CarthageConfig.json`
print("1. collecting all dependencies as specified in `CarthageConfig.json`")

# reading in each `Cartfile` as specified in `CarthageConfig.json`
for cartfile_path in carthage_config["cartfiles"]:
    cartfile = open(cartfile_path).read()
    lines = [line.strip() for line in cartfile.splitlines()]
    lines = list(filter(lambda x: len(x) > 0, lines))
    for line in lines:
        cache_dependency(line, cartfile_path)

# 2. checking for conflicts
print("2. checking for conflicts")
hasDiffer = False
for identifier in dependencies:
    children = dependencies[identifier]
    if len(children) == 1:
        continue
    differ = False
    first = children[0]
    for i in range(1, len(children)):
        current = children[i]
        differ = first.predicate != current.predicate
    if differ is True:
        hasDiffer = True
        print("entries for {} differ".format(identifier))
        for c in children:
            print("\t=> {}".format(c))
        print("")

if hasDiffer:
    print("...please resolve conflicts first!")
    raise SystemExit
print("...no conflicts found!")

# 3. writing overall `Cartfile`
print("3. writing overall `Cartfile`")
with open("./Cartfile", "w") as overall_cartfile:
    for dep in list(sorted(dependencies.values(), key=lambda dep: dep[0].identifier)):
        overall_cartfile.write(f"{dep[0].line}\n")

# 4. run `carthage update --platform iOS [...]`
call_chain =["carthage", "update", "--platform", "iOS"]
if carthage_config.get("no-use-binaries", False):
    call_chain.append("--no-use-binaries")
if carthage_config.get("cache-builds", False):
    call_chain.append("--cache-builds")
if carthage_config.get("use-ssh", False):
    call_chain.append("--use-ssh")
print(f"4. run `{' '.join(call_chain)}`")
call(call_chain)
