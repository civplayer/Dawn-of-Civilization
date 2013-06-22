# Rhye's and Fall of Civilization - Barbarian units and cities

from CvPythonExtensions import *
import CvUtil
import PyHelpers        # LOQ
#import Popup
#import cPickle as pickle
import RFCUtils
import Consts as con

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ
utils = RFCUtils.RFCUtils()

### Constants ###

iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNative = con.iNative
iCeltia = con.iCeltia
iCarthage = con.iCarthage
pIndependent = gc.getPlayer(iIndependent)
pIndependent2 = gc.getPlayer(iIndependent2)
pNative = gc.getPlayer(iNative)
pCeltia = gc.getPlayer(iCeltia)
pCarthage = gc.getPlayer(iCarthage)
teamIndependent = gc.getTeam(pIndependent.getTeam())
teamIndependent2 = gc.getTeam(pIndependent2.getTeam())
teamNative = gc.getTeam(pNative.getTeam())
teamCeltia = gc.getTeam(pCeltia.getTeam())

iBarbarian = con.iBarbarian
pBarbarian = gc.getPlayer(iBarbarian)
teamBarbarian = gc.getTeam(pBarbarian.getTeam())
      

# city coordinates, spawn 1st turn and retries
# converted to years (3rd col.), last col. stays the same(turns) - edead
lUr = [77, 38, -3000, 0] #0
lJerusalem = [73, 38, -3000, 0] #0
lBabylon = [76, 40, -3000, 0] #0
lSusa = [79, 40, -3000, 0] #0
lTyre = [73, 40, -3000, 0] #0 / 2700BC #turn10
lKnossos = [69, 39, -2600, 0] #13
lHattusas = [73, 43, -2000, 0] #34
lSamarkand = [85, 47, -2000, 0] #34
lNineveh = [76, 42, -1800, 0] #42
lVaranasi = [92, 39, -2000, 0]
lIndraprastha = [90, 40, -2000, 0]
lGadir = [51, 40, -1100, 0] #70
lLepcis = [61, 37, -1100, 0] #70
lBeijing = [102, 47, -1000, 0]
lAnkara = [72, 44, -1000, 0]
lCarthage = [58, 39, -814, 0] #86
lGordion = [71, 43, -800, 0] #87
lPalermo = [60, 40, -760, 0] #94-5
lMilan = [59, 47, -760, 0] #94-5
lAugsburg = [60, 49, -760, 0] #94-5
lRusadir = [54, 38, -650, 0] #97
lLyon = [56, 47, -350, 0] #117
#lAxum = [72, 29, -300, 0] #121
lShenyang = [105, 49, -300, 0]
lBordeaux = [53, 48, -300, 0] #121
lThanjavur = [91, 31, -300, 0]
lThanjavur = [91, 31, -300, 0]
lMadras = [92, 33, -325, 0]
lCartagena = [54, 42, -230, 0] #125
lArtaxata = [77, 44, -190,0] #128
lDunhuang = [95, 47, -100, 0] #133 Orka
lKashgar = [89, 46, -75, 0] #133 Orka
lLutetia = [55, 50, -50, 0] #137
#lSeoul = [109, 46, -25, 0] #139
#lTikal = [22, 35, 60, 0] #145
lSanaa = [76, 30, 100, 0] #147
lPagan = [98, 36, 107, 0] #148
#lInverness = [52, 60, 400, 0] #167
#lEdinburgh = [52, 59, 400, 0] #167
#lChichenItza = [23, 37, 445, 0] #170
lBaku = [77, 45, 600, 0] #180
lLhasa = [96, 43, 633, 0] #184
#lAngkor = [102, 34, 802, 0] #201
lMarrakesh = [51, 37, 680, 0]
lTiwanaku = [30, 20, 700, 0]
lVienna = [63, 49, 800, 0]
lHamburg = [59, 53, 830, 0]
lLubeck = [60, 53, 830, 0]
lHanoi = [101, 37, 866, 0] #208
lTucume = [24, 26, 900, 0] #211
lChanChan = [25, 23, 900, 0]
lKiev = [69, 52, 900, 0] #211
lJelling = [59, 55, 980, 0] #219
lDublin = [49, 56, 990, 0] #220
lNidaros = [61, 62, 1000, 0] #221
lZimbabwe = [69, 15, 1000, 0] #221
lQuelimane = [71, 17, 1000, 0] #221
lUppsala = [63, 58, 1070, 0] #228
lMombasa = [71, 22, 1100, 0] #231
lKazan = [77, 55, 1200, 0] #241
lKongo = [62, 20, 1483, 0] #278

# do some research on dates here
tMinorStates = (
	(633, 1400, 96, 43, [con.iArcher, con.iSwordsman]),	# Tibet
	(-75, 1600, 89, 46, [con.iHorseArcher]),		# Kashgar
	(-75, 1600, 85, 47, [con.iHorseArcher]),		# Samarkand
	(-300, 600, 91, 31, [con.iArcher, con.iSwordsman, con.iWarElephant]), # Chola
	(-300, 600, 92, 33, [con.iArcher, con.iSwordsman, con.iWarElephant]), # Chola
	(-300, 900, 105, 49, [con.iHorseArcher, con.iSwordsman]), # Manchu
	(1100, 1500, 60, 44, [con.iPikeman, con.iLongbowman]), # Rome late
	(0, 1100, 60, 44, [con.iSpearman, con.iArcher]), # Rome early
)



