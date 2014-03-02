### Libraries ###
import random;
import sys;
# Import any additional needed libraries here #

# NO MODIFICATION ZONE (DO NOT MODIFY ANYHTING UP UNTIL "END NO MODIFICATION ZONE")
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
# END NO MODIFICATION ZONE

# Position (Change to the player's XYZ starting position)
x=0;
y=0;
z=0;

# NO MODIFICATION ZONE (After this one, these will always be abbreviated as "NMZ")
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
# END NO MODIFICATION ZONE

# Environment-affecting item-spec variables
### Define them here ###

# NMZ
if debugmode:
	print("Done.");

###########################
# Initialize dictionaries #
###########################

if debugmode:
	print("Initializing global dictionaries...");

### Dictionaries ###
### REQUIRED FOR FUNCTIONALITY (MODIFY AT YOUR OWN RISK!) ###
# Rooms
global roomdict;
roomdict=[];
# Items
global itemdict;
itemdict=[];
# Items that can be used to dig using the "dig" command
global diggingitems;
diggingitems=[];
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
# END NMZ

### Define any additional dictionaries here ###

# NMZ
if debugmode:
	print("Done.");

#########
# Items #
#########

if debugmode:
	print("Initializing items...");

# END NMZ
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
	### Define any additional properties for items under the appropriate header ###
	# NMZ
	def __init__(self):
		itemdict.append(self);
	# END NMZ

# lamp (REQUIRED FOR FUNCTIONALITY)
lamp=item();
lamp.name="a lamp";
lamp.cmdaliases=["lamp"];
lamp.desc=None;
lamp.weight=4;
lamp.treasure=False;

# key (REQUIRED FOR FUNCTIONALITY)
key=item();
key.name="a key";
key.spec_gndtitle="a shiny brass key";
key.spec_invtitle="a brass key";
key.cmdaliases=["key"];
key.desc=None;
key.weight=0.2;
key.treasure=False;

### Define additional items here ###
# If your item is used for digging add this line after the declaration:
#	diggingitems.append(<your item name here>);
# If your item is used for breaking things add this line after the declaration:
#	breakingitems.append(<your item name here);

# NMZ
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

# END NMZ
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
	### Define any additional properties for vehicles under the appropriate header ###
	# NMZ
	def __init__(self):
		vehicledict.append(self);
	# END NMZ

### Define vehicles here ###
# Remember to adhere to the Vehicle Class System when designating vehicle classes (see above) #

# NMZ
if debugmode:
	print("Done.");

#############
# Computers #
#############

if debugmode:
	print("Initializing computers...");

# END NMZ
class cfile:
	name="";
	ext="";
	canopen=True;
	datemod="";
	timemod="";
	data="";
	### Define any additional properties for files here (Remember to add them to the __init__ method) ###
	def __init__(self,namel,extl,canopenl,datemodl,timemodl,datal): # Remember to add any additional properties to the parameters and content of this method
		self.name=namel;
		self.ext=extl;
		self.canopen=canopenl;
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
	### Define any additional properties of computer objects under the appropriate header ###
	# NMZ
	def __init__(self):
		compdict.append(self);
	# END NMZ

### Define computers here ###

# NMZ
# REQUIRED FOR FUNCTIONALITY #
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
# END NMZ

# REQUIRED FOR FUNCTIONALITY #
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
						if comp.assoc.connectedUSB:
							currentroom.items.append(printedpage(filel.data));
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

# NMZ
if debugmode:
	print("Done.");

#########
# Rooms #
#########

# Regular max desc line length = 62 chars

if debugmode:
	print("Initializing rooms...");

walls_all=["north","south","east","west","up","down","northeast","northwest","southeast","southwest"];
# END NMZ

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
	# NMZ
	def __init__(self):
		roomdict.append(self);
	def openwall(self,direction):
		self.openwalls.append(direction);
	def lockwall(self,direction):
		self.lockwalls.append(direction);
	def closewall(self,direction):
		self.openwalls.remove(direction);
		self.lockwalls.remove(direction);
	# END NMZ
	### Define any additional properties of rooms under the appropriate heading ###

# Null room (REQUIRED FOR FUNCTIONALITY)
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

### Define additional rooms here ###

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

### Define portals here (Recommended: For each area bridged by portals, make 2 linked portals, unless not being able to get back is a deliberate part of the game) ###

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

### Define killzones here (Try to make the death messages informative) ###

if debugmode:
	print("Done.");

############
# Commands #
############

if debugmode:
	print("Initializing commands...");

### Stock commands (REQUIRED FOR FUNCTIONALITY) ###
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
### Define additional command aliases here (Remember to implement them down below in the main handler) ###

if debugmode:
	print("Done.");

# Post-init variables
inventory.append(lamp);
# currentroom=<the name of your starting room here> (It must match up with your starting XYZ coordinates!) (Remember to remove this comment text and uncomment this line);
skipinput=False;

# NMZ
# Initialize treasures
for iteml in itemdict:
	if iteml.treasure:
		maxscore+=10;
# END NMZ

#############
# Functions #
#############

if debugmode:
	print("Initializing game functions...");

### Stock functions (REQUIRED FOR FUNCTIONALITY) ###
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

### Define additional functions here ###

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
	if nummoves>4:
		killplayer("You trip over a grue and fall into a pit and break every bone in your body.")
	totalweight=0;
	for iteml in inventory:
		totalweight+=iteml.weight;
	if totalweight>100:
		noitems=True;
	else:
		noitems=False;
	# Define checks or operations to be executed each loop here #
	
	### Read and interpret commands ###
	if not skipinput:
		cmdin=str(input(">"))+"\n";
		cmd,args=cmdinterpret(cmdin);
	else:
		skipinput=False;
		pass;
	
	### Stock commands (REQUIRED FOR FUNCTIONALITY) ###
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
		itemx=None;
		for iteml in inventory:
			if iteml in diggingitems:
				itemx=iteml;
				break;
		else:
			itemx=None;
		if itemx:
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
	
	### Define additional commands here (Remember to define their aliases first) ###
	
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
	
	### Define additional cheats here ###
	# Remember to add checking for debugmode AND cheatmode #
	
	### Help ###
	# If you define any additional commands, add them to the help screen #
	elif cmd in helpcmd:
		if debugmode:
			print("# (DEBUG MODE)");
		print("# AVAILABLE COMMANDS:");
		print("# Movement: n s e w u d ne se nw sw in out");
		print("# Inventory: take drop put inventory i");
		print("# General: look l dig type score quit");
		if debugmode:
			print("# Cheats: cheats noclip god give setscore takeeverything spawn delete");
	
	### Define additional commands here (Remember to define their aliases first) ###
	
	# REQUIRED FOR FUNCTIONALITY #
	# DO NOT CHANGE #
	### Command not found ###
	
	# Empty command
	elif cmd=="":
		continue;
	
	# Command not found
	else:
		print("I don't understand that.");