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
inventory=[];
currentroom=None;
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

# Environment-affecting item-spec variables
printer_hasPower=False;

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
# Items that can be used to break stuff using the "break" command
global breakingitems;
breakingitems=[];
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
	tethered=False;
	# Messages
	tethered_dropmsg=None;
	spec_takemsg=None;
	spec_putmsg=None;
	treasure_dropmsg=None;
	# Special actions
	spec_loopaction=None;
	spec_lookaction=None;
	spec_takeaction=None;
	spec_putaction=None;
	spec_breakaction=None;
	def __init__(self):
		itemdict.append(self);

# lamp
lamp=item();
lamp.name="a lamp";
lamp.cmdaliases=["lamp"];
lamp.desc=None;
lamp.weight=4;
lamp.treasure=False;

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
dropchute.name="a trophy case";
dropchute.cmdaliases=["case"];
dropchute.desc=None;
dropchute.weight=0;
dropchute.takeable=False;
dropchute.silent=True;
dropchute.treasuredrop=True;
dropchute.treasure_dropmsg="You put it into the case.";

# trophy
trophy=item();
trophy.name="a trophy";
trophy.cmdaliases=["trophy"];
trophy.desc="It is a shiny gold trophy.";
trophy.weight=8;
trophy.treasure=True;

# vendor_dummy
vendor_dummy=item();
vendor_dummy.name="some vending machines";
vendor_dummy.spec_gndphrase="There are some vending machines here.";
vendor_dummy.cmdaliases=["machines"];
vendor_dummy.desc="""\
The machines do not appear to be functional. Some
are tipped over on their sides, as though someone
had used them as blockades."""
vendor_dummy.weight=400;
vendor_dummy.takeable=False;

# hammer
hammer=item();
hammer.name="a sledgehammer";
hammer.cmdaliases=["hammer","sledgehammer"];
hammer.desc=None;
hammer.weight=9;
breakingitems.append(hammer);

# powercord
powercord=item();
powercord.name="the wall end of a power cord";
powercord.spec_gndtitle="a power cord on the ground";
powercord.cmdaliases=["cord","power"];
powercord.desc=None;
powercord.weight=1;
powercord.tethered=True;
powercord.tethered_dropmsg="As you leave, you drop the power cord by the printer.";

# usbcable
usbcable=item();
usbcable.name="the computer end of a USB cable";
usbcable.spec_gndtitle="a USB cable on the ground";
usbcable.cmdaliases=["usb","cable"];
usbcable.desc=None;
usbcable.weight=1;
usbcable.tethered=True;
usbcable.tethered_dropmsg="You unplug the USB cable and set it by the printer.";

# printer
printer=item();
printer.name="a printer";
printer.cmdaliases=["printer"];
printer.desc="The printer has a power cord and a USB\ncable attached to it.";
printer.weight=200;
printer.takeable=False;

# printedpage
class printedpage(item):
	def __init__(self,pagetitle,pagecontent):
		self.name="a printed page ({0})".format(pagetitle);
		self.desc="The page says:\n"+pagecontent;
		self.cmdaliases=[pagetitle];
		self.weight=0.1;
		itemdict.append(self);

# walloutlet_dummy
walloutlet_dummy=item();
walloutlet_dummy.name="an outlet";
walloutlet_dummy.cmdaliases=["outlet"];
walloutlet_dummy.desc="It is a standard 110 volt outlet with 2 ports.";
walloutlet_dummy.weight=0;
walloutlet_dummy.takeable=False;
walloutlet_dummy.silent=True;
def walloutlet_dummy_spec_putaction(other):
	if other==powercord:
		printer_hasPower=True;
		print("Done.");
	else:
		print("What exactly are you trying to do anyway?");
	inventory.remove(other);
walloutlet_dummy.spec_putaction=walloutlet_dummy_spec_putaction;
del walloutlet_dummy_spec_putaction;

