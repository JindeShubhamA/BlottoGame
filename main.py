import random
import json
#Return 1 if winner is playerA else return -1
#Also return the the difference of troops A and B on the battlefields
def getWinner(playerA, playerB):
    playerA_wins = 0
    playerB_wins = 0
    difference_troops = []
    for i in range(0,len(playerA)):
        difference_troops.append({"index":playerA[i]['index'],"troopsDifference":playerA[i]['troops'] - playerB[i]['troops']})
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
        jsonDistribution.append({'index':i,'troops':distribution[i]})
    return jsonDistribution

#Returns Json of the distribution that will beat the distrubution send via argument
def findDistributionToBeat(sortedDistributionOfTheOpponent,numberOfTroops):
    numberOfTroopsRemaining = numberOfTroops
    distribution = []
    for i in range(0,len(sortedDistributionOfTheOpponent)):
        if((numberOfTroopsRemaining - sortedDistributionOfTheOpponent[i]['troops']) > 1):
            distribution.append({'index':sortedDistributionOfTheOpponent[i]['index'],'troops':sortedDistributionOfTheOpponent[i]['troops'] + 1})
            numberOfTroopsRemaining = numberOfTroopsRemaining - sortedDistributionOfTheOpponent[i]['troops'] - 1
        else:
            distribution.append({'index':sortedDistributionOfTheOpponent[i]['index'],'troops':numberOfTroopsRemaining})
            numberOfTroopsRemaining = 0
    return sorted(distribution, key=lambda i: i['index'])

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
          troops_allocation.append({"index":count + 1,"troops":next_val-prev_val})
          count = count + 1
          prev_val = next_val
    return troops_allocation

if __name__ == "__main__" :
    agentA=distributeTroopsRandomly(8,3)
    agentB=distributeTroopsRandomly(8,3)
    print("Troops Distribution for Agent A\n",agentA)
    print("Troops Distribution for Agent B\n",agentB)
    winner, val = getWinner(agentA,agentB)
    print("Winner of the battle is \n",winner)
    print("Troops remaining for A are \n",val)
    #print getJsonForDistribution(agentA)
    agentB_higherOrder = distributeTroopsForHigherOrderAgent(agentA,agentB,2,8)
    agentA_higherOrder = distributeTroopsForHigherOrderAgent(agentA, agentA,3, 8)
    print ("Distribution for agentA \n",agentA_higherOrder)
    print ("Distribution for agentB \n",agentB_higherOrder)

