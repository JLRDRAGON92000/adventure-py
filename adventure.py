### Libraries ###
import random;
import sys;

### Debug mode ###
termargs=sys.argv;

if len(termargs)>1:
	if termargs[1]=="debug":
		debugmode=True;
else:
	debugmode=False;


if debugmode:
	print("");
	print("Initializing...");

#############################
# Initialize game variables #
#############################

if debugmode:
	print("Initializing game variables...");

# Main variables
cmd="nil";
x=0;
y=0;
z=0;
nummoves=0;
noitems=False;
score=0;
maxscore=0;
curvehicle=None;

# Cheat variables
cheatmode=False;
noclip=False;
takeeverything=False;
godmode=False;

if debugmode:
	print("Done.");

###########################
# Initialize dictionaries #
###########################

if debugmode:
	print("Initializing global dictionaries...");

# Rooms
global roomdict;
roomdict=[];
# Items
global itemdict;
itemdict=[];
# Computers
global compdict;
compdict=[];
# Vehicles
global vehicledict;
vehicledict=[];
# Portals
global portaldict;
portaldict=[];
# Death zones
global killzonedict;
killzonedict=[];

if debugmode:
	print("Done.");

#########
# Items #
#########

if debugmode:
	print("Initializing items...");

class item:
	# Identification
	name="";
	spec_gndtitle=None;
	spec_invtitle=None;
	spec_gndphrase=None;
	cmdaliases=[];
	desc=None;
	# Item properties
	weight=0;
	treasure=False;
	takeable=True;
	silent=False;
	treasuredrop=False;
	spec_lookaction=None;
	def __init__(self):
		itemdict.append(self);

# lamp
lamp=item();
lamp.name="a lamp";
lamp.cmdaliases=["lamp"];
lamp.desc=None;
lamp.weight=4;
lamp.treasure=False;

# shovel
shovel=item();
shovel.name="a shovel";
shovel.cmdaliases=["shovel"];
shovel.desc=None;
shovel.weight=10;
shovel.treasure=False;

# key
key=item();
key.name="a key";
key.spec_gndtitle="a shiny brass key";
key.spec_invtitle="a brass key";
key.cmdaliases=["key"];
key.desc=None;
key.weight=0.2;
key.treasure=False;

# dropchute
dropchute=item();
dropchute.name="a chute";
dropchute.cmdaliases=["chute"];
dropchute.desc=None;
dropchute.weight=0;
dropchute.takeable=False;
dropchute.silent=True;
dropchute.treasuredrop=True;

# money
money=item();
money.name="a $100 bill";
money.cmdaliases=["bill"];
money.desc=None;
money.weight=0.1;
money.treasure=True;

# coins
coins=item();
coins.name="some valuable coins";
coins.cmdaliases=["coins"];
coins.desc=None;
coins.weight=2;
coins.treasure=True;

# laptop
laptop=item();
laptop.name="a laptop";
laptop.cmdaliases=["laptop"];
laptop.desc="The laptop still appears to work.\n\n(Use the \"type\" command to use computers)";
laptop.weight=4;
laptop.spec_gndphrase="There is a laptop resting on a table nearby.";

if debugmode:
	print("Done.");

############
# Vehicles #
############

#####################################################
# Vehicle class system								#
# ===============================================	#
# Class 0: Small vehicles, such as bikes and ATVs	#
# Class 1: Midsize vehicles, such as cars			#
# Class 2: Larger vehicles, such as buses			#
# Class 3: Aircraft									#
# Class 4: Watercraft								#
#####################################################

if debugmode:
	print("Initializing vehicles...");

class vehicle:
	# Identification
	name="";
	desc="";
	cmdaliases=[];
	desc=None;
	vclass=0;
	# Position
	xpos=None;
	ypos=None;
	zpos=None;
	def __init__(self):
		vehicledict.append(self);

# bicycle
bicycle=vehicle();
bicycle.name="a bicycle";
bicycle.cmdaliases=["bicycle","bike"];
bicycle.desc=None;
bicycle.vclass=0;

# bus
bus=vehicle();
bus.name="a bus"
bus.cmdaliases=["bus"];
bus.desc=None;
bus.vclass=2;

# boat
boat=vehicle();
boat.name="a boat";
boat.cmdaliases=["boat"];
boat.desc=None;
boat.vclass=4;

if debugmode:
	print("Done.");