# laptop
laptop=item();
laptop.name="a laptop";
laptop.spec_gndphrase="There is a laptop resting on the ground nearby.";
laptop.cmdaliases=["laptop"];
laptop.desc="You turn the laptop over. A sticker on the back reads \"066328\".\n\
It still appears to work.\n\n(Use the \"type\" command to use computers)";
laptop.weight=4;
laptop.connectedUSB=False;
def laptop_spec_loopaction():
	if not (usbcable in inventory):
		laptop.connectedUSB=False;
laptop.spec_loopaction=laptop_spec_loopaction;
del laptop_spec_loopaction;

def laptop_spec_putaction(other):
	if other==usbcable:
		laptop.connectedUSB=True;
		print("Done.");
laptop.spec_putaction=laptop_spec_putaction;
del laptop_spec_putaction;

# boards
boards=item();
boards.name="some boards";
boards.spec_gndphrase="There are some boards nailed to the floor here.";
boards.cmdaliases=["boards","board"];
boards.desc="They are weakened and look like they could be broken.";
boards.weight=10;
def boards_spec_breakaction(other):
	if other==hammer:
		currentroom.items.remove(boards);
		currentroom.openwall("down");
		print("Done. Breaking the boards reveals a hole in the floor.\nA ladder leads down.");
	else:
		print("You can't use that to break these boards.");
