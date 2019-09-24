import random
import json
import zmq

#TODO
'''
Some of the Global Variables might be required to read it from the config file or get it from the frontEnd.
HardCoding the global Variables for now
'''
game="BlottoGame"
implementation = "1v1"
noOfTroops = 8
noOfBattleFields = 3
totalPlayers = 2





#Return 1 if winner is playerA else return -1
#Also return the the difference of troops A and B on the battlefields
def getWinner(playerA, playerB):
    playerA_wins = 0
    playerB_wins = 0
    difference_troops = []
    for i in range(0,len(playerA)):
        difference_troops.append({"battleField":playerA[i]['battleField'],"troopsDifference":playerA[i]['troops'] - playerB[i]['troops']})
        if playerA[i]['troops'] > playerB[i]['troops']:
            playerA_wins = playerA_wins + 1
        elif playerA[i]['troops'] == playerB[i]['troops']:
            continue
        else:
            playerB_wins = playerB_wins + 1
    if (playerA_wins > playerB_wins):
        return 1, difference_troops
    elif(playerA_wins == playerB_wins):
        return 0,difference_troops
    else:
        return -1, difference_troops

#Return the json like {{index:0,value:2},{index:1,value:3}}
def getJsonForDistribution(distribution):
    jsonDistribution = []
    for i in range(0,len(distribution)):
        jsonDistribution.append({'battleField':i,'troops':distribution[i]})
    return jsonDistribution

#Returns Json of the distribution that will beat the distrubution send via argument
def findDistributionToBeat(sortedDistributionOfTheOpponent,numberOfTroops):
    numberOfTroopsRemaining = numberOfTroops
    distribution = []
    for i in range(0,len(sortedDistributionOfTheOpponent)):
        if((numberOfTroopsRemaining - sortedDistributionOfTheOpponent[i]['troops']) > 1):
            distribution.append({'battleField':sortedDistributionOfTheOpponent[i]['battleField'],'troops':sortedDistributionOfTheOpponent[i]['troops'] + 1})
            numberOfTroopsRemaining = numberOfTroopsRemaining - sortedDistributionOfTheOpponent[i]['troops'] - 1
        else:
            distribution.append({'battleField':sortedDistributionOfTheOpponent[i]['battleField'],'troops':numberOfTroopsRemaining})
            numberOfTroopsRemaining = 0
    return sorted(distribution, key=lambda i: i['battleField'])

#Will return the troops dostribution for higher order agent
def distributeTroopsForHigherOrderAgent(distributionOfTheOpponent, distributionOfTheUser, orderOfTheAgent, numberOfTroops):
    jsonForDistribution = []
    #distributionReturn = getJsonForDistribution(distributionOfTheUser)
    jsonDistributionForOpponent = distributionOfTheOpponent
    while(orderOfTheAgent > 0):
         sortedDistributionForOpponent=sorted(jsonDistributionForOpponent, key=lambda i: i['troops'])
         distributionReturn = findDistributionToBeat(sortedDistributionForOpponent, numberOfTroops)
         jsonDistributionForOpponent = distributionReturn
         orderOfTheAgent = orderOfTheAgent - 1
    return distributionReturn

#Distribute the troops randomly in given battlefields
def distributeTroopsRandomly(troops, battlefields):
    split=random.sample(range(0, troops+1), battlefields -1)
    split =  sorted(split)
    split.append(troops)
    troops_allocation = []
    prev_val = 0
    count=0
    while( count  < (battlefields)):
          next_val = split[count]
          troops_allocation.append({"battleField":count + 1,"troops":next_val-prev_val})
          count = count + 1
          prev_val = next_val
    return troops_allocation

def getJsonToSend(game,implementation,noOfTroops,noOfBattleFields,totalPlayers,maxWins,agent1Distribution,agent2Distribution,afterBattleDistribution):
    infoJson = {}
    infoJson["Game"] = game
    infoJson["Implementation"] = implementation
    infoJson["battle_fields"] = noOfBattleFields
    infoJson["total_troops"] = noOfTroops
    infoJson["total_players"] = totalPlayers
    infoJson["max_wins"] = maxWins
    distributionOfTroops = []

    #TODO Currently the code is hardcoded for only 2 agents. Needs to add support for more agent

    distributionJson = {}
    distributionJson["Name_of_the_Agent"] = "Agent" + str(1)
    distributionJson["distribution"] = agent1Distribution
    distributionOfTroops.append(distributionJson)
    distributionJson = {}
    distributionJson["Name_of_the_Agent"] = "Agent" + str(2)
    distributionJson["distribution"] = agent2Distribution
    distributionOfTroops.append(distributionJson)
    infoJson["distribution_of_troops"] = distributionOfTroops
    afterBattleResults = []
    for i in range(0,noOfBattleFields):
        infoBattleField = {}
        infoBattleField["battle_field"] = afterBattleDistribution[i]["battleField"]
        #print("AfterBattleDistribution",afterBattleDistribution)
        if(afterBattleDistribution[i]["troopsDifference"]>0):
            winner = "Agent1"
            troops_remaining = afterBattleDistribution[i]["troopsDifference"]
        else:
            winner = "Agent2"
            troops_remaining = -1*afterBattleDistribution[i]["troopsDifference"]
        infoBattleField["winner"] = winner
        infoBattleField["troops_remaining"] = troops_remaining
        afterBattleResults.append(infoBattleField)
    infoJson["After_battle_results"] = afterBattleResults
    return infoJson




if __name__ == "__main__" :
    agentA=distributeTroopsRandomly(noOfTroops,noOfBattleFields)
    agentB=distributeTroopsRandomly(noOfTroops,noOfBattleFields)
    print("Troops Distribution for Agent 1\n",agentA)
    print("Troops Distribution for Agent 2\n",agentB)
    winner, val = getWinner(agentA,agentB)
    print("Winner of the battle is \n",winner)
    print("Troops remaining for A are \n",val)
    #print getJsonForDistribution(agentA)
    agentB_higherOrder = distributeTroopsForHigherOrderAgent(agentA,agentB,3,noOfTroops)
    agentA_higherOrder = distributeTroopsForHigherOrderAgent(agentA, agentA,4, noOfTroops)
    print ("Distribution for agent1 \n",agentA_higherOrder)
    print ("Distribution for agent2 \n",agentB_higherOrder)
    winner,afterBattleDistribution = getWinner(agentA_higherOrder,agentB_higherOrder)
    if(winner):
        maxWins = "Agent1"
    else:
        maxWins = "Agent2"
    #print("After Battle Distribution",afterBattleDistribution[0]['battleField'])
    msgJson = getJsonToSend(game,implementation,noOfTroops,noOfBattleFields,totalPlayers,maxWins,agentA_higherOrder,agentB_higherOrder,afterBattleDistribution)
    print("Msg Json",msgJson)


    '''
    zmq sending msg to the frontend
    '''
    context = zmq.Context()

    #  Socket to talk to server
    socket = context.socket(zmq.REQ)

    socket.connect("tcp://127.0.0.1:5555")

    socket.send_json(msgJson)