#############
# Computers #
#############

if debugmode:
	print("Initializing computers...");

class cfile:
	name="";
	ext="";
	canopen=True;
	data="";
	def __init__(self,namel,extl,canopenl,datal):
		self.name=namel;
		self.ext=extl;
		self.canopen=canopenl;
		self.data=datal;

class computer:
	# Identification
	hostname="";
	availusers=None;
	assoc=None;
	exitmsg="";
	exitmsg_inv=""
	portable=False;
	# File system
	driveltr="C"
	drivelbl="";
	driveser="0000-0000";
	dirhierarchy={};
	def __init__(self):
		compdict.append(self);

# comp_laptop
comp_laptop=computer();
comp_laptop.hostname="L019385-12";
comp_laptop.assoc=laptop;
comp_laptop.exitmsg="You close the laptop and step back.";
comp_laptop.exitmsg_inv="You close the laptop and stash it in your inventory.";
comp_laptop.portable=True;
comp_laptop.driveltr="D";
comp_laptop.drivelbl="OFFLINEDATA";
comp_laptop.driveser="49F3-AC3B";
comp_laptop.dirhierarchy={
	"random.txt":cfile(
		namel="random.txt",
		extl="txt",
		datal="lol",
		canopenl=True
	)
};

def compcmdinterpret(command):
	command=str(command).lower();
	cmds="";
	cmdl=[];
	for cmdc in command:
		if cmdc==" " or cmdc=="\n" or cmdc=="\t":
			cmdl.append(cmds);
			cmds="";
		else:
			cmds=cmds+cmdc;	   
	cmd=cmdl[0];
	args=cmdl[1:];
	return cmd,args;

def compCmdProcessor(comp,isInv):
	# Commands recognized by computer
	dirList=["dir"];
	fileData=["type"];
	returnToGame=["exit"];
	
	while True:
		# Read input
		ccmdin=str(input(comp.driveltr+":\\>"))+"\n";
		ccmd,cargs=compcmdinterpret(ccmdin);
	
		if ccmd in dirList:
			numfiles=0;
			numbytes=0;
			if comp.drivelbl=="":
				print(" Volume in drive "+comp.driveltr+" has no label.");
			else:
				print(" Volume in drive "+comp.driveltr+" is "+comp.drivelbl);
			print(" Volume serial number is "+comp.driveser);
			print("\n Directory of "+comp.driveltr+":\\");
			for fkey,filel in comp.dirhierarchy.items():
				formstr="02/28/2014  02:08 PM    {} {}";
				print(formstr.format(str(len(filel.data)),filel.name));
				numfiles+=1;
				numbytes+=len(filel.data);
			print("               {0} File(s)    {1} bytes".format(numfiles,numbytes));
	
		elif ccmd in fileData:
			if len(cargs)<1:
				print("Bad command or file name");
			else:
				for fkey,filel in comp.dirhierarchy.items():
					if filel.name==cargs[0]:
						print(filel.data);
						break;
				else:
					print("Bad command or file name");
	
		elif ccmd in returnToGame:
			if isInv:
				print(comp.exitmsg_inv);
			else:
				print(comp.exitmsg);
			return 0;
	
		elif ccmd=="":
			continue;
		else:
			print("Bad command or file name");

if debugmode:
	print("Done.");

#########
# Rooms #
#########

# Regular max desc line length = 62 chars

if debugmode:
	print("Initializing rooms...");

walls_all=["north","south","east","west","up","down","northeast","northwest","southeast","southwest"];

class room:
	# Identification
	name="";
	desc="";
	# Position
	xpos=0;
	ypos=0;
	zpos=0;
	# Passable walls
	openwalls=[];
	# Passable walls with key
	lockwalls=[];
	# Vehicle-passable walls
	vwalls_class0=[];
	vwalls_class1=[];
	vwalls_class2=[];
	vwalls_class3=[];
	vwalls_class4=[];
	# Other room-local variables
	dark=False;
	visited=False;
	# Objects in room
	diggables=[];
	items=[];
	vehicles=[];
	
	# Functions
	def __init__(self):
		roomdict.append(self);
	def openwall(self,direction):
		self.openwalls.append(direction);
	def lockwall(self,direction):
		self.lockwalls.append(direction);
	def closewall(self,direction):
		self.openwalls.remove(direction);
		self.lockwalls.remove(direction);

