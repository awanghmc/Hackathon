
#Authors: Scott Chow, Reed Haubenstock, Thomas Le, Aaron Wang

import re, urllib
from time import gmtime, strftime

portfolio=[]
Player=[]

def get_quote(symbol):
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    find_q = re.search(r'\<span\sid="ref_\d+.*">(.+)<', content)
    if find_q:
        quote = find_q.group(1)
    else:
        quote = 'none fuck there'
    return quote

def profilemaker():
    """prompts user for a username. Sets  100000"""
    while True:
        username = raw_input("Type in your username: ")
        if len(username)>10:
            print "usernames must be 10 characters or less"
            continue
        else:
            check = usernamevalidation(username)
            if check == False:
                continue
            else:
                break
    while True:
        try:
            initial_money=float(input("Type in how much money you want to start with (Must be include cents. ie $100.00): "))
            if moneyvalidation(initial_money)==True:
                break
            else:
                continue
        except:
            print "Please input a valid money amount."

    Player.append(username)
    Player.append(initial_money)
    Player.append(initial_money)
    return Player

def usernamevalidation(S):
    illegalcharacters = "\"\',@#$%^&*()<>?.!:{}[]+-=/\\"
    checker=0
    for i in range(len(illegalcharacters)):
        if illegalcharacters[i] in S:
            print "Cannot have", illegalcharacters[i], "in username"
            checker=1
        else:
            continue
    if checker==1:
        return False
    else:
        return True

def moneyvalidation(Money):
    checker=0
    while True:
        cents=Money%1
        if 100*cents%1!=0:
            print "Must enter dollar and cent amounts (ie. 1.00 not 1)"
            checker = 1
            break
        elif Money<0.01:
            print "Money must be at least $0.01"
            checker = 1
            break
        elif Money>1000000000000:
            print "Money must be less than $1,000,000,000,000"
            checker = 1
            break
        else:
            break
    if checker ==0:
        return True
    else:
        return False

def main():
    """Gives user a list of choices to make e.g. buy/sell/check portfolio."""

    print "==================WELCOME=================="
    print "Welcome to Market Sim"
    print "Practice trading stocks and shit."
    print "Written by SC,RH,TL,AW"
    print "==========================================="
    print
    print
    profilemaker()
    menu()
    

def menu():
  
    print
    print '===================='
    print "Main Menu"
    print '===================='
    print "Hi "+Player[0]+", what would you like to do today?"
    print
    print "(1) Display Portfolio Summary"
    print "(2) Buy Stocks."
    print "(3) Sell Stocks."
    print "(4) Get current prices."
    print "(5) Exit."
    print
    user_input=raw_input("Enter choice: ")
    if user_input=="1":
        portfolioSum()
    elif user_input=="2":
        buyStock()
    elif user_input=="3":
        if len(portfolio)==0:
            print 'You dont own any stocks to sell!'
            menu()
        else:
            sellStocks()
    elif user_input=="4":
        findPrice()
    elif user_input=="5":
        print 'Good Day'
        return


def portfolioSum():
    
    print
    print " Stock Value: $"+str(stockbalance())
    print "Cash Balance: $"+str(Player[1])
    print " Total Value: $"+str(worth())
    print "    Net Gain: "+str(perworthchange())
    print
    if len(portfolio)==0:
        print "You currently have no shares in your portfolio."
        menu()
    
    print "  Company Name | # Stocks Owned | Total Stock Value"
    print '----------------------------------------------------'
    for x in range(len(portfolio)):
        if portfolio[x][1]==0:
            continue
        print'%14s %16s %19s' % (portfolio[x][0][:13], portfolio[x][1],"$"+str(float(removeComma(get_quote(portfolio[x][0])))*float(portfolio[x][1])))
    print 
    menu()


def stockbalance():
    
    stockSum=0
    for i in range(len(portfolio)):
        stockSum+=float(removeComma(get_quote(portfolio[i][0])))*float(portfolio[i][1])
    return stockSum

def worth():
    return Player[1] + stockbalance()

def perworthchange():
    
    percent = 100*(1.0*worth())/Player[2]
    
    if worth < Player[2]:
        return str(worth()-Player[2]) + "("+str(100.0-percent)+ "%)"
    else:
        return str(worth()-Player[2]) + "(+"+str(percent-100.0)+ "%)"

