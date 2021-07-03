from django.shortcuts import render


def button(request):
    return render(request,'home.html')

def output(request):
    import requests as rq

    import time

    from bs4 import BeautifulSoup 

    import datetime

    import pandas as pd

    from sklearn.model_selection import train_test_split

    from sklearn.linear_model import LinearRegression


    u = 'https://www.coindesk.com/price/bitcoin'

    bitcoin = []

    bitcoinZ = []

    waitTime = 60
    times = []


    a = 1


    for i in range(3):


        page = rq.get(u) 

        

        soup = BeautifulSoup(page.content, 'html.parser') 

        results = soup.find('div',attrs={'class':'price-large'}) 
        
        price = results.text      

        price = price[1:] 

        price = price.replace(',','')    

        price = float(price) 
        
        bitcoin.append(price)      


        resultsZ = soup.find('div',attrs={'class' : 'percent-change-medium'}) 
        
        priceZ = resultsZ.text       

        priceZ = priceZ[1:] 

        priceZ = priceZ.replace('%','')    

        priceZ = float(priceZ) 

        
        bitcoinZ.append(priceZ)

        now = datetime.datetime.now() 


        date_time = now.strftime("%d/%m/%Y")  

        
        d = date_time.replace('/','')
        times.append(date_time)


        d = {'date':times,'Cost':bitcoin, 'Rate':bitcoinZ}

        df = pd.DataFrame(d) 
        

        time.sleep (5)    

        df = df.set_index('date')

    df.to_csv('Data.csv', mode ='a', header = False)

    dataset = pd.read_csv('Data.csv',index_col='date')

    x = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)



    r = LinearRegression()
    r.fit(x_train, y_train)

    y_pred = r.predict([[5]])

    print(y_pred)

    data = y_pred

    return render(request, 'home.html',{'data':str(y_pred[0])})