# Null room
null_room=room();
null_room.name="nil";
null_room.desc="nil";
null_room.xpos=None;
null_room.ypos=None;
null_room.zpos=None;
null_room.openwalls=walls_all;
null_room.lockwalls=[];
null_room.vwalls_class0=null_room.openwalls;
null_room.vwalls_class1=null_room.openwalls;
null_room.vwalls_class2=null_room.openwalls;
null_room.vwalls_class3=null_room.openwalls;
null_room.vwalls_class4=null_room.openwalls;
null_room.dark=False;
null_room.diggables=[];
null_room.items=[];

# Barren moor
barren_moor=room();
barren_moor.name="Barren moor";
barren_moor.desc="""\
You are on a barren moor. The surrounding area is in ruins,
and appears to have been abandoned long ago. You see a small
wooden footbridge to the east.""";
barren_moor.xpos=0;
barren_moor.ypos=0;
barren_moor.zpos=0;
barren_moor.openwalls=["east"];
barren_moor.lockwalls=[];
barren_moor.dark=False;
barren_moor.diggables=[];
barren_moor.items=[shovel]

# Meadow
meadow=room();
meadow.name="Meadow";
meadow.desc="""\
You are in a meadow. A dirt path leads to the east towards a
building, while a bridge leads west.""";
meadow.xpos=1;
meadow.ypos=0;
meadow.zpos=0;
meadow.openwalls=["east","west"];
meadow.lockwalls=[];
meadow.dark=False;
meadow.diggables=[key];
meadow.items=[];

# Winners' room
winners_room=room();
winners_room.name="Winners' room";
winners_room.desc="""\
You are in a small room, with the words "Winners' Circle"
written on the walls. There are doors to the north and
west.""";
winners_room.xpos=2;
winners_room.ypos=0;
winners_room.zpos=0;
winners_room.openwalls=["west"]
winners_room.lockwalls=["north"];
winners_room.dark=False;
winners_room.diggables=[];
winners_room.items=[laptop];

# Last room
last_room=room();
last_room.name="Last room";
last_room.desc="""\
This is the last room to be implemented for now. Mounted to the wall,
there is a chute marked 'put treasures here for points'. There
are doors to the north and south.""";
last_room.xpos=2;
last_room.ypos=1;
last_room.zpos=0;
last_room.openwalls=["north"];
last_room.lockwalls=["south"];
last_room.dark=False;
last_room.diggables==[];
last_room.items=[money,dropchute];

# South end of N/S hallway
south_end_of_ns_hallway=room();
south_end_of_ns_hallway.name="South end of N/S hallway";
south_end_of_ns_hallway.desc="""\
You are at the south end of a north/south hallway. There is a door
to the south, and a room to the west.""";
south_end_of_ns_hallway.xpos=12;
south_end_of_ns_hallway.ypos=34;
south_end_of_ns_hallway.zpos=0;
south_end_of_ns_hallway.openwalls=["north","south","west"];
south_end_of_ns_hallway.lockwalls=[];
south_end_of_ns_hallway.dark=False;
south_end_of_ns_hallway.diggables=[];
south_end_of_ns_hallway.items=[];

# North end of N/S hallway
north_end_of_ns_hallway=room();
north_end_of_ns_hallway.name="North end of N/S hallway";
north_end_of_ns_hallway.desc="""\
You are at the north end of a north/south hallway. There are doors
to the north and east.""";
north_end_of_ns_hallway.xpos=12;
north_end_of_ns_hallway.ypos=35;
north_end_of_ns_hallway.zpos=0;
north_end_of_ns_hallway.openwalls=["north","south"];
north_end_of_ns_hallway.lockwalls=[];
north_end_of_ns_hallway.dark=False;
north_end_of_ns_hallway.diggables=[];
north_end_of_ns_hallway.items=[];

# Overlook
overlook=room();
overlook.name="Overlook";
overlook.desc="""\
You are at the top of a very tall cliff. The cliff wall drops
off to the north. There is a door to the south leading into a
building."""
overlook.xpos=12;
overlook.ypos=36;
overlook.zpos=0;
overlook.openwalls=["north","south"];
overlook.lockwalls=[];
overlook.dark=False;
overlook.diggables=[];
overlook.items=[];