def findPrice():
    end=False
    while (end!=True):
        print
        
        print
        stockCheck = raw_input("Enter a stock to check: ")
        if get_quote(stockCheck)=='none fuck there':
            print 'Stock does not exist, please enter a valid company name or symbol.'
            print
            menu()
        stockValue = get_quote(stockCheck)
        print
        print stockCheck+" shares are worth $"+ str(stockValue)+" per share. " + strftime("%Y-%m-%d %H:%M:%S")
   
        print
        checkAgain=raw_input("Check another stock?(Y/N): ")
        if checkAgain=='Y' or checkAgain=='y':
            end=False
        else:
            end=True
    menu()

        
def removeComma(S):
    if S=='':
        return S
    else:
        if S[0]==',':
            return S[1:]
        else:
            return S[0]+removeComma(S[1:])
 
def checkBalance(totalCost):
    if totalCost>Player[1]:
        return False
    else:
        return True



def sellStocks():
    """Takes the player's own portfolio and asks what stocks the player
        would like to sell.
    """
    print '================'
    print "SELL STOCKS"
    print '================'
    
    end=False
    while (end!=True):
        compName=raw_input("What company's stocks would you like to sell? ")
        
        if  not compName in [i[0] for i in portfolio]:
            print "You do not currently own stocks in " + compName+", please select another."
            continue
        else:
            compIndex=[i[0] for i in portfolio].index(compName)
            stockNum=int(portfolio[compIndex][1])
            print "You currently own " + str(stockNum)+ " shares in " + compName+" worth $"+str(float(removeComma(get_quote(compName)))*stockNum)+". "
            print compName+ " is currently worth $"+removeComma(get_quote(compName))+" per share at "+strftime("%Y-%m-%d %H:%M:%S")+". "
        
            number=raw_input("How many stocks would you like to sell? ")
            number=int(number)
            if number>stockNum:
                print "You do not own enough "+compName+ " shares to make this action."
            elif number<=0:
                print "Please enter a valid amount of shares."
            else:
                print
                print "Transaction complete at "+strftime("%Y-%m-%d %H:%M:%S")+". You sold "+str(number)+" of "+compName+" shares for a total of $"+str(number*float(removeComma(get_quote(compName))))
                Player[1]+=number*float(removeComma(get_quote(compName)))
                portfolio[compIndex][1] = stockNum - number
                
               
                print    
                print "You now own "+str(portfolio[compIndex][1])+" shares of "+portfolio[compIndex][0]
                print
                print "Returning to main menu.."
                end=True
    menu()
    
                                     
            



def buyStock():
    print '=================='
    print "BUY STOCKS"
    print '=================='
    end=False
    while(end==False):
        inputStock = raw_input("Please enter the company name or symbol you want to buy: ")
        if get_quote(inputStock)=='none fuck there':
            print 'Stock does not exist, please enter a valid company name or symbol.'
            print
            continue
        print
        print "Current price for " + inputStock + " is $"+get_quote(inputStock)
        print "Your cash balance is $"+str(Player[1])
        numberStock = raw_input("Enter the amount of stocks you wish to purchase. (Enter 0 if you want to search up a new stock)  ")
        if numberStock==0:
            continue
        else:
            totalCost = float(removeComma(get_quote(inputStock)))*float(numberStock)
            print "You are about to purchase "+str(numberStock)+" of "+str(inputStock)+" worth $"+str(totalCost)
            validation = raw_input("Do you want to continue with the purchase?(Y/N): ")
            if validation == 'Y' or 'y':
                if checkBalance(totalCost)==True: #checks portfolio balance, returns True or False
                          
                          portfolio.append([inputStock,numberStock])
                          Player[1]-=totalCost
                          print
                          print "Transaction processed at "+strftime("%Y-%m-%d %H:%M:%S")+". Your current portfolio balance is $"+str(Player[1])
                          end=True
                else:
                          print
                          print "You do not have enough money."
                          end = True
            else:
                    end = True
    print 'Returning to menu...'
    print
    menu()
    




    


if __name__ == "__main__":
    main()
