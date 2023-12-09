ml2_addr = "C:\\src\\marioland2\\"
world_addr = "c:\\src\\archipelago\\worlds\\marioland2\\"

file = open(ml2_addr + "ml2.sym", "r")
data = file.read()
file.close()
file = open(world_addr + "rom_addresses.py", "w")
file.write("rom_addresses = {\n")
count = 0
for line in data.split("\n"):
    if ".Archipelago_" in line:
        address = line.split(" ")[0]
        address = address.split(":")
        if int(address[0], 16) == 0:
            address = int(address[1], 16)
        else:
            address = (int(address[0], 16) * 0x4000) + int(int(address[1], 16) - 0x4000)
        label = line.split(".")[-1]
        offset = int(label.split("_")[-1])
        address += offset
        label = "_".join(label.split("_")[1:-1])

        file.write("    \"" + label + "\": " + hex(address) + ",\n")
        count += 1


file.write("}\n")
file.close()

with open(ml2_addr + "baserom.gb", "br") as file:
    sml2base = bytes(file.read())

with open(ml2_addr + "sml2.gb", "br") as file:
    sml2ap = bytes(file.read())


import bsdiff4
patch = bsdiff4.diff(sml2base, sml2ap)

with open(world_addr + "basepatch.bsdiff4", "bw") as file:
    file.write(patch)