boards.spec_breakaction=boards_spec_breakaction;
del boards_spec_breakaction;

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
	noarticle="";
	desc="";
	boardedphrase="";
	cmdaliases=[];
	desc=None;
	opentop=False;
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
bicycle.noarticle="bicycle";
bicycle.cmdaliases=["bicycle","bike"];
bicycle.boardedphrase="You are on the bicycle.";
bicycle.desc="It is a standard 10 speed bicycle.\n\n(Type \"in\" to board vehicles)";
bicycle.opentop=True;
bicycle.vclass=0;
bicycle.xpos=-1;
bicycle.ypos=8;
bicycle.zpos=-1;

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
	canprint=True;
	datemod="";
	timemod="";
	data="";
	def __init__(self,namel,extl,canopenl,canprintl,datemodl,timemodl,datal):
		self.name=namel;
		self.ext=extl;
		self.canopen=canopenl;
		self.canprint=canprintl;
		self.datemod=datemodl;
		self.timemod=timemodl;
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
comp_laptop.hostname="L066328-12";
comp_laptop.assoc=laptop;
comp_laptop.exitmsg="You close the laptop and step back.";
comp_laptop.exitmsg_inv="You close the laptop and stash it in your inventory.";
comp_laptop.portable=True;
comp_laptop.driveltr="D";
comp_laptop.drivelbl="OFFLINEDATA";
comp_laptop.driveser="49F3-AC3B";
comp_laptop.dirhierarchy={
	"day28.txt":cfile(
		namel="day28.txt",
		extl="txt",
		canopenl=True,
		canprintl=True,
		datemodl="03/30/2014",
		timemodl="08:18 PM",
		datal="\
Sunday, March 30, 2014, 8:14 PM\n\
It's been nearly a month since the invasion began.\n\
Some of us still manage to survive by hiding out in\n\
secret passages. However, most of us are still\n\
blockaded inside our rooms. Hopefully our hideout\n\
will hold up. If not, we can at least fight back.",
	),
	"hideout.txt":cfile(
		namel="hideout.txt",
		extl="txt",
		canopenl=True,
		canprintl=True,
		datemodl="03/14/2014",
		timemodl="02:14 PM",
		datal="\
Friday, March 14, 2014, 2:11 PM\n\
Some of the guys in charge of fortifying room 28 told\n\
us that they built an underground hideout behind the\n\
podium. However, we don't want to go over there, for\n\
fear of compromising our own shelter.\n\
Also, I just realized that I\'m not going to get my\n\
prizes for selling all those cookies."
	),
	"key.txt":cfile(
		namel="key.txt",
		extl="txt",
		canopenl=False,
		canprintl=True,
		datemodl="03/24/2014",
		timemodl="03:36 PM",
		datal="\
Monday, March 24, 2014, 3:34 PM\n\
The guys in room 27 told us they were keeping the key\n\
to some kind of secret escape hatch that the room 28\n\
team had discovered and locked down. Will go investigate\n\
when it becomes safe. Right now, it is not even close."
	),
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
	volInfo=["vol"];
	printFile=["print"];
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
			print("\n Directory of "+comp.driveltr+":\\\n");
			for fkey,filel in comp.dirhierarchy.items():
				formstr="{0}  {1}    {2} {3}";
				print(formstr.format(filel.datemod,filel.timemod,str(len(filel.data)),filel.name));
				numfiles+=1;
				numbytes+=len(filel.data);
			print("               {0} File(s)    {1} bytes".format(numfiles,numbytes));
		
		elif ccmd in fileData:
			if len(cargs)<1:
				print("Bad command or file name");
			else:
				for fkey,filel in comp.dirhierarchy.items():
					if filel.name==cargs[0]:
						if filel.canopen:
							print(filel.data);
							break;
						elif (not filel.canopen) and filel.canprint:
							print("Access allowed only for printing");
							break;
						else:
							print("Access denied");
							break;
				else:
					print("Bad command or file name");
		
		elif ccmd in volInfo:
			if comp.drivelbl=="":
				print(" Volume in drive "+comp.driveltr+" has no label.");
			else:
				print(" Volume in drive "+comp.driveltr+" is "+comp.drivelbl);
			print(" Volume serial number is "+comp.driveser+"\n");
		
		elif ccmd in printFile:
			if len(cargs)<1:
				print("Bad command or file name");
			else:
				for fkey,filel in comp.dirhierarchy.items():
					if filel.name==cargs[0]:
						if not filel.canprint:
							print("No print access for this file");
							break;
						elif comp.assoc.connectedUSB:
							currentroom.items.append(printedpage(filel.data));
							print("Printed 1 Page(s)");
							print("Notice: In the game, refer to printed pages by their filenames");
							break;
						else:
							print("No print device found");
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

### Entering the building ###

# Building entrance
building_entrance=room();
building_entrance.name="Building entrance";
building_entrance.desc="""\
You are in front of a building. The entrance is to
the north. The doors appear to have been forced
open."""
building_entrance.xpos=0;
building_entrance.ypos=0;
building_entrance.zpos=0;
building_entrance.openwalls=["north"];
building_entrance.dark=False;
building_entrance.items=[];

### First floor ###

# Lobby
lobby=room();
lobby.name="Lobby";
lobby.desc="""\
You are in the lobby of a building. Nobody else
appears to be inside. A hallway leads east from
here, there is an improvised barrier to the north,
and the exit is to the south. It is dark inside."""
lobby.xpos=0;
lobby.ypos=1;
lobby.zpos=0;
lobby.openwalls=["east","south"];
lobby.dark=True;
lobby.items=[];

# E/W hallway with stairwell
e_w_hall_with_stairwell=room();
e_w_hall_with_stairwell.name="E/W hallway with stairwell";
e_w_hall_with_stairwell.desc="""\
You are in an east/west hallway. However, an
improvised barrier has been built to the east.
A stairwell leads down from here."""
e_w_hall_with_stairwell.xpos=1;
e_w_hall_with_stairwell.ypos=1;
e_w_hall_with_stairwell.zpos=0;
e_w_hall_with_stairwell.openwalls=["west","down"];
e_w_hall_with_stairwell.dark=True;
lobby.items=[];

### Ground floor ###

# Atrium
atrium=room();
atrium.name="Atrium";
atrium.desc="""\
You are on the lower floor of a building, in
a large, open area. To the east and west are
hallways. However, the one to the east is
protected by an improvised barrier. There
is an exit to the northeast, but it has
been heavily boarded up. Stairs lead up
from here."""
atrium.xpos=1;
atrium.ypos=1;
atrium.zpos=-1;
atrium.openwalls=["west","up"];
atrium.dark=True;
atrium.items=[];

# North wing hallway (Rooms 20-32) #

# Vending machines (Room 20S)
vending_machines=room();
vending_machines.name="Vending machines";
vending_machines.desc="""\
You are at the south end of a north/south
hallway. To the east is the atrium, and to 
the west is a door."""
vending_machines.xpos=0;
vending_machines.ypos=1;
vending_machines.zpos=-1;
vending_machines.openwalls=["east","west","north"];
vending_machines.dark=True;
vending_machines.items=[vendor_dummy];

# N/S hallway (Rooms 20N/25)
n_s_hallway_20_25=room();
n_s_hallway_20_25.name="N/S hallway";
n_s_hallway_20_25.desc="""\
You are in a north/south hallway. There
are doors to the east and west."""
n_s_hallway_20_25.xpos=0;
n_s_hallway_20_25.ypos=2;
n_s_hallway_20_25.zpos=-1;
n_s_hallway_20_25.openwalls=["north","south","east","west"];
n_s_hallway_20_25.dark=True;
n_s_hallway_20_25.items=[];

# N/S hallway (Rooms 26/27)
n_s_hallway_26_27=room();
n_s_hallway_26_27.name="N/S hallway";
n_s_hallway_26_27.desc="""\
You are in a north/south hallway. There
are doors to the east and west."""
n_s_hallway_26_27.xpos=0;
n_s_hallway_26_27.ypos=3;
n_s_hallway_26_27.zpos=-1;
n_s_hallway_26_27.openwalls=["north","south","east","west"];
n_s_hallway_26_27.dark=True;
n_s_hallway_26_27.items=[];

# N/S hallway (Rooms 28/29)
n_s_hallway_28_29=room();
n_s_hallway_28_29.name="N/S hallway";
n_s_hallway_28_29.desc="""\
You are in a north/south hallway. There
are doors to the east and west."""
n_s_hallway_28_29.xpos=0;
n_s_hallway_28_29.ypos=4;
n_s_hallway_28_29.zpos=-1;
n_s_hallway_28_29.openwalls=["north","south","east","west"];
n_s_hallway_28_29.dark=True;
n_s_hallway_28_29.items=[];

# N/S/W junction (Stairs/Printer area)
n_s_w_junction_stairs_printer=room();
n_s_w_junction_stairs_printer.name="N/S hallway";
n_s_w_junction_stairs_printer.desc="""\
You are at a junction of 3 paths. One leads
to the west, another leads to the south, and
a door leads north into a room."""
n_s_w_junction_stairs_printer.xpos=0;
n_s_w_junction_stairs_printer.ypos=5;
n_s_w_junction_stairs_printer.zpos=-1;
n_s_w_junction_stairs_printer.openwalls=["north","south","west"];
n_s_w_junction_stairs_printer.dark=True;
n_s_w_junction_stairs_printer.items=[];

# Stairs area (Ground floor, north wing)
stairs_area_g_nwing=room();
stairs_area_g_nwing.name="Stairwell";
stairs_area_g_nwing.desc="""\
You are in a room surrounded wooden boards.
You guess that this room used to be made up
of glass, and that it had been boarded up.
You see the destroyed remnants of what you
assume were once stairs leading up to the
next floor. There is a door to the south.
To the east, there is a heavily boarded up
door."""
stairs_area_g_nwing.xpos=0;
stairs_area_g_nwing.ypos=6;
stairs_area_g_nwing.zpos=-1;
stairs_area_g_nwing.openwalls=["south"];
stairs_area_g_nwing.dark=True;
stairs_area_g_nwing.items=[];

# Printer area (Rooms 30,32)
printer_area=room();
printer_area.name="Printer area";
printer_area.desc="""\
You are in a small room at the end of the
hallway. In here there are some sofas, and
a large printer. There is a wall outlet nearby.
There are doors to the north and west, and the
hallway is to the east."""
printer_area.xpos=-1;
printer_area.ypos=5;
printer_area.zpos=-1;
printer_area.openwalls=["east","west","north"];
printer_area.dark=True;
printer_area.items=[printer,powercord,usbcable,walloutlet_dummy];

# Rooms 20-32 #

# Room 20 south end
room_20_southend=room();
room_20_southend.name="Room 20";
room_20_southend.desc="""\
You are at the south end of a large room.
It appears this room was used as a woodshop,
as there is woodworking equipment strewn
throughout the room. There is a door to the
east."""
room_20_southend.xpos=-1;
room_20_southend.ypos=1;
room_20_southend.zpos=-1;
room_20_southend.openwalls=["east","north"];
room_20_southend.dark=True;
room_20_southend.items=[hammer,laptop];

# Room 20 north end
room_20_northend=room();
room_20_northend.name="Room 20";
room_20_northend.desc="""\
You are at the north end of a large room.
It appears this room was used as a woodshop,
as there is woodworking equipment strewn
throughout the room. There is a door to the
east."""
room_20_northend.xpos=-1;
room_20_northend.ypos=2;
room_20_northend.zpos=-1;
room_20_northend.openwalls=["east","south"];
room_20_northend.dark=True;
room_20_northend.items=[];

# Room 25
room_25=room();
room_25.name="Room 25";
room_25.desc="""\
You are in a room with tiled floors. There
are tables and chairs strewn about, some
positioned in blockade formation."""
room_25.xpos=1;
room_25.ypos=2;
room_25.zpos=-1;
room_25.openwalls=["west"];
room_25.dark=True;
room_25.items=[];

# Room 26
room_26=room();
room_26.name="Room 26";
room_26.desc="""\
You are in an abandoned classroom. There
are tables and chairs strewn about, some
positioned in blockade formation."""
room_26.xpos=-1;
room_26.ypos=3;
room_26.zpos=-1;
room_26.openwalls=["east"];
room_26.dark=True;
room_26.items=[];

# Room 27
room_27=room();
room_27.name="Room 27";
room_27.desc="""\
You are in an abandoned classroom. There
are tables and chairs strewn about, some
positioned in blockade formation."""
room_27.xpos=1;
room_27.ypos=3;
room_27.zpos=-1;
room_27.openwalls=["west"];
room_27.dark=True;
room_27.items=[key];

# Room 28
room_28=room();
room_28.name="Room 28";
room_28.desc="""\
You are in an abandoned classroom. Unlike
the other rooms, there seems to be a bit
more order to the positioning of the
furniture, almost like a fortification."""
room_28.xpos=-1;
room_28.ypos=4;
room_28.zpos=-1;
room_28.openwalls=["east"];
room_28.dark=True;
room_28.items=[boards];

# Room 29
room_29=room();
room_29.name="Room 29";
room_29.desc="""\
You are in an abandoned classroom. There
are tables and chairs strewn about, some
positioned in blockade formation."""
room_29.xpos=1;
room_29.ypos=4;
room_29.zpos=-1;
room_29.openwalls=["west"];
room_29.dark=True;
room_29.items=[];

# Room 30
room_30=room();
room_30.name="Room 30";
room_30.desc="""\
You are in an abandoned classroom. There
are tables and chairs strewn about, some
positioned in blockade formation."""
room_30.xpos=-2;
room_30.ypos=5;
room_30.zpos=-1;
room_30.openwalls=["east"];
room_30.dark=True;
room_30.items=[];

# Room 32
room_32=room();
room_32.name="Room 32";
room_32.desc="""\
You are in a room that appears as though it
used to be an office. There is a desk positioned
on its side, as if to form a blockade against
something."""
room_32.xpos=-1;
room_32.ypos=6;
room_32.zpos=-1;
room_32.openwalls=["south"];
room_32.dark=True;
room_32.items=[];

### Underground passage ###
# N/S underground passage (Just under room 28)
n_s_passage_under28=room();
n_s_passage_under28.name="South end of N/S underground passage";
n_s_passage_under28.desc="""\
You are at the south end of a north/south underground
passage. A ladder leads up from here."""
n_s_passage_under28.xpos=-1;
n_s_passage_under28.ypos=4;
n_s_passage_under28.zpos=-2;
n_s_passage_under28.openwalls=["up","north"];
n_s_passage_under28.dark=True;
n_s_passage_under28.items=[];

# N/S underground passage (1/2 way)
n_s_passage_12way=room();
n_s_passage_12way.name="N/S underground passage";
n_s_passage_12way.desc="""\
You are in a north/south underground passage."""
n_s_passage_12way.xpos=-1;
n_s_passage_12way.ypos=5;
n_s_passage_12way.zpos=-2;
n_s_passage_12way.openwalls=["north","south"];
n_s_passage_12way.dark=True;
n_s_passage_12way.items=[];

# N/S underground passage (Under exit)
n_s_passage_underexit=room();
n_s_passage_underexit.name="North end of N/S underground passage";
n_s_passage_underexit.desc="""\
You are at the north end of a north/south underground
passage. A ladder leads up a manhole."""
n_s_passage_underexit.xpos=-1;
n_s_passage_underexit.ypos=8;
n_s_passage_underexit.zpos=-2;
n_s_passage_underexit.openwalls=["south"];
n_s_passage_underexit.lockwalls=["up"];
n_s_passage_underexit.dark=True;
n_s_passage_underexit.items=[];

### Exit ###
# Exit
exitroom=room();
exitroom.name="Field";
exitroom.desc="""\
You are on a large field. Very close by are many
buildings with boarded up entrances and windows.
There is an exposed manhole with a ladder leading
down, and a road leading northwest."""
exitroom.xpos=-1;
exitroom.ypos=8;
exitroom.zpos=-1;
exitroom.openwalls=["down","northwest"];
exitroom.vwalls_class0=["northwest"];
exitroom.dark=False;
exitroom.items=[];

# NW/SE road to exit
ne_sw_road=room();
ne_sw_road.name="NW/SE road";
ne_sw_road.desc="""\
You are on a northwest/southeast road. Up ahead,
you can see a small building in the distance."""
ne_sw_road.xpos=-2;
ne_sw_road.ypos=9;
ne_sw_road.zpos=-1;
ne_sw_road.openwalls=["northwest","southeast"];
ne_sw_road.vwalls_class0=["northwest","southeast"];
ne_sw_road.dark=False;
ne_sw_road.items=[];

# In front of the shack
in_front_of_final=room();
in_front_of_final.name="Building front";
in_front_of_final.desc="""\
You are at the northwest end of a northwest/
southeast road. In front of you is a small
fortified building. The entrance is to the
north."""
in_front_of_final.xpos=-3;
in_front_of_final.ypos=10;
in_front_of_final.zpos=-1;
in_front_of_final.openwalls=["north","southeast"];
in_front_of_final.vwalls_class0=["southeast"];
in_front_of_final.dark=False;
in_front_of_final.items=[];

# The Ending Shack
finalroom=room();
finalroom.name="Safe house";
finalroom.desc="""\
You are in a small fortified building. A sign
on the wall reads \"Congratulations! You have
won! Place the trophy in the trophy case to
complete the game.\""""
finalroom.xpos=-3;
finalroom.ypos=11;
finalroom.zpos=-1;
finalroom.openwalls=["south"];
finalroom.dark=False;
finalroom.items=[trophy,dropchute];

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
tstportal1.xpos=-1;
tstportal1.ypos=6;
tstportal1.zpos=-2;
tstportal1.targetx=-1;
tstportal1.targety=8;
tstportal1.targetz=-2;

# tstportal2
tstportal2=portal();
tstportal2.xpos=-1;
tstportal2.ypos=7;
tstportal2.zpos=-2;
tstportal2.targetx=-1;
tstportal2.targety=5;
tstportal2.targetz=-2;

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
breakcmd=["break"];
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
inventory.append(lamp);
currentroom=building_entrance;
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
		for vehl in vehicledict:
			if vehl.xpos==x and vehl.ypos==y and vehl.zpos==z and vehl!=curvehicle:
				print("There is "+vehl.name+" here.");
		
	if curvehicle:
		print(curvehicle.boardedphrase);
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

# Move vehicle
def moveVehicle(xpos,ypos,zpos):
	if curvehicle:
		curvehicle.xpos=xpos;
		curvehicle.ypos=ypos;
		curvehicle.zpos=zpos;

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

# Check whether the player can actually move in that direction
def chkmove(_direction):
	if _direction not in currentroom.openwalls and _direction not in currentroom.lockwalls:
		print("You can't go that way.");
		return False;
	elif _direction in currentroom.lockwalls and key not in inventory:
		print("You don't have a key that can open this door.");
		return False;
	else:
		return True;

# Remove tethered items from the player's inventory before leaving a room
def tethereditems():
	itemf=False;
	il=0;
	for iteml in inventory[:]:
		if iteml.tethered:
			itemf=True;
			inventory.remove(iteml);
			currentroom.items.append(iteml);
			print(iteml.tethered_dropmsg);
			il+=1;

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
	for iteml in inventory:
		if iteml.spec_loopaction!=None:
			iteml.spec_loopaction();
	
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
			tethereditems();
			y+=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			moveVehicle(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in south:
		if chkmove("south") or noclip:
			tethereditems();
			y-=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			moveVehicle(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in east:
		if chkmove("east") or noclip:
			tethereditems();
			x+=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			moveVehicle(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in west:
		if chkmove("west") or noclip:
			tethereditems();
			x-=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			moveVehicle(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	
	# Secondary directions
	elif cmd in northeast:
		if chkmove("northeast") or noclip:
			tethereditems();
			y+=1;
			x+=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			moveVehicle(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in northwest:
		if chkmove("northwest") or noclip:
			tethereditems();
			y+=1;
			x-=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			moveVehicle(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in southeast:
		if chkmove("southeast") or noclip:
			tethereditems();
			y-=1;
			x+=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			moveVehicle(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in southwest:
		if chkmove("southwest") or noclip:
			tethereditems();
			y-=1;
			x-=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			moveVehicle(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	
	# Vertical directions
	elif cmd in up:
		if chkmove("up") or noclip:
			tethereditems();
			z+=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			moveVehicle(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	elif cmd in down:
		if chkmove("down") or noclip:
			tethereditems();
			z-=1;
			killchk(x,y,z);
			x,y,z=portalchk(x,y,z);
			moveVehicle(x,y,z);
			currentroom=setLoc(x,y,z);
			drawLocation();
	
	# Boarding vehicles
	elif cmd in enter:
		for vehl in vehicledict:
			if vehl.xpos==x and vehl.ypos==y and vehl.zpos==z:
				curvehicle=vehl;
				if curvehicle.opentop:
					print("You hop on the "+curvehicle.noarticle+".");
				else:
					print("You hop off the "+curvehicle.noarticle+".");
				break;
		else:
			print("You can't go that way.");
	elif cmd in _exit:
		if curvehicle:
			if curvehicle.opentop:
				print("You hop off the "+curvehicle.noarticle+".");
			else:
				print("You get out of the "+curvehicle.noarticle+".")
			curvehicle=None;
			
		else:
			print("You can't go that way.")
	
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
					for ixx,itemxx in enumerate(inventory):
						if args[2] in itemxx.cmdaliases:
							itemii=itemxx;
							break;
					else:
						print("That indirect object is not here.");
						continue;
			
			if itemii.treasuredrop:
				print(itemii.treasure_dropmsg);
				inventory.pop(il);
				if itemi.treasure:
					if score<maxscore:
						score+=10;
					scoref();
			elif itemii.spec_putaction!=None:
				itemii.spec_putaction(itemi);
	
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
	
	# Break
	elif cmd in breakcmd:
		if len(args)<1:
			print("You must supply an object.");
			continue;
		else:
			brkitem=None;
			for itemx in breakingitems:
				if itemx in inventory:
					brkitem=itemx;
					break;
			else:
				print("You have nothing with which to break things.");
				continue;
			for iteml in currentroom.items:
				if args[0] in iteml.cmdaliases and iteml.spec_breakaction!=None:
					iteml.spec_breakaction(itemx);
					break;
			else:
				print("I don't see that here.");
	
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