# Supply closet
supply_closet=room();
supply_closet.name="Supply closet";
supply_closet.desc="""\
You are in a small supply closet. It appears to have been
ransacked, and nearly all of the contents are gone. There
is a door out to the east, and a ladder leads down a hole.""";
supply_closet.xpos=11;
supply_closet.ypos=34;
supply_closet.zpos=0;
supply_closet.openwalls=["east","down"];
supply_closet.lockwalls=[];
supply_closet.dark=True;
supply_closet.diggables=[];
supply_closet.items=[];

# SW end of NE/SW passage
sw_end_of_nesw_passage=room();
sw_end_of_nesw_passage.name="SW end of NE/SW passage";
sw_end_of_nesw_passage.desc="""\
You are at the southwest end of a northeast/southwest passage.
A ladder leads up into the distance.""";
sw_end_of_nesw_passage.xpos=11;
sw_end_of_nesw_passage.ypos=34;
sw_end_of_nesw_passage.zpos=-1;
sw_end_of_nesw_passage.openwalls=["up","northeast"];
sw_end_of_nesw_passage.lockwalls=[];
sw_end_of_nesw_passage.dark=True;
sw_end_of_nesw_passage.diggables=[];
sw_end_of_nesw_passage.items=[];

# NE end of NE/SW passage
ne_end_of_nesw_passage=room();
ne_end_of_nesw_passage.name="NE end of NE/SW passage";
ne_end_of_nesw_passage.desc="""\
You are at the northeast end of a northeast/southwest passage.""";
ne_end_of_nesw_passage.xpos=12;
ne_end_of_nesw_passage.ypos=35;
ne_end_of_nesw_passage.zpos=-1;
ne_end_of_nesw_passage.openwalls=["southwest"]
ne_end_of_nesw_passage.lockwalls=[];
ne_end_of_nesw_passage.dark=True;
ne_end_of_nesw_passage.diggables=[];
ne_end_of_nesw_passage.items=[coins];

if debugmode:
	print("Done.");

###########
# Portals #
###########

if debugmode:
	print("Initializing portals...");

class portal:
	xpos=0;
	ypos=0;
	zpos=0;
	targetx=0;
	targety=0;
	targetz=0;
	def __init__(self):
		portaldict.append(self);

# tstportal1
tstportal1=portal();
tstportal1.xpos=2;
tstportal1.ypos=2;
tstportal1.zpos=0;
tstportal1.targetx=12;
tstportal1.targety=34;
tstportal1.targetz=0;

# tstportal2
tstportal2=portal();
tstportal2.xpos=12;
tstportal2.ypos=33;
tstportal2.zpos=0;
tstportal2.targetx=2;
tstportal2.targety=1;
tstportal2.targetz=0;

if debugmode:
	print("Done.");

###############
# Death zones #
###############

if debugmode:
	print("Initializing killzones...");

class killzone:
	xpos=0;
	ypos=0;
	zpos=0;
	message="";
	def __init__(self):
		killzonedict.append(self);

# testcliff
testcliff=killzone();
testcliff.xpos=12;
testcliff.ypos=37;
testcliff.zpos=0;
testcliff.message="You fall down the cliff and land on your head.";

if debugmode:
	print("Done.");

############
# Commands #
############

if debugmode:
	print("Initializing commands...");

# Movement
gocmd=["go"];
north=["north","n"];
south=["south","s"];
east=["east","e"];
west=["west","w"];
northeast=["northeast","ne"];
southeast=["southeast","se"];
northwest=["northwest","nw"];
southwest=["southwest","sw"];
up=["up","u"];
down=["down","d"];
enter=["enter","in","board","on"];
_exit=["exit","out","off"];
# Item interactions
invcmd=["inventory","i"];
pickup=["pickup","take"];
remove=["remove","drop"];
combine=["put"];
# Other general commands
look=["look","l","read","examine"];
dig=["dig"];
compinteract=["type"];
helpcmd=["help"];
quit=["quit"];
scorecmd=["score"];
# Cheat commands
cheatcmd=["cheats"];
noclipcmd=["noclip"];
givecmd=["give"];
setscorecmd=["setscore"];
takeallcmd=["takeeverything"];
spawncmd=["spawn"];
objdelcmd=["delete"];
godmodecmd=["god"];

if debugmode:
	print("Done.");

# Post-init variables
inventory=[lamp];
currentroom=barren_moor;
skipinput=False;