#handicap level modifier
iHandicapOld = (gc.getGame().getHandicapType() - 1)



class Barbs:

        def makeUnit(self, iUnit, iPlayer, tCoords, iNum, iForceAttack):
                'Makes iNum units for player iPlayer of the type iUnit at tCoords.'
                for i in range(iNum):
                        player = gc.getPlayer(iPlayer)
                        if (iForceAttack == 0):
                                player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
                        elif (iForceAttack == 1):
                                player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)                                  
                        elif (iForceAttack == 2):
                                player.initUnit(iUnit, tCoords[0], tCoords[1], UnitAITypes.UNITAI_ATTACK_SEA, DirectionTypes.DIRECTION_SOUTH)



        	
        def checkTurn(self, iGameTurn):
            
                #handicap level modifier
                iHandicap = (gc.getGame().getHandicapType() - 1)
		bGreatWall = (gc.getPlayer(con.iChina).isAlive() and gc.getPlayer(con.iChina).countNumBuildings(con.iGreatWall) > 0)
		
		# Leoreth: buff certain cities if independent / barbarian (imported from SoI)
		if iGameTurn % 20 == 10:
			for tMinorCity in tMinorStates:
				if iGameTurn > getTurnForYear(tMinorCity[0]) and iGameTurn < getTurnForYear(tMinorCity[1]):
					plot = gc.getMap().plot(tMinorCity[2], tMinorCity[3])
					iOwner = plot.getOwner()
					if plot.isCity() and plot.getNumUnits() < 4 and iOwner >= con.iNumPlayers:
						lUnitList = tMinorCity[4]
						iRand = gc.getGame().getSorenRandNum(len(lUnitList), 'random unit')
						iUnit = lUnitList[iRand]
						utils.makeUnit(iUnit, iOwner, (tMinorCity[2], tMinorCity[3]), 1)

                if (iGameTurn >= getTurnForYear(-3000) and iGameTurn <= getTurnForYear(-850)):
                        if (iHandicap >= 0):
				self.checkSpawn(iBarbarian, con.iWarrior, 1, (76, 46), (99, 53), self.spawnMinors, iGameTurn, 5, 0)
			
			self.checkSpawn(iBarbarian, con.iWolf, 1, (75, 54), (104, 64), self.spawnNatives, iGameTurn, 5, 2)
			self.checkSpawn(iBarbarian, con.iBear, 1, (75, 54), (104, 64), self.spawnNatives, iGameTurn, 5, 4)
			self.checkSpawn(iBarbarian, con.iLion, 1, (55, 10), (72, 29), self.spawnNatives, iGameTurn, 4, 1)
			self.checkSpawn(iBarbarian, con.iPanther, 1, (55, 10), (72, 29), self.spawnNatives, iGameTurn, 4, 3)

                        
                #celts
                if (iGameTurn >= getTurnForYear(-650) and iGameTurn <= getTurnForYear(-110)):
                        self.checkSpawn(iCeltia, con.iCelticGallicWarrior, 1, (49, 46), (65, 52), self.spawnMinors, iGameTurn, 7, 0)
                        if (iHandicap >= 0):
                                self.checkSpawn(iCeltia, con.iAxeman, 1, (49, 46), (65, 52), self.spawnMinors, iGameTurn, 9, 6, ["TXT_KEY_ADJECTIVE_GAUL"])

                #norse
                if (iGameTurn >= getTurnForYear(-650) and iGameTurn <= getTurnForYear(550)):
                        self.checkSpawn(iBarbarian, con.iGalley, 1, (50, 49), (61, 55), self.spawnPirates, iGameTurn, 20, 0, ["TXT_KEY_ADJECTIVE_NORSE"])
                        
                #mongolia
                if (iGameTurn >= getTurnForYear(-210) and iGameTurn < getTurnForYear(300)):
                        self.checkSpawn(iBarbarian, con.iHorseArcher, 2 + 2*iHandicap, (94, 48), (107, 54), self.spawnNomads, iGameTurn, 8, 0, ["TXT_KEY_ADJECTIVE_XIONGNU"])
                if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(900)):
			iNumUnits = 3 + iHandicap*2
			if bGreatWall: iNumUnits = 2
                        self.checkSpawn(iBarbarian, con.iHorseArcher, iNumUnits, (91, 50), (107, 54), self.spawnNomads, iGameTurn, 7, 0, ["TXT_KEY_ADJECTIVE_GOKTURK", "TXT_KEY_ADJECTIVE_UIGHUR"])
                if (iGameTurn > getTurnForYear(900) and iGameTurn <= getTurnForYear(1100)):
			iNumUnits = 2 + iHandicap
			if bGreatWall: iNumUnits = iHandicap
                        self.checkSpawn(iBarbarian, con.iHorseArcher, iNumUnits, (94, 48), (107, 54), self.spawnNomads, iGameTurn, 6, 0, ["TXT_KEY_ADJECTIVE_JURCHEN"])
                        
                #tibet
                if (iGameTurn >= getTurnForYear(-350) and iGameTurn <= getTurnForYear(1100)):
                        self.checkSpawn(iBarbarian, con.iSwordsman, 1 + iHandicap, (92, 41), (99, 45), self.spawnMinors, iGameTurn, 10-iHandicap, 3, ["TXT_KEY_ADJECTIVE_TIBETAN"])

                #elephants in india pre-khmer
                if (iGameTurn >= getTurnForYear(-210) and iGameTurn <= getTurnForYear(700)):
                        self.checkSpawn(iBarbarian, con.iWarElephant, 1, (86, 31), (100, 41), self.spawnInvaders, iGameTurn, 8-iHandicap, 4)

		#Indo-Scythians
		if iGameTurn >= getTurnForYear(-200) and iGameTurn <= getTurnForYear(400):
			self.checkSpawn(iBarbarian, con.iHorseArcher, 2, (84, 40), (89, 43), self.spawnNomads, iGameTurn, 8-iHandicap, 4, ["TXT_KEY_ADJECTIVE_INDO_SCYTHIAN"])

		#Kushana
		if iGameTurn >= getTurnForYear(30) and iGameTurn <= getTurnForYear(220):
			self.checkSpawn(iBarbarian, con.iKushanAsvaka, 3+iHandicap, (84, 40), (89, 43), self.spawnInvaders, iGameTurn, 8, 3, ["TXT_KEY_ADJECTIVE_KUSHANA"])

		#Hephtalites
		if iGameTurn >= getTurnForYear(400) and iGameTurn <= getTurnForYear(550):
			self.checkSpawn(iBarbarian, con.iHorseArcher, 2+iHandicap, (84, 40), (89, 43), self.spawnInvaders, iGameTurn, 5-iHandicap, 2, ["TXT_KEY_ADJECTIVE_HEPHTHALITE"])

       
                        
                #pirates in Mediterranean
                if (iGameTurn >= getTurnForYear(-210) and iGameTurn <= getTurnForYear(50)):
                        self.checkSpawn(iBarbarian, con.iTrireme, 1, (49, 37), (72, 44), self.spawnPirates, iGameTurn, 8, 0)
                #pirates in Barbary coast
                if (iGameTurn >= getTurnForYear(50) and iGameTurn <= getTurnForYear(700)):
                        self.checkSpawn(iBarbarian, con.iTrireme, 1, (46, 30), (62, 39), self.spawnPirates, iGameTurn, 18, 0)
                if (iGameTurn >= getTurnForYear(700) and iGameTurn <= getTurnForYear(1400)):
                        self.checkSpawn(iBarbarian, con.iTrireme, 1, (46, 30), (62, 39), self.spawnPirates, iGameTurn, 8, 0)
                #pirates in Indian ocean
                if (iGameTurn >= getTurnForYear(-650) and iGameTurn <= getTurnForYear(700)):
                        self.checkSpawn(iBarbarian, con.iTrireme, 1, (72, 20), (91, 36), self.spawnPirates, iGameTurn, 18, 0)
                if (iGameTurn >= getTurnForYear(700) and iGameTurn <= getTurnForYear(1700)):
                        self.checkSpawn(iBarbarian, con.iTrireme, 1, (72, 20), (91, 36), self.spawnPirates, iGameTurn, 10, 0)



		# Leoreth: Barbarians in Anatolia (Hittites), replace Hattusas spawn
		if (iGameTurn >= getTurnForYear(-2000) and iGameTurn <= getTurnForYear(-800)):
			self.checkSpawn(iBarbarian, con.iHittiteHuluganni, 2 + iHandicap, (68, 42), (74, 45), self.spawnInvaders, iGameTurn, 12, 0, ["TXT_KEY_ADJECTIVE_HITTITE"])
                        
                #barbarians in europe
                if (iGameTurn >= getTurnForYear(-210) and iGameTurn <= getTurnForYear(470)):
                        self.checkSpawn(iBarbarian, con.iAxeman, 3 + iHandicap, (50, 45), (63, 52), self.spawnInvaders, iGameTurn, 12, 0, ["TXT_KEY_ADJECTIVE_GERMANIC"])
			self.checkSpawn(iBarbarian, con.iAxeman, 2 + iHandicap, (64, 49), (69, 55), self.spawnInvaders, iGameTurn, 14, 2, ["TXT_KEY_ADJECTIVE_GERMANIC"])
		# Leoreth: begins 100 AD instead of 50 AD
                if (iGameTurn >= getTurnForYear(100) and iGameTurn <= getTurnForYear(470)):
                        self.checkSpawn(iBarbarian, con.iSwordsman, 3, (58, 45), (70, 55), self.spawnInvaders, iGameTurn, 10, 5, ["TXT_KEY_ADJECTIVE_GERMANIC"])
                if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(550)):
                        self.checkSpawn(iBarbarian, con.iAxeman, 4 + iHandicap, (49, 41), (56, 52), self.spawnInvaders, iGameTurn, 6, 4, ["TXT_KEY_ADJECTIVE_VISIGOTHIC"])
			self.checkSpawn(iBarbarian, con.iSwordsman, 4 + iHandicap, (49, 41), (57, 52), self.spawnInvaders, iGameTurn, 6, 2, ["TXT_KEY_ADJECTIVE_VISIGOTHIC"])
			self.checkSpawn(iBarbarian, con.iHorseArcher, 3, (55, 49), (65, 53), self.spawnInvaders, iGameTurn, 6, 0, ["TXT_KEY_ADJECTIVE_HUNNIC"])
                if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(700)):
                        self.checkSpawn(iBarbarian, con.iHorseArcher, 3 + iHandicap, (58, 50), (88, 53), self.spawnInvaders, iGameTurn, 4, 2, ["TXT_KEY_ADJECTIVE_HUNNIC"])

		#Leoreth: barbarians in Balkans / Black Sea until the High Middle Ages (Bulgarians, Cumans, Pechenegs)
		if (iGameTurn >= getTurnForYear(680) and iGameTurn <= getTurnForYear(1000)):
			self.checkSpawn(iBarbarian, con.iHorseArcher, 3 + iHandicap, (64, 45), (69, 49), self.spawnInvaders, iGameTurn, 6, 2, ["TXT_KEY_ADJECTIVE_AVAR", "TXT_KEY_ADJECTIVE_BULGAR"])
		if (iGameTurn >= getTurnForYear(900) and iGameTurn <= getTurnForYear(1200)):
			self.checkSpawn(iBarbarian, con.iHorseArcher, 3 + iHandicap, (68, 48), (78, 50), self.spawnInvaders, iGameTurn, 8, 5, ["TXT_KEY_ADJECTIVE_CUMAN"])

                #barbarians in central asia
                if (iGameTurn >= getTurnForYear(-1600) and iGameTurn < getTurnForYear(-850)):
                        self.checkSpawn(iBarbarian, con.iSumerianVulture, 2 + iHandicap, (74, 34), (78, 44), self.spawnNomads, iGameTurn, 6-iHandicap, 2, ["TXT_KEY_ADJECTIVE_ASSYRIAN"])
                if (iGameTurn >= getTurnForYear(-850) and iGameTurn < getTurnForYear(300)):
                        self.checkSpawn(iBarbarian, con.iSumerianVulture, 1 + iHandicap, (73, 38), (78, 44), self.spawnNomads, iGameTurn, 7-iHandicap, 2, ["TXT_KEY_ADJECTIVE_ASSYRIAN"])
			self.checkSpawn(iBarbarian, con.iHorseArcher, 2 + iHandicap, (79, 41), (84, 49), self.spawnInvaders, iGameTurn, 7-iHandicap, 2, ["TXT_KEY_ADJECTIVE_PARTHIAN"])
                if (iGameTurn >= getTurnForYear(300) and iGameTurn <= getTurnForYear(700)):
                        if utils.getScenario() == con.i3000BC:  #late start condition
                                self.checkSpawn(iBarbarian, con.iHorseArcher, 3 + iHandicap, (78, 42), (88, 50), self.spawnNomads, iGameTurn, 8-iHandicap, 2, ["TXT_KEY_ADJECTIVE_TURKIC"])
                if (iGameTurn > getTurnForYear(700) and iGameTurn <= getTurnForYear(1040)):
                        if utils.getScenario() == con.i3000BC:  #late start condition
                                self.checkSpawn(iBarbarian, con.iHorseArcher, 2 + iHandicap, (78, 42), (90, 52), self.spawnNomads, iGameTurn, 6-iHandicap, 2, ["TXT_KEY_ADJECTIVE_TURKIC"])
                        
                #barbarians in Elam
                if (iGameTurn >= getTurnForYear(-1600) and iGameTurn < getTurnForYear(-1000)):
                        self.checkSpawn(iBarbarian, con.iChariot, 2, (81, 37), (87, 45), self.spawnMinors, iGameTurn, 7-iHandicap, 0, ["TXT_KEY_ADJECTIVE_ELAMITE"])

                #barbarians in north africa
                if (iGameTurn >= getTurnForYear(-210) and iGameTurn < getTurnForYear(50)):
                        self.checkSpawn(iBarbarian, con.iCarthageNumidianCavalry, 1, (54, 31), (67, 35), self.spawnNomads, iGameTurn, 9-iHandicap, 3, ["TXT_KEY_ADJECTIVE_BERBER"])
                if (iGameTurn >= getTurnForYear(50) and iGameTurn < getTurnForYear(900)):
                        if utils.getScenario() == con.i3000BC:  #late start condition
				self.checkSpawn(iBarbarian, con.iCarthageNumidianCavalry, 4 + iHandicap, (54, 31), (67, 35), self.spawnNomads, iGameTurn, 10-iHandicap, 5, ["TXT_KEY_ADJECTIVE_BERBER"])
                if (iGameTurn >= getTurnForYear(900) and iGameTurn <= getTurnForYear(1800)):
                        self.checkSpawn(iBarbarian, con.iCamelArcher, 1, (54, 27), (67, 35), self.spawnNomads, iGameTurn, 8-iHandicap, 4, ["TXT_KEY_ADJECTIVE_BERBER"])
                        
                #camels in arabia
                if (iGameTurn >= getTurnForYear(190) and iGameTurn <= getTurnForYear(550)):
                        self.checkSpawn(iBarbarian, con.iCamelArcher, 2, (73, 30), (82, 36), self.spawnNomads, iGameTurn, 9-iHandicap, 7, ["TXT_KEY_ADJECTIVE_BEDOUIN"])
                if iGameTurn >= getTurnForYear(-800) and iGameTurn <= getTurnForYear(1300):
			iNumUnits = 1 + iHandicap
			if utils.getScenario() == con.i3000BC: iNumUnits += 1
			if iGameTurn >= getTurnForYear(400): iNumUnits += 2
			self.checkSpawn(iBarbarian, con.iNubianMedjay, iNumUnits, (66, 28), (71, 34), self.spawnUprising, iGameTurn, 12, 4, ["TXT_KEY_ADJECTIVE_NUBIAN"])
                if (iGameTurn >= getTurnForYear(450) and iGameTurn <= getTurnForYear(1600)):
                        if utils.getScenario() == con.i3000BC:
                                self.checkSpawn(iNative, con.iZuluImpi, 3 + iHandicap, (60, 10), (72, 27), self.spawnNatives, iGameTurn, 10, 4)
                        else:
                                self.checkSpawn(iNative, con.iZuluImpi, 3 + iHandicap, (60, 10), (72, 27), self.spawnNatives, iGameTurn, 15, 4)
		if iGameTurn >= getTurnForYear(1600) and iGameTurn <= getTurnForYear(1800):
			self.checkSpawn(iNative, con.iKongoPombos, 2 + iHandicap, (60, 10), (72, 27), self.spawnNatives, iGameTurn, 10, 4)
				
                #west africa
                if (iGameTurn >= getTurnForYear(450) and iGameTurn <= getTurnForYear(1700)):
                        if iGameTurn < getTurnForYear(1300):
				sAdj = ["TXT_KEY_ADJECTIVE_GHANAIAN"]
			else:
				sAdj = ["TXT_KEY_ADJECTIVE_SONGHAI"]
			self.checkSpawn(iBarbarian, con.iMandeFarari, 1, (48, 26), (65, 37), self.spawnMinors, iGameTurn, 16, 4, sAdj)
			self.checkSpawn(iBarbarian, con.iZuluImpi, 2, (48, 22), (63, 29), self.spawnMinors, iGameTurn, 16, 10, sAdj)

                #American natives
                if (iGameTurn >= getTurnForYear(600) and iGameTurn <= getTurnForYear(1100)):
                        self.checkSpawn(iBarbarian, con.iNativeAmericaDogSoldier, 2 + iHandicap, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 20, 0)
                        if utils.getScenario() == con.i3000BC:  #late start condition
                                self.checkSpawn(iBarbarian, con.iAztecJaguar, 3, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
                        else:  #late start condition
                                self.checkSpawn(iBarbarian, con.iAztecJaguar, 2, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
                if (iGameTurn >= getTurnForYear(1300) and iGameTurn <= getTurnForYear(1600)):
                        self.checkSpawn(iBarbarian, con.iNativeAmericaDogSoldier, 3 + iHandicap, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 8, 0)
                if (iGameTurn >= getTurnForYear(1400) and iGameTurn <= getTurnForYear(1800)):
                        self.checkSpawn(iBarbarian, con.iNativeAmericaDogSoldier, 2 + iHandicap, (11, 44), (33, 51), self.spawnUprising, iGameTurn, 12, 0)
			self.checkSpawn(iBarbarian, con.iNativeAmericaDogSoldier, 2 + iHandicap, (11, 44), (33, 51), self.spawnUprising, iGameTurn, 12, 6)
                if (iGameTurn >= getTurnForYear(1300) and iGameTurn <= getTurnForYear(1600)):
                        if (iGameTurn % 18 == 0):
                                if (gc.getMap().plot(27, 29).getNumUnits() == 0):
                                        self.makeUnit(con.iNativeAmericaDogSoldier, iBarbarian, (27, 29), 3 + iHandicap, 1)
                        if (iGameTurn % 18 == 9):
                                if (gc.getMap().plot(30, 13).getNumUnits() == 0):
                                        self.makeUnit(con.iNativeAmericaDogSoldier, iBarbarian, (30, 13), 3 + iHandicap, 1)
					
		if iGameTurn >= getTurnForYear(1700) and iGameTurn <= getTurnForYear(1900):
			self.checkSpawn(iBarbarian, con.iSiouxMountedBrave, 1 + iHandicap, (15, 44), (24, 52), self.spawnUprising, iGameTurn, 12 - iHandicap, 2)
			
		if iGameTurn >= getTurnForYear(1500) and iGameTurn <= getTurnForYear(1850):
			self.checkSpawn(iBarbarian, con.iIroquoisMohawk, 2 + iHandicap, (24, 46), (30, 51), self.spawnUprising, iGameTurn, 8 - iHandicap, 4)
			
			
                #pirates in the Caribbean
                if (iGameTurn >= getTurnForYear(1600) and iGameTurn <= getTurnForYear(1800)):
                        self.checkSpawn(iBarbarian, con.iPrivateer, 1, (24, 32), (35, 46), self.spawnPirates, iGameTurn, 5, 0)
                #pirates in Asia
                if (iGameTurn >= getTurnForYear(1500) and iGameTurn <= getTurnForYear(1900)):
                        self.checkSpawn(iBarbarian, con.iPrivateer, 1, (72, 24), (110, 36), self.spawnPirates, iGameTurn, 8, 0)



                self.foundCity(iIndependent, lJerusalem, "Yerushalayim", iGameTurn, 2, con.iArcher, 3)                        
                self.foundCity(iIndependent2, lSusa, "Shushan", iGameTurn, 1, con.iArcher, 1)
                self.foundCity(iIndependent, lSamarkand, "Afrasiyab", iGameTurn, 1, con.iArcher, 1)
                self.foundCity(iCeltia, lMilan, "Melpum", iGameTurn, 2, con.iArcher, 2)
                self.foundCity(iCeltia, lLyon, "Lugodunon", iGameTurn, 2, -1, -1)
                self.foundCity(iCeltia, lBordeaux, "Burdigala", iGameTurn, 2, -1, -1)
                self.foundCity(iIndependent2, lArtaxata, "Artashat", iGameTurn, 1, -1, -1)
                self.foundCity(iCeltia, lLutetia, "Lutetia", iGameTurn, 2, -1, -1)
                self.foundCity(iIndependent, lSanaa, "Sana'a", iGameTurn, 1, -1, -1)
                self.foundCity(iIndependent2, lPagan, "Pagan", iGameTurn, 2, -1, -1)
                self.foundCity(iBarbarian, lLhasa, "Lasa", iGameTurn, 2, -1, -1)
                self.foundCity(iBarbarian, lHanoi, "Hanoi", iGameTurn, 2, -1, -1)
		
		self.foundCity(iNative, lTiwanaku, "Tiwanaku", iGameTurn, 1, -1, -1)
                self.foundCity(iNative, lTucume, "Tucume", iGameTurn, 1, con.iArcher, 2)
		self.foundCity(iNative, lChanChan, "Chan Chan", iGameTurn, 2, con.iArcher, 2)
		
		self.foundCity(iIndependent, lKiev, "Kyiv", iGameTurn, 2, con.iLongbowman, 2, [con.iOrthodoxy])
                if utils.getScenario() == con.i3000BC:
                        self.foundCity(iCeltia, lDublin, "&#193;th Cliath", iGameTurn, 1, -1, -1)
                else:
                        self.foundCity(iIndependent, lDublin, "&#193;th Cliath", iGameTurn, 1, -1, -1)
		self.foundCity(iIndependent, lVienna, "Wien", iGameTurn, 1, con.iLongbowman, 1)
                self.foundCity(iNative, lQuelimane, "Quelimane", iGameTurn, 1, con.iZuluImpi, 1)
                self.foundCity(iNative, lMombasa, "Mombasa", iGameTurn, 1, con.iZuluImpi, 1)
                self.foundCity(iBarbarian, lKazan, "Kazan", iGameTurn, 2, con.iHorseArcher, 1)
                self.foundCity(iNative, lKongo, "Mbanza Kongo", iGameTurn, 1, con.iZuluImpi, 1)

		if utils.getHumanID() != con.iTamils:
			self.foundCity(iIndependent, lMadras, "Kanchipuram", iGameTurn, 2, con.iArcher, 1)
			
		if not gc.getPlayer(con.iTamils).isAlive():
			self.foundCity(iIndependent, lThanjavur, "Tanjapuri", iGameTurn, 1, con.iWarElephant, 1)

		self.foundCity(iIndependent, lVaranasi, "Varanasi", iGameTurn, 1, con.iWarrior, 1)
		self.foundCity(iIndependent, lIndraprastha, "Indraprastha", iGameTurn, 1, con.iWarrior, 1)

                if ( self.foundCity(iBarbarian, lDunhuang, "Dunhuang", iGameTurn, 1, con.iArcher, 1) ): #Orka                    
                        if (not gc.getPlayer(con.iChina).isHuman()): #Orka     
                                self.makeUnit(con.iHorseArcher, con.iChina, (99, 46), 3, 1)     
                self.foundCity(iBarbarian, lKashgar, "Kashgar", iGameTurn, 1, con.iArcher, 1) #Orka

		if utils.getHumanID() != con.iChina:
			self.foundCity(iIndependent, lBeijing, "Zhongdu", iGameTurn, 2, con.iSpearman, 1)

		self.foundCity(iBarbarian, lShenyang, "Simiyan hoton", iGameTurn, 2, con.iChariot, 2)

		self.foundCity(iIndependent, lAnkara, "Ankuwash", iGameTurn, 2, con.iArcher, 2)
		
		if utils.getHumanID() != con.iHolyRome:
			if utils.getSeed() % 4 == 0:
				self.foundCity(iIndependent, lLubeck, "L&#252;beck", iGameTurn, 2, con.iCrossbowman, 1)
			else:
				self.foundCity(iIndependent, lHamburg, "Hamburg", iGameTurn, 2, con.iCrossbowman, 1)
				
		if utils.getScenario() == con.i3000BC:
			self.foundCity(iIndependent, lMarrakesh, "Marrakus", iGameTurn, 1, con.iCrossbowman, 1)


                if iGameTurn == getTurnForYear(-3000):
			gc.getMap().plot(lJerusalem[0], lJerusalem[1]).getPlotCity().setHasRealBuilding(con.iTempleOfSalomon, True)
			
		if iGameTurn == getTurnForYear(con.tBirth[con.iInca]):
			if utils.getHumanID() == con.iInca:
				utils.makeUnit(con.iIncanQuechua, iNative, (lTucume[0], lTucume[1]), 1)
				utils.makeUnit(con.iIncanQuechua, iNative, (lChanChan[0], lChanChan[1]), 1)



        def getCity(self, tCoords): #by LOQ
                'Returns a city at coordinates tCoords.'
                return CyGlobalContext().getMap().plot(tCoords[0], tCoords[1]).getPlotCity()

        def foundCity(self, iCiv, lCity, name, iTurn, iPopulation, iUnitType, iNumUnits, lReligions=[]):
                if ((iTurn == getTurnForYear(lCity[2]) + lCity[3]) and (lCity[3]<10)): # conversion from years - edead
                        #print self.checkRegion(tUr)
                        bResult, lCity[3] = self.checkRegion(lCity)
			print ("bResult: "+repr(bResult))
                        if (bResult == True):
                                pCiv = gc.getPlayer(iCiv)
				print ("Attempting to found city "+name+" with "+repr(lCity))
				# the code gets to this point, then crashes
                                pCiv.found(lCity[0], lCity[1])
				# this point is not reached anymore
				print "City founded"
                                self.getCity((lCity[0], lCity[1])).setName(name, False)
				print "Name set"
                                if (iPopulation != 1):
                                        self.getCity((lCity[0], lCity[1])).setPopulation(iPopulation)
					print "Population set"
                                if (iNumUnits > 0):
                                        self.makeUnit(iUnitType, iCiv, (lCity[0], lCity[1]), iNumUnits, 0)
					print "Units created"
				for iReligion in lReligions:
					self.getCity((lCity[0], lCity[1])).setHasReligion(iReligion, True, False, False)
                                return True
                        if (bResult == False) and (lCity[3] == -1):
                                return False
                               

        def checkRegion(self, tCity):
                cityPlot = gc.getMap().plot(tCity[0], tCity[1])
                iNumUnitsInAPlot = cityPlot.getNumUnits()
##                print iNumUnitsInAPlot
                
                #checks if the plot already belongs to someone
                if (cityPlot.isOwned()):
                        if (cityPlot.getOwner() != iBarbarian ):
                                return (False, -1)
                    
##                #checks if there's a unit on the plot
                if (iNumUnitsInAPlot):
                        for i in range(iNumUnitsInAPlot):
                                unit = cityPlot.getUnit(i)
                                iOwner = unit.getOwner()
                                if (iOwner == iBarbarian):
                                        return (False, tCity[3]+1) 
                                #pOwner = gc.getPlayer(iOwner)
                                #if (pOwner.isHuman()):
                                #        return (False, tCity[3]+1)                    

                #checks the surroundings and allows only AI units
                for x in range(tCity[0]-1, tCity[0]+2):
                        for y in range(tCity[1]-1, tCity[1]+2):
                                currentPlot=gc.getMap().plot(x,y)
                                if (currentPlot.isCity()):
                                        return (False, -1)                                
                                iNumUnitsInAPlot = currentPlot.getNumUnits()
                                if (iNumUnitsInAPlot):
                                        for i in range(iNumUnitsInAPlot):
                                                unit = currentPlot.getUnit(i)
                                                iOwner = unit.getOwner()
                                                pOwner = gc.getPlayer(iOwner)
                                                if (pOwner.isHuman()):
                                                        return (False, tCity[3]+1)
                return (True, tCity[3])



        def spawnUnits(self, iCiv, tTopLeft, tBottomRight, iUnitType, iNumUnits, iTurn, iPeriod, iRest, function, iForceAttack):
                if (iTurn % utils.getTurns(iPeriod) == iRest):
                        dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, function, [] )
                        if (len(plotList)):
                                rndNum = gc.getGame().getSorenRandNum(len(plotList), 'Spawn units')
                                result = plotList[rndNum]
                                if (result):
                                        self.makeUnit(iUnitType, iCiv, result, iNumUnits, iForceAttack)
                                


	    
        def killNeighbours(self, tCoords):
                'Kills all units in the neigbbouring tiles of plot (as well as plot itself) so late starters have some space.'
                for x in range(tCoords[0]-1, tCoords[0]+2):        # from x-1 to x+1
                        for y in range(tCoords[1]-1, tCoords[1]+2):	# from y-1 to y+1
                                killPlot = CyMap().getPlot(x, y)
                                for i in range(killPlot.getNumUnits()):
                                        unit = killPlot.getUnit(0)	# 0 instead of i because killing units changes the indices
                                        unit.kill(False, iBarbarian)
					
	#Leoreth: new ways to spawn barbarians
	def checkSpawn(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj=[]):
	
		if len(lAdj) == 0:
			sAdj = ""
		else:
			sAdj = utils.getRandomEntry(lAdj)
	
		if iTurn % utils.getTurns(iPeriod) == iRest:
			spawnFunction(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj)
			
	def getFreeWaterTiles(self, tTL, tBR, bTerritory=False, bOcean=False):
	
		plotList = []
	
		for x in range(tTL[0], tBR[0]+1):
			for y in range(tTL[1], tBR[1]+1):
				plot = gc.getMap().plot(x,y)
				if plot.getTerrainType() == con.iCoast or (bOcean and plot.getTerrainType() == con.iOcean):
					if not plot.isUnit() and plot.area().getNumTiles() > 10:
						if not (bTerritory and plot.getOwner() != -1):
							plotList.append((x,y))
							
		return plotList
		
	def getFreeLandTiles(self, tTL, tBR, bTerritory=False, bJungle=False):
	
		plotList = []
	
		for x in range(tTL[0], tBR[0]+1):
			for y in range(tTL[1], tBR[1]+1):
				plot = gc.getMap().plot(x,y)
				if plot.isHills() or plot.isFlatlands():
					if plot.getTerrainType() != con.iMarsh and (bJungle or plot.getFeatureType() != con.iJungle):
						if not plot.isUnit() and not plot.isCity():
							bClear = True
							for i in range(x-1, x+2):
								for j in range(y-1, y+2):
									if gc.getMap().plot(i,j).isUnit(): bClear = False
								
							if bClear and not (bTerritory and plot.getOwner() != -1):
								plotList.append((x,y))
							
		return plotList
		
	def getTargetCities(self, tTL, tBR):
		cityPlotList = []
		
		for x in range(tTL[0], tBR[0]+1):
			for y in range(tTL[1], tBR[1]+1):
				plot = gc.getMap().plot(x,y)
				if plot.isCity():
					city = plot.getPlotCity()
					if city.getOwner() < con.iNumPlayers and (city.getPopulation() > 1 or city.getCultureLevel() > 0):
						cityPlotList.append((city.getX(), city.getY()))
						
		return cityPlotList
		
	def getCitySpawnPlot(self, tPlot):
		x, y = tPlot
		plotList = []
		
		for i in range(x-2, x+3):
			for j in range(y-2, y+3):
				if abs(x-i) == 2 or abs(y-j) == 2:
					if not gc.getMap().plot(i,j).isUnit() and not gc.getMap().plot(i,j).isWater():
						plotList.append((i,j))
						
		return utils.getRandomEntry(plotList)

	def spawnPirates(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: spawns all ships at the same coastal spot, out to pillage and disrupt trade, can spawn inside borders'''
	
		plotList = self.getFreeWaterTiles(tTL, tBR, False, False)
		tPlot = utils.getRandomEntry(plotList)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_PIRATE_SEA, iNumUnits, sAdj)
		
	def spawnNatives(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: outside of territory, in jungles, all dispersed on several plots, out to pillage'''
		
		plotList = self.getFreeLandTiles(tTL, tBR, True, True)
		
		for i in range(iNumUnits):
			tPlot = utils.getRandomEntry(plotList)
			if not tPlot: break
			
			plotList.remove(tPlot)
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, 1, sAdj)
			
	def spawnMinors(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents minor states without ingame cities
			    outside of territory, not in jungles, in groups, passive'''
			    
		plotList = self.getFreeLandTiles(tTL, tBR, True, False)
		tPlot = utils.getRandomEntry(plotList)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
		
	def spawnNomads(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents aggressive steppe nomads etc.
			    outside of territory, not in jungles, in small groups, target cities'''
			    
		plotList = self.getFreeLandTiles(tTL, tBR, True, False)
		iUnitsLeft = iNumUnits
		iGroupSize = 2
		
		if iNumUnits > 5: iGroupSize = 3	# shouldn't be larger than 8 where 4 per group would be better (maximum is 7 currently)
		
		while iUnitsLeft > 0:
			tPlot = utils.getRandomEntry(plotList)
			if not tPlot: break
			plotList.remove(tPlot)
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, min(iUnitsLeft, iGroupSize), sAdj)
			iUnitsLeft -= iGroupSize
			
	def spawnInvaders(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents large invasion forces and migration movements
			    inside of territory, not in jungles, in groups, target cities'''
			    
		plotList = self.getFreeLandTiles(tTL, tBR, False, False)
		tPlot = utils.getRandomEntry(plotList)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
			
	def spawnUprising(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		''' Leoreth: represents uprisings of Natives against colonial settlements, especially North America
			     spawns units in a free plot in the second ring of a random target city in the area'''
			     
		targetCityList = self.getTargetCities(tTL, tBR)
		tCity = utils.getRandomEntry(targetCityList)
		
		if tCity:
			tPlot = self.getCitySpawnPlot(tCity)
			
			if tPlot:
				utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)