# Initialize treasures
for iteml in itemdict:
	if iteml.treasure:
		maxscore+=10;

#############
# Functions #
#############

if debugmode:
	print("Initializing game functions...");

# Draw location
def drawLocation(inclDesc=False):
	if currentroom.dark and lamp not in inventory and lamp not in currentroom.items:
		print("It is pitch dark.");
	else:
		if debugmode:
			print(currentroom.name+" ("+str(currentroom)+")");
		else:
			print(currentroom.name);
		if (not currentroom.visited) or (bool(inclDesc)):
			print(currentroom.desc);
		for iteml in currentroom.items:
			if (not iteml.silent) and iteml.spec_gndphrase==None and iteml.spec_gndtitle==None:
				print("There is "+iteml.name+" here.")
			elif (not iteml.silent) and iteml.spec_gndphrase!=None:
				print(iteml.spec_gndphrase);
			elif (not iteml.silent) and iteml.spec_gndtitle!=None:
				print("There is "+iteml.spec_gndtitle+" here.");
		for vehl in currentroom.vehicles:
			print("There is "+vehl.name+" here.");
	if curvehicle:
		print("You are operating "+curvehicle.name+".");
	if debugmode:
		print(x,y,z);
		print("roomdiggables:",currentroom.diggables);
		print("roomobjects:",currentroom.items);
	currentroom.visited=True;

# Set location
def setLoc(xpos,ypos,zpos):
	croom=currentroom;
	for rooml in roomdict:
		if xpos==rooml.xpos and ypos==rooml.ypos and zpos==rooml.zpos:
			croom=rooml;
			break;
	else:
		croom=null_room;
	return croom;

# Portal checking
def portalchk(xpos,ypos,zpos):
	for portalx in portaldict:
		if xpos==portalx.xpos and ypos==portalx.ypos and zpos==portalx.zpos:
			return portalx.targetx,portalx.targety,portalx.targetz;
	else:
		return xpos,ypos,zpos;

# Score
def scoref():
	print("You have scored "+str(score)+" out of a possible "+str(maxscore)+" points.");
	if score>=maxscore:
		print("\n\nCongratulations. You have won.");

# Death
def killplayer(message=None):
	if message:
		print(message);
	print("You are dead.");
	scoref();
	exit();

# Check killzones
def killchk(xpos,ypos,zpos):
	for killx in killzonedict:
		if xpos==killx.xpos and ypos==killx.ypos and zpos==killx.zpos and not godmode:
			killplayer(killx.message);
			break;

# Command interpreter
def cmdinterpret(command):
	command=str(command).lower();
	cmds="";
	cmdl=[];
	for cmdc in command:
		if cmdc==" " or cmdc=="\n" or cmdc=="\t":
			cmdl.append(cmds);
			cmds="";
		else:
			cmds=cmds+cmdc;	   
	cmd=cmdl[0];
	args=cmdl[1:];
	return cmd,args;

# Movement
def chkmove(_direction):
	if _direction not in currentroom.openwalls and _direction not in currentroom.lockwalls:
		print("You can't go that way.");
		return False;
	elif _direction in currentroom.lockwalls and key not in inventory:
		print("You don't have a key that can open this door.");
		return False;
	else:
		return True;

if debugmode:
	print("Done.");

if debugmode:
	print("Initialization completed.");

print("");

#####################
# Main game handler #
#####################

drawLocation();
while True:
	### Checks done each loop ###
	if (not currentroom.dark) or (lamp in inventory):
		nummoves=0;
	nummoves+=1;
	totalweight=0;
	for iteml in inventory:
		totalweight+=iteml.weight;
	if totalweight>100:
		noitems=True;
	else:
		noitems=False;
	
	### Read and interpret commands ###
	if not skipinput:
		cmdin=str(input(">"))+"\n";
		cmd,args=cmdinterpret(cmdin);
	else:
		skipinput=False;
		pass;
	
	### Movement commands ###
	
	# Cardinal directions
	if cmd in north:
		if chkmove("north") or noclip:
			y+=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in south:
		if chkmove("south") or noclip:
			y-=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in east:
		if chkmove("east") or noclip:
			x+=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in west:
		if chkmove("west") or noclip:
			x-=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	
	# Secondary directions
	elif cmd in northeast:
		if chkmove("northeast") or noclip:
			y+=1;
			x+=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in northwest:
		if chkmove("northwest") or noclip:
			y+=1;
			x-=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in southeast:
		if chkmove("southeast") or noclip:
			y-=1;
			x+=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in southwest:
		if chkmove("southwest") or noclip:
			y-=1;
			x-=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	
	# Vertical directions
	elif cmd in up:
		if chkmove("up") or noclip:
			z+=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in down:
		if chkmove("down") or noclip:
			z-=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	
	# Go
	elif cmd in gocmd:
		# No argument given
		if len(args)<1:
			print("I don't understand where you want me to go.");
			continue;
		
		cmd=args[0];
		args=[];
		skipinput=True;
		continue;
		
	### Item and inventory interaction commands ###
	
	# Take
	elif cmd in pickup:
		if len(args)<1:
			print("You must supply an object.");
			continue;
		if args[0]!="all":
			for il,iteml in enumerate(currentroom.items):
				if args[0] in iteml.cmdaliases and (iteml.takeable or takeeverything):
					if noitems:
						print("Your load would be too heavy.");
						break;
					else:
						currentroom.items.pop(il);
						inventory.append(iteml);
						print("Taken.");
						break;
				elif args[0] in iteml.cmdaliases and iteml.takeable==False:
					print("You cannot take that.");
					break;
			else:
				print("I do not see that here.");
		elif args[0]=="all":
			itemf=False;
			il=0;
			for iteml in currentroom.items[:]:
				if iteml.takeable or takeeverything:
					itemf=True;
					itemname=iteml.name[0].upper()+iteml.name[1:];
					if noitems:
						print(itemname+": Your load would be too heavy.");
					else:
						inventory.append(iteml);
						if debugmode:
							print("Added 1 "+iteml.name+" to inventory.");
						currentroom.items.remove(iteml);
						if debugmode:
							print("Removed 1 of "+iteml.name+" from room.");
						print(itemname+": Taken.")
				il+=1;
				if debugmode:
					print("Completed iteration "+str(il));
			if not itemf:
				print("Nothing to take.");
		else:
			print("I don't know what that is.");
	
	# Drop
	elif cmd in remove:
		if len(args)<1:
			print("You must supply an object.");
			continue;
		for il,iteml in enumerate(inventory):
			if args[0] in iteml.cmdaliases:
				inventory.pop(il);
				currentroom.items.append(iteml);
				print("Done.");
				break;
		else:
			print("You don't have that.");
	
	# Put
	elif cmd in combine:
		itemi=None;
		itemii=None;
		if len(args)<1:
			print("You must supply an object.");
		elif len(args)<3:
			print("You must supply an indirect object.");
		else:
			for il,iteml in enumerate(inventory):
				if args[0] in iteml.cmdaliases:
					itemi=iteml;
					ils=il;
					break;
			else:
				print("You don't have that.");
				continue;
			for ilx,itemlx in enumerate(inventory):
				if args[2] in iteml.cmdaliases:
					itemii=iteml;
					break;
			else:
				for ix,itemx in enumerate(currentroom.items):
					if args[2] in itemx.cmdaliases:
						itemii=itemx;
						break;
				else:
					print("That indirect object is not here.");
					continue;
			
			if itemii.treasuredrop:
				print("You hear it slide down the chute and into the distance.")
				inventory.pop(il);
				if itemi.treasure:
					if score<maxscore:
						score+=10;
					scoref();
	
	# Inventory
	elif cmd in invcmd:
		print("You currently have: ");
		if len(inventory)>0:
			for iteml in inventory:
				if iteml.spec_invtitle!=None:
					iteminvtitle=iteml.spec_invtitle[0].upper()+iteml.spec_invtitle[1:];
					if debugmode:
						print(iteminvtitle+" ("+str(iteml)+")");
					else:
						print(iteminvtitle);
					del iteminvtitle;
				else:
					itemname=iteml.name[0].upper()+iteml.name[1:];
					if debugmode:
						print(itemname+" ("+str(iteml)+")");
					else:
						print(itemname);
					del itemname;
		
	### General commands ###
	
	# Look
	elif cmd in look:
		if len(args)>0:
			for iteml in inventory+currentroom.items:
				if args[0] in iteml.cmdaliases:
					if iteml.spec_lookaction!=None:
						iteml.spec_lookaction(x,y,z);
						break;
					elif iteml.desc!=None and iteml.spec_lookaction==None:
						print(iteml.desc);
						break;
					else:
						print("I see nothing special about that.");
						break;
			else:
				print("I don't see that here.");
		else:
			drawLocation(inclDesc=True);
	
	# Dig
	elif cmd in dig:
		if shovel in inventory:
			for il,diggable in enumerate(currentroom.diggables):
				currentroom.items.append(diggable);
				currentroom.diggables.pop(il);
				print("I think you found something.");
				break;
			else:
				print("Digging here reveals nothing.");
		else:
			print("You have nothing with which to dig.");
	
	# Type
	elif cmd in compinteract:
		for compl in compdict:
			if compl.assoc in currentroom.items:
				compCmdProcessor(compl,False);
			elif compl.assoc in inventory and compl.portable:
				compCmdProcessor(compl,True);
			else:
				print("There is nothing here on which you could type.");
	
	# Score
	elif cmd in scorecmd:
		scoref();
		
	# Cheats on/off
	elif cmd in cheatcmd:
		if not debugmode:
			print("I don't understand that.");
			continue;
		else:
			if not cheatmode:
				cheatmode=True;
				print("cheats ON");
			elif cheatmode:
				cheatmode=False;
				print("cheats OFF");
	
	# Quit
	elif cmd in quit:
		scoref();
		exit();
	
	### Cheat commands ###
	
	# Noclip
	elif cmd in noclipcmd:
		if not debugmode or not cheatmode:
			print("I don't understand that.");
			continue;
		else:
			if not noclip:
				noclip=True;
				print("noclip ON");
			elif noclip:
				noclip=False;
				print("noclip OFF");
	
	# Give
	elif cmd in givecmd:
		if not debugmode or not cheatmode:
			print("I don't understand that.");
			continue;
		else:
			if len(args)<1:
				print("You must supply an object.");
				continue;
			for iteml in itemdict:
				if args[0] in iteml.cmdaliases:
					inventory.append(iteml);
					print("Done.");
					break;
			else:
				print("I don't know what that is.");
	
	# Set score
	elif cmd in setscorecmd:
		if not debugmode or not cheatmode:
			print("I don't understand that.");
			continue;
		else:
			if len(args)<1:
				print("You must supply a new score.");
				continue;
			score=int(args[0]);
			print("Done.");
	
	# Enable/disable non-takeables
	elif cmd in takeallcmd:
		if not debugmode or not cheatmode:
			print("I don't understand that.");
			continue;
		else:
			if not takeeverything:
				takeeverything=True;
				print("takeeverything ON");
			elif takeeverything:
				takeeverything=False;
				print("takeeverything OFF");
	
	# Spawn object
	elif cmd in spawncmd:
		if not debugmode or not cheatmode:
			print("I don't understand that.");
			continue;
		else:
			if len(args)<1:
				print("You must supply an object.");
				continue;
			
			for iteml in itemdict:
				if args[0] in iteml.cmdaliases:
					currentroom.items.append(iteml);
					print("Done.");
					break;
			else:
				print("I don't know what that is.");
				continue;
	
	# Delete object
	elif cmd in objdelcmd:
		if not debugmode or not cheatmode:
			print("I don't understand that.");
			continue;
		else:
			if len(args)<1:
				print("You must supply an object.");
				continue;
			
			for iteml in itemdict:
				if args[0] in iteml.cmdaliases and iteml in currentroom.items:
					currentroom.items.remove(iteml);
					print("Done.");
					break;
			else:
				print("I don't see that here.");
	
	# God mode
	elif cmd in godmodecmd:
		if not debugmode or not cheatmode:
			print("I don't understand that.");
			continue;
		else:
			if not godmode:
				godmode=True;
				print("god ON");
			elif godmode:
				godmode=False;
				print("god OFF");
				killchk(x,y,z);
	
	### Help ###
	elif cmd in helpcmd:
		if debugmode:
			print("# (DEBUG MODE)");
		print("# AVAILABLE COMMANDS:");
		print("# Movement: n s e w u d ne se nw sw in out");
		print("# Inventory: take drop put inventory i");
		print("# General: look l dig type score quit");
		if debugmode:
			print("# Cheats: cheats noclip god give setscore takeeverything spawn delete");
	
	### Command not found ###
	
	# Empty command
	elif cmd=="":
		continue;
	
	# Command not found
	else:
		print("I don't understand that.");