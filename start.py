# import streamlit as st
# import requests
# from datetime import datetime
# import pandas as pd
#
# class MControlAPI:
#     def __init__(self, symbol, resolution=1, data_from=None, data_to='2024-02-29 9:15:00.0'):
#         self.symbol = symbol
#         self.resolution = resolution
#         if isinstance(data_to, str):
#             data_to = datetime.strptime(data_to, '%Y-%m-%d %H:%M:%S.%f')
#         self.data_to = int(data_to.timestamp())
#         self.resolution_dt = {
#             '1': 60, '3': 180, '5': 300, '15': 900, '30': 1800,
#             '60': 3600, '300': 18000, 'D': 24*3600, 'W': 7*24*3600,
#             'M': 30*24*3600, '45': 45*24*3600, '120': 120*24*3600, '240': 240*24*3600
#         }
#         self.delta_time = self.resolution_dt[str(self.resolution)]
#         if data_from is None:
#             self.data_from = self.data_to - self.delta_time * 1
#         else:
#             self.data_from = int(data_from.timestamp())
#
#         self.session = requests.sessions.Session()
#         self.session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
#         self.session.get('https://www.moneycontrol.com/stocksmarketsindia/')
#         self.symbol_meta = None
#         self.dataframe = []
#
#     def fetch_symbol_meta(self):
#         if self.symbol_meta is None:
#             self.symbol_meta = self.session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/symbol?symbol=' + self.symbol)
#         return self.symbol_meta
#
#     def fetch_intraday_data(self, countback=None):
#         new_data = 0
#         try:
#             if countback is None:
#                 countback = int((self.data_to - self.data_from) / self.delta_time)
#                 if countback > 376:
#                     countback = 376
#
#             resp = self.session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?' +
#                                     'symbol={0}&resolution={1}&from={2}&to={3}&countback={4}'.format(
#                                         self.symbol, self.resolution, self.data_from, self.data_to, countback))
#             data = resp.json()
#             if data['s'] == 'no_data':
#                 return -1
#
#             df = pd.DataFrame.from_dict(data)
#             df['dt'] = pd.to_datetime(df['t'] + 19800, unit='s')
#
#             n = len(self.dataframe)
#
#             if n == 0:
#                 self.dataframe = df.copy()
#                 new_data = len(self.dataframe)
#
#             else:
#                 df = pd.concat([self.dataframe, df[df['t'].isin(self.dataframe['t']) == False]]).reset_index(drop=True)
#                 self.dataframe = df.copy()
#                 new_data = len(self.dataframe) - n
#
#             self.data_from = self.data_to
#             self.data_to += self.delta_time
#
#         except Exception as ex:
#             new_data = -1
#             st.error(ex)
#
#         return new_data
#
# def main():
#     st.title("MControlAPI Data Fetcher")
#     symbols = ['GPPL', 'SBIN', 'IRFC']  # Example list of symbols
#
#     combined_dataframe = pd.DataFrame()  # Initialize an empty DataFrame to store combined data
#
#     for symbol in symbols:
#         obj = MControlAPI(symbol)
#         nd = 0
#         while nd > -1:
#             nd = obj.fetch_intraday_data()
#             if nd > 0:
#                 obj.dataframe['symbol'] = symbol  # Add symbol column
#                 combined_dataframe = pd.concat([combined_dataframe, obj.dataframe], ignore_index=True)  # Concatenate dataframes
#             break  # Breaking out of the loop after fetching data for one symbol
#
#     # Move 'symbol' column to the first position
#     cols = combined_dataframe.columns.tolist()
#     cols = ['symbol'] + [col for col in cols if col != 'symbol']
#     combined_dataframe = combined_dataframe[cols]
#
#     # Display combined_dataframe
#     st.write(combined_dataframe)
#
#     # Generate file name based on data_to and Start
#     file_name = f"{obj.data_to}_{obj.data_from}_Start.csv"
#
#     # Save combined_dataframe to a CSV file with the generated file name
#     combined_dataframe.to_csv(file_name, index=False)
#
# if __name__ == '__main__':
#     main()

# import streamlit as st
# import requests
# from datetime import datetime
# import pandas as pd
#
# class MControlAPI:
#     def __init__(self, symbol, resolution=1, data_from=None, data_to=None):
#         self.symbol = symbol
#         self.resolution = resolution
#         if data_to is not None:
#             self.data_to = int(data_to.timestamp())
#         else:
#             # Default value if user doesn't provide data_to
#             self.data_to = int(datetime.now().timestamp())  # Assuming you want current timestamp if data_to is not provided
#         self.resolution_dt = {
#             '1': 60, '3': 180, '5': 300, '15': 900, '30': 1800,
#             '60': 3600, '300': 18000, 'D': 24*3600, 'W': 7*24*3600,
#             'M': 30*24*3600, '45': 45*24*3600, '120': 120*24*3600, '240': 240*24*3600
#         }
#         self.delta_time = self.resolution_dt[str(self.resolution)]
#         if data_from is None:
#             self.data_from = self.data_to - self.delta_time * 1
#         else:
#             self.data_from = int(data_from.timestamp())
#
#         self.session = requests.sessions.Session()
#         self.session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
#         self.session.get('https://www.moneycontrol.com/stocksmarketsindia/')
#         self.symbol_meta = None
#         self.dataframe = []
#
#     def fetch_symbol_meta(self):
#         if self.symbol_meta is None:
#             self.symbol_meta = self.session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/symbol?symbol=' + self.symbol)
#         return self.symbol_meta
#
#     def fetch_intraday_data(self, countback=None):
#         new_data = 0
#         try:
#             if countback is None:
#                 countback = int((self.data_to - self.data_from) / self.delta_time)
#                 if countback > 376:
#                     countback = 376
#
#             resp = self.session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?' +
#                                     'symbol={0}&resolution={1}&from={2}&to={3}&countback={4}'.format(
#                                         self.symbol, self.resolution, self.data_from, self.data_to, countback))
#             data = resp.json()
#             if data['s'] == 'no_data':
#                 return -1
#
#             df = pd.DataFrame.from_dict(data)
#             df['dt'] = pd.to_datetime(df['t'] + 19800, unit='s')
#
#             n = len(self.dataframe)
#
#             if n == 0:
#                 self.dataframe = df.copy()
#                 new_data = len(self.dataframe)
#
#             else:
#                 df = pd.concat([self.dataframe, df[df['t'].isin(self.dataframe['t']) == False]]).reset_index(drop=True)
#                 self.dataframe = df.copy()
#                 new_data = len(self.dataframe) - n
#
#             self.data_from = self.data_to
#             self.data_to += self.delta_time
#
#         except Exception as ex:
#             new_data = -1
#             st.error(ex)
#
#         return new_data
#
# def main():
#     st.title("MControlAPI Data Fetcher")
#     symbols = ['GPPL', 'SBIN', 'IRFC']  # Example list of symbols
#     data_to = st.date_input("Select data_to", datetime.now())
#
#     combined_dataframe = pd.DataFrame()  # Initialize an empty DataFrame to store combined data
#
#     for symbol in symbols:
#         obj = MControlAPI(symbol, data_to=data_to)
#         nd = 0
#         while nd > -1:
#             nd = obj.fetch_intraday_data()
#             if nd > 0:
#                 obj.dataframe['symbol'] = symbol  # Add symbol column
#                 combined_dataframe = pd.concat([combined_dataframe, obj.dataframe], ignore_index=True)  # Concatenate dataframes
#             break  # Breaking out of the loop after fetching data for one symbol
#
#     # Move 'symbol' column to the first position
#     cols = combined_dataframe.columns.tolist()
#     cols = ['symbol'] + [col for col in cols if col != 'symbol']
#     combined_dataframe = combined_dataframe[cols]
#
#     # Display combined_dataframe
#     st.write(combined_dataframe)
#
#     # Generate file name based on data_to and Start
#     file_name = f"{obj.data_to}_{obj.data_from}_Start.csv"
#
#     # Save combined_dataframe to a CSV file with the generated file name
#     combined_dataframe.to_csv(file_name, index=False)
#
# if __name__ == '__main__':
#     main()


# F
#
# import streamlit as st
# import requests
# from datetime import datetime, timedelta
# import pandas as pd
#
# class MControlAPI:
#     def __init__(self, symbol, resolution=1, data_from=None, data_to=None):
#         self.symbol = symbol
#         self.resolution = resolution
#         if data_to is not None:
#             self.data_to = datetime.strptime(data_to, '%Y-%m-%d %H:%M:%S.%f')
#         else:
#             # Default value if user doesn't provide data_to
#             self.data_to = datetime.now()  # Assuming you want current datetime if data_to is not provided
#         self.data_to_str = self.data_to.strftime('%Y-%m-%d %H:%M:%S.%f')
#         self.data_to_timestamp = int(self.data_to.timestamp())
#         self.resolution_dt = {
#             '1': 60, '3': 180, '5': 300, '15': 900, '30': 1800,
#             '60': 3600, '300': 18000, 'D': 24*3600, 'W': 7*24*3600,
#             'M': 30*24*3600, '45': 45*24*3600, '120': 120*24*3600, '240': 240*24*3600
#         }
#         self.delta_time = self.resolution_dt[str(self.resolution)]
#         if data_from is None:
#             self.data_from = self.data_to - timedelta(seconds=self.delta_time * 1)
#         else:
#             self.data_from = data_from
#
#         self.session = requests.sessions.Session()
#         self.session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
#         self.session.get('https://www.moneycontrol.com/stocksmarketsindia/')
#         self.symbol_meta = None
#         self.dataframe = []
#
#     def fetch_symbol_meta(self):
#         if self.symbol_meta is None:
#             self.symbol_meta = self.session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/symbol?symbol=' + self.symbol)
#         return self.symbol_meta
#
#     def fetch_intraday_data(self, countback=None):
#         new_data = 0
#         try:
#             if countback is None:
#                 countback = int((self.data_to_timestamp - self.data_from.timestamp()) / self.delta_time)
#                 if countback > 376:
#                     countback = 376
#
#             resp = self.session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?' +
#                                     'symbol={0}&resolution={1}&from={2}&to={3}&countback={4}'.format(
#                                         self.symbol, self.resolution, self.data_from.timestamp(), self.data_to_timestamp, countback))
#             data = resp.json()
#             if data['s'] == 'no_data':
#                 return -1
#
#             df = pd.DataFrame.from_dict(data)
#             df['dt'] = pd.to_datetime(df['t'] + 19800, unit='s')
#
#             n = len(self.dataframe)
#
#             if n == 0:
#                 self.dataframe = df.copy()
#                 new_data = len(self.dataframe)
#
#             else:
#                 df = pd.concat([self.dataframe, df[df['t'].isin(self.dataframe['t']) == False]]).reset_index(drop=True)
#                 self.dataframe = df.copy()
#                 new_data = len(self.dataframe) - n
#
#             self.data_from = self.data_to
#             self.data_to += timedelta(seconds=self.delta_time)
#
#         except Exception as ex:
#             new_data = -1
#             st.error(ex)
#
#         return new_data
#
# def main():
#     st.title("Welcome! Data Analysis World...")
#     entered_password = st.text_input("Enter Password:", type="password")
#
#     if entered_password == "///":
#         st.success("Access granted! You are now logged in.")
#
#
#         st.title("MControlAPI Data Fetcher")
#         symbols = ['360ONE','3MINDIA','ABB','ACC','AIAENG','APLAPOLLO','AUBANK','AARTIDRUGS','AARTIIND','AAVAS','ABBOTINDIA','ADANIENSOL','ADANIENT','ADANIGREEN','ADANIPORTS','ADANIPOWER','ATGL','AWL','ABCAPITAL','ABFRL','AEGISCHEM','AETHER','AFFLE','AJANTPHARM','APLLTD','ALKEM','ALKYLAMINE','ALLCARGO','ALOKINDS','ARE&M','AMBER','AMBUJACEM','ANGELONE','ANURAS','APARINDS','APOLLOHOSP','APOLLOTYRE','APTUS','ACI','ASAHIINDIA','ASHOKLEY','ASIANPAINT','ASTERDM','ASTRAL','ATUL','AUROPHARMA','AVANTIFEED','DMART','AXISBANK','BEML','BLS','BSE','BAJAJ-AUTO','BAJFINANCE','BAJAJFINSV','BAJAJHLDNG','BALAMINES','BALKRISIND','BALRAMCHIN','BANDHANBNK','BANKBARODA','BANKINDIA','MAHABANK','BATAINDIA','BAYERCROP','BERGEPAINT','BDL','BEL','BHARATFORG','BHEL','BPCL','BHARTIARTL','BIKAJI','BIOCON','BIRLACORPN','BSOFT','BLUEDART','BLUESTARCO','BBTC','BORORENEW','BOSCHLTD','BRIGADE','BCG','BRITANNIA','MAPMYINDIA','CCL','CESC','CGPOWER','CIEINDIA','CRISIL','CSBBANK','CAMPUS','CANFINHOME','CANBK','CGCL','CARBORUNIV','CASTROLIND','CEATLTD','CENTRALBK','CDSL','CENTURYPLY','CENTURYTEX','CERA','CHALET','CHAMBLFERT','CHEMPLASTS','CHOLAHLDNG','CHOLAFIN','CIPLA','CUB','CLEAN','COALINDIA','COCHINSHIP','COFORGE','COLPAL','CAMS','CONCORDBIO','CONCOR','COROMANDEL','CRAFTSMAN','CREDITACC','CROMPTON','CUMMINSIND','CYIENT','DCMSHRIRAM','DLF','DABUR','DALBHARAT','DATAPATTNS','DEEPAKFERT','DEEPAKNTR','DELHIVERY','DELTACORP','DEVYANI','DIVISLAB','DIXON','LALPATHLAB','DRREDDY','EIDPARRY','EIHOTEL','EPL','EASEMYTRIP','EICHERMOT','ELGIEQUIP','EMAMILTD','ENDURANCE','ENGINERSIN','EPIGRAL','EQUITASBNK','ERIS','ESCORTS','EXIDEIND','FDC','NYKAA','FEDERALBNK','FACT','FINEORG','FINCABLES','FINPIPE','FSL','FIVESTAR','FORTIS','GRINFRA','GAIL','GMMPFAUDLR','GMRINFRA','GALAXYSURF','GICRE','GILLETTE','GLAND','GLAXO','GLS','GLENMARK','MEDANTA','GOCOLORS','GPIL','GODFRYPHLP','GODREJCP','GODREJIND','GODREJPROP','GRANULES','GRAPHITE','GRASIM','GESHIP','GRINDWELL','GUJALKALI','GAEL','FLUOROCHEM','GUJGASLTD','GNFC','GPPL','GSFC','GSPL','HEG','HCLTECH','HDFCAMC','HDFCBANK','HDFCLIFE','HFCL','HLEGLAS','HAPPSTMNDS','HAVELLS','HEROMOTOCO','HINDALCO','HAL','HINDCOPPER','HINDPETRO','HINDUNILVR','HINDZINC','POWERINDIA','HOMEFIRST','HONAUT','HUDCO','ICICIBANK','ICICIGI','ICICIPRULI','ISEC','IDBI','IDFCFIRSTB','IDFC','IIFL','IRB','IRCON','ITC','ITI','INDIACEM','IBULHSGFIN','INDIAMART','INDIANB','IEX','INDHOTEL','IOC','IOB','IRCTC','IRFC','INDIGOPNTS','IGL','INDUSTOWER','INDUSINDBK','INFIBEAM','NAUKRI','INFY','INGERRAND','INTELLECT','INDIGO','IPCALAB','JBCHEPHARM','JKCEMENT','JBMA','JKLAKSHMI','JKPAPER','JMFINANCIL','JSWENERGY','JSWSTEEL','JAMNAAUTO','JINDALSAW','JSL','JINDALSTEL','JUBLFOOD','JUBLINGREA','JUBLPHARMA','JUSTDIAL','JYOTHYLAB','KPRMILL','KEI','KNRCON','KPITTECH','KRBL','KSB','KAJARIACER','KPIL','KALYANKJIL','KANSAINER','KARURVYSYA','KAYNES','KEC','KFINTECH','KOTAKBANK','KIMS','L&TFH','LTTS','LICHSGFIN','LTIM','LAXMIMACH','LT','LATENTVIEW','LAURUSLABS','LXCHEM','LEMONTREE','LICI','LINDEINDIA','LUPIN','LUXIND','MMTC','MRF','MTARTECH','LODHA','MGL','M&MFIN','M&M','MHRIL','MAHLIFE','MANAPPURAM','MRPL','MANKIND','MARICO','MARUTI','MASTEK','MFSL','MAXHEALTH','MAZDOCK','MEDPLUS','METROBRAND','METROPOLIS','MINDACORP','MSUMI','MOTILALOFS','MCX','MUTHOOTFIN','NATCOPHARM','NBCC','NCC','NHPC','NLCINDIA','NMDC','NSLNISP','NTPC','NH','NATIONALUM','NAVINFLUOR','NAZARA','NESTLEIND','NETWORK18','NAM-INDIA','NUVOCO','OBEROIRLTY','ONGC','OIL','OLECTRA','PAYTM','OFSS','ORIENTELEC','POLICYBZR','PCBL','PIIND','PNBHOUSING','PNCINFRA','PVRINOX','PAGEIND','PATANJALI','PERSISTENT','PETRONET','PFIZER','PHOENIXLTD','PIDILITIND','PEL','PPLPHARMA','POLYMED','POLYCAB','POLYPLEX','POONAWALLA','PFC','POWERGRID','PRAJIND','PRESTIGE','PRINCEPIPE','PRSMJOHNSN','PGHL','PGHH','PNB','QUESS','RBLBANK','RECLTD','RHIM','RITES','RADICO','RVNL','RAIN','RAINBOW','RAJESHEXPO','RALLIS','RCF','RATNAMANI','RTNINDIA','RAYMOND','REDINGTON','RELAXO','RELIANCE','RBA','ROSSARI','ROUTE','SBICARD','SBILIFE','SJVN','SKFINDIA','SRF','SAFARI','MOTHERSON','SANOFI','SAPPHIRE','SAREGAMA','SCHAEFFLER','SHARDACROP','SFL','SHOPERSTOP','SHREECEM','RENUKA','SHRIRAMFIN','SHYAMMETL','SIEMENS','SOBHA','SOLARINDS','SONACOMS','SONATSOFTW','STARHEALTH','SBIN','SAIL','SWSOLAR','STLTECH','SUMICHEM','SPARC','SUNPHARMA','SUNTV','SUNDARMFIN','SUNDRMFAST','SUNTECK','SUPRAJIT','SUPREMEIND','SUVENPHAR','SUZLON','SWANENERGY','SYMPHONY','SYNGENE','SYRMA','TTKPRESTIG','TV18BRDCST','TVSMOTOR','TANLA','TATACHEM','TATACOMM','TCS','TATACONSUM','TATAELXSI','TATAINVEST','TATAMTRDVR','TATAMOTORS','TATAPOWER','TATASTEEL','TTML','TEAMLEASE','TECHM','TEJASNET','NIACL','RAMCOCEM','THERMAX','TIMKEN','TITAN','TORNTPHARM','TORNTPOWER','TRENT','TRIDENT','TRIVENI','TRITURBINE','TIINDIA','UCOBANK','UNOMINDA','UPL','UTIAMC','UJJIVANSFB','ULTRACEMCO','UNIONBANK','UBL','MCDOWELL-N','USHAMART','VGUARD','VMART','VIPIND','VAIBHAVGBL','VTL','VARROC','VBL','MANYAVAR','VEDL','VIJAYA','VINATIORGA','IDEA','VOLTAS','WELCORP','WELSPUNLIV','WESTLIFE','WHIRLPOOL','WIPRO','YESBANK','ZFCVINDIA','ZEEL','ZENSARTECH','ZOMATO','ZYDUSLIFE','ZYDUSWELL','ECLERX']
#         data_to_string = st.text_input("Enter data_to (2024-03-7 09:15:00.0):") #YYYY-MM-DD HH:MM:SS.%f
#
#         if st.button("Get Data"):
#             combined_dataframe = pd.DataFrame()  # Initialize an empty DataFrame to store combined data
#
#             for symbol in symbols:
#                 obj = MControlAPI(symbol, data_to=data_to_string)
#                 nd = 0
#                 while nd > -1:
#                     nd = obj.fetch_intraday_data()
#                     if nd > 0:
#                         obj.dataframe['symbol'] = symbol  # Add symbol column
#                         combined_dataframe = pd.concat([combined_dataframe, obj.dataframe], ignore_index=True)  # Concatenate dataframes
#                     break  # Breaking out of the loop after fetching data for one symbol
#
#             # Move 'symbol' column to the first position
#             cols = combined_dataframe.columns.tolist()
#             cols = ['symbol'] + [col for col in cols if col != 'symbol']
#             combined_dataframe = combined_dataframe[cols]
#
#             # Display combined_dataframe
#             st.write(combined_dataframe[['symbol', 'c', 'v', 'dt']])
#             st.download_button("Download CSV File",
#                                combined_dataframe.to_csv(index=False),
#                                file_name='Result.csv',
#                                mime='text/csv'
#                                )
#             st.balloons()
#
#     else:
#         st.text("Please enter the password to continue.")
#
# if __name__ == '__main__':
#     main()


# import streamlit as st
# import requests
# from datetime import datetime, timedelta
# import pandas as pd
#
# class MControlAPI:
#     def __init__(self, symbol, resolution=1, data_from=None, data_to=None):
#         self.symbol = symbol
#         self.resolution = resolution
#         if data_to is not None:
#             self.data_to = datetime.strptime(data_to, '%Y-%m-%d %H:%M:%S.%f')
#         else:
#             # Default value if user doesn't provide data_to
#             self.data_to = datetime.now()  # Assuming you want current datetime if data_to is not provided
#         self.data_to_str = self.data_to.strftime('%Y-%m-%d %H:%M:%S.%f')
#         self.data_to_timestamp = int(self.data_to.timestamp())
#         self.resolution_dt = {
#             '1': 60, '3': 180, '5': 300, '15': 900, '30': 1800,
#             '60': 3600, '300': 18000, 'D': 24*3600, 'W': 7*24*3600,
#             'M': 30*24*3600, '45': 45*24*3600, '120': 120*24*3600, '240': 240*24*3600
#         }
#         self.delta_time = self.resolution_dt[str(self.resolution)]
#         if data_from is None:
#             self.data_from = self.data_to - timedelta(seconds=self.delta_time * 1)
#         else:
#             self.data_from = data_from
#
#         self.session = requests.sessions.Session()
#         self.session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
#         self.session.get('https://www.moneycontrol.com/stocksmarketsindia/')
#         self.symbol_meta = None
#         self.dataframe = []
#
#     def fetch_symbol_meta(self):
#         if self.symbol_meta is None:
#             self.symbol_meta = self.session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/symbol?symbol=' + self.symbol)
#         return self.symbol_meta
#
#     def fetch_intraday_data(self, countback=None):
#         new_data = 0
#         try:
#             if countback is None:
#                 countback = int((self.data_to_timestamp - self.data_from.timestamp()) / self.delta_time)
#                 if countback > 376:
#                     countback = 376
#
#             resp = self.session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?' +
#                                     'symbol={0}&resolution={1}&from={2}&to={3}&countback={4}'.format(
#                                         self.symbol, self.resolution, self.data_from.timestamp(), self.data_to_timestamp, countback))
#             data = resp.json()
#             if data['s'] == 'no_data':
#                 return -1
#
#             df = pd.DataFrame.from_dict(data)
#             df['dt'] = pd.to_datetime(df['t'] + 19800, unit='s')
#
#             n = len(self.dataframe)
#
#             if n == 0:
#                 self.dataframe = df.copy()
#                 new_data = len(self.dataframe)
#
#             else:
#                 df = pd.concat([self.dataframe, df[df['t'].isin(self.dataframe['t']) == False]]).reset_index(drop=True)
#                 self.dataframe = df.copy()
#                 new_data = len(self.dataframe) - n
#
#             self.data_from = self.data_to
#             self.data_to += timedelta(seconds=self.delta_time)
#
#         except Exception as ex:
#             new_data = -1
#             st.error(ex)
#
#         return new_data
#
# def main():
#     st.title("Welcome! Data Analysis World...")
#     entered_password = st.text_input("Enter Password:", type="password")
#
#     if entered_password == "///":
#         st.success("Access granted! You are now logged in.")
#
#
#         st.title("MControlAPI Data Fetcher")
#         symbols = ['360ONE','3MINDIA','ABB','ACC','AIAENG','APLAPOLLO','AUBANK','AARTIDRUGS','AARTIIND','AAVAS','ABBOTINDIA','ADANIENSOL','ADANIENT','ADANIGREEN','ADANIPORTS']
#         data_to_string = st.text_input("Enter data_to (2024-03-7 09:15:00.0):") #YYYY-MM-DD HH:MM:SS.%f
#
#         if st.button("Get Data"):
#             combined_dataframe = pd.DataFrame()  # Initialize an empty DataFrame to store combined data
#
#             for symbol in symbols:
#                 obj = MControlAPI(symbol, data_to=data_to_string)
#                 nd = 0
#                 while nd > -1:
#                     nd = obj.fetch_intraday_data()
#                     if nd > 0:
#                         obj.dataframe['symbol'] = symbol  # Add symbol column
#                         combined_dataframe = pd.concat([combined_dataframe, obj.dataframe], ignore_index=True)  # Concatenate dataframes
#                     break  # Breaking out of the loop after fetching data for one symbol
#
#             # Move 'symbol' column to the first position
#             cols = combined_dataframe.columns.tolist()
#             cols = ['symbol'] + [col for col in cols if col != 'symbol']
#             combined_dataframe = combined_dataframe[cols]
#
#             # Display combined_dataframe
#             st.write(combined_dataframe)  #combined_dataframe[['symbol', 'c', 'v', 'dt']]
#             st.download_button("Download CSV File",
#                                combined_dataframe.to_csv(index=False),
#                                file_name='Result.csv',
#                                mime='text/csv'
#                                )
#             st.balloons()
#
#     else:
#         st.text("Please enter the password to continue.")
#
# if __name__ == '__main__':
#     main()


# import pandas as pd
# import streamlit as st
# import requests
# from datetime import datetime, timedelta
# import multiprocessing
#
# class MControlAPI:
#     def __init__(self, symbol, resolution=1, data_from=None, data_to=None):
#         self.symbol = symbol
#         self.resolution = resolution
#         if data_to is not None:
#             self.data_to = datetime.strptime(data_to, '%Y-%m-%d %H:%M:%S.%f')
#         else:
#             self.data_to = datetime.now()
#         self.data_to_str = self.data_to.strftime('%Y-%m-%d %H:%M:%S.%f')
#         self.data_to_timestamp = int(self.data_to.timestamp())
#         self.resolution_dt = {
#             '1': 60, '3': 180, '5': 300, '15': 900, '30': 1800,
#             '60': 3600, '300': 18000, 'D': 24*3600, 'W': 7*24*3600,
#             'M': 30*24*3600, '45': 45*24*3600, '120': 120*24*3600, '240': 240*24*3600
#         }
#         self.delta_time = self.resolution_dt[str(self.resolution)]
#         if data_from is None:
#             self.data_from = self.data_to - timedelta(seconds=self.delta_time * 1)
#         else:
#             self.data_from = data_from
#
#         self.session = requests.sessions.Session()
#         self.session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
#         self.session.get('https://www.moneycontrol.com/stocksmarketsindia/')
#         self.symbol_meta = None
#         self.dataframe = []
#
#     def fetch_symbol_meta(self):
#         if self.symbol_meta is None:
#             self.symbol_meta = self.session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/symbol?symbol=' + self.symbol)
#         return self.symbol_meta
#
#     def fetch_intraday_data(self, countback=None):
#         new_data = 0
#         try:
#             if countback is None:
#                 countback = int((self.data_to_timestamp - self.data_from.timestamp()) / self.delta_time)
#                 if countback > 376:
#                     countback = 376
#
#             resp = self.session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?' +
#                                     'symbol={0}&resolution={1}&from={2}&to={3}&countback={4}'.format(
#                                         self.symbol, self.resolution, self.data_from.timestamp(), self.data_to_timestamp, countback))
#             data = resp.json()
#             if data['s'] == 'no_data':
#                 return -1
#
#             df = pd.DataFrame.from_dict(data)
#             df['dt'] = pd.to_datetime(df['t'] + 19800, unit='s')
#
#             n = len(self.dataframe)
#
#             if n == 0:
#                 self.dataframe = df.copy()
#                 new_data = len(self.dataframe)
#
#             else:
#                 df = pd.concat([self.dataframe, df[df['t'].isin(self.dataframe['t']) == False]]).reset_index(drop=True)
#                 self.dataframe = df.copy()
#                 new_data = len(self.dataframe) - n
#
#             self.data_from = self.data_to
#             self.data_to += timedelta(seconds=self.delta_time)
#
#         except Exception as ex:
#             new_data = -1
#             st.error(ex)
#
#         return new_data
#
# def process_symbol(symbol, data_to_string, dataframes):
#     obj = MControlAPI(symbol, data_to=data_to_string)
#     nd = 0
#     while nd > -1:
#         nd = obj.fetch_intraday_data()
#         if nd > 0:
#             obj.dataframe['symbol'] = symbol
#             dataframes.append(obj.dataframe)
#
# def main():
#     st.title("Welcome! Data Analysis World...")
#     entered_password = st.text_input("Enter Password:", type="password")
#
#     if entered_password == "///":
#         st.success("Access granted! You are now logged in.")
#
#         st.title("MControlAPI Data Fetcher")
#         symbols = ['360ONE','3MINDIA','ABB','ACC','AIAENG','APLAPOLLO','AUBANK','AARTIDRUGS','AARTIIND','AAVAS','ABBOTINDIA','ADANIENSOL','ADANIENT','ADANIGREEN','ADANIPORTS','ADANIPOWER','ATGL','AWL','ABCAPITAL','ABFRL','AEGISCHEM','AETHER','AFFLE','AJANTPHARM','APLLTD']
#
#         data_to_string = st.text_input("Enter data_to (2024-03-07 09:15:00.0):")
#
#         if st.button("Get Data"):
#             manager = multiprocessing.Manager()
#             dataframes = manager.list()  # Shared list to store dataframes
#
#             processes = []
#             for symbol in symbols:
#                 p = multiprocessing.Process(target=process_symbol, args=(symbol, data_to_string, dataframes))
#                 p.start()
#                 processes.append(p)
#
#             for p in processes:
#                 p.join()
#
#             # Concatenate dataframes obtained from each process
#             combined_dataframe = pd.concat(dataframes, ignore_index=True)
#
#             st.write(combined_dataframe)
#             st.balloons()
#
#     else:
#         st.text("Please enter the password to continue.")
#
# if __name__ == '__main__':
#     main()

# Final-2
# import pandas as pd
# import streamlit as st
# import requests
# from datetime import datetime, timedelta
# import concurrent.futures
#
#
# class MControlAPI:
#     def __init__(self, symbol, resolution=1, data_from=None, data_to=None):
#         self.symbol = symbol
#         self.resolution = resolution
#         self.data_to = datetime.now() if data_to is None else datetime.strptime(data_to, '%Y-%m-%d %H:%M:%S.%f')
#         self.data_to_str = self.data_to.strftime('%Y-%m-%d %H:%M:%S.%f')
#         self.data_to_timestamp = int(self.data_to.timestamp())
#         self.resolution_dt = {
#             '1': 60, '3': 180, '5': 300, '15': 900, '30': 1800,
#             '60': 3600, '300': 18000, 'D': 24 * 3600, 'W': 7 * 24 * 3600,
#             'M': 30 * 24 * 3600, '45': 45 * 24 * 3600, '120': 120 * 24 * 3600, '240': 240 * 24 * 3600
#         }
#         self.delta_time = self.resolution_dt.get(str(self.resolution), 60)
#         self.data_from = data_from if data_from else self.data_to - timedelta(seconds=self.delta_time * 1)
#         self.session = requests.sessions.Session()
#         self.session.headers[
#             'User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
#         self.session.get('https://www.moneycontrol.com/stocksmarketsindia/')
#         self.symbol_meta = None
#         self.dataframe = pd.DataFrame()
#
#     def fetch_symbol_meta(self):
#         if not self.symbol_meta:
#             self.symbol_meta = self.session.get(
#                 f'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/symbol?symbol={self.symbol}')
#         return self.symbol_meta
#
#     def fetch_intraday_data(self, countback=None):
#         try:
#             if countback is None:
#                 countback = min(int((self.data_to_timestamp - self.data_from.timestamp()) / self.delta_time), 376)
#
#             resp = self.session.get(
#                 f'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol={self.symbol}&resolution={self.resolution}&from={self.data_from.timestamp()}&to={self.data_to_timestamp}&countback={countback}')
#             data = resp.json()
#             if data['s'] == 'no_data':
#                 return pd.DataFrame()
#
#             df = pd.DataFrame.from_dict(data)
#             df['dt'] = pd.to_datetime(df['t'] + 19800, unit='s')
#             return df
#
#         except Exception as ex:
#             st.error(ex)
#             return pd.DataFrame()
#
#
# def process_symbol(symbol, data_to_string):
#     obj = MControlAPI(symbol, data_to=data_to_string)
#     return obj.fetch_intraday_data()
#
#
# def main():
#     st.title("Welcome! Data Analysis World...")
#     entered_password = st.text_input("Enter Password:", type="password")
#
#     if entered_password == "///":
#         st.success("Access granted! You are now logged in.")
#
#         st.title("MControlAPI Data Fetcher")
#         symbols = ['360ONE','3MINDIA','ABB','ACC','AIAENG','APLAPOLLO','AUBANK','AARTIDRUGS','AARTIIND','AAVAS','ABBOTINDIA','ADANIENSOL','ADANIENT','ADANIGREEN','ADANIPORTS','ADANIPOWER','ATGL','AWL','ABCAPITAL','ABFRL','AEGISCHEM','AETHER','AFFLE','AJANTPHARM','APLLTD','ALKEM','ALKYLAMINE','ALLCARGO','ALOKINDS','ARE&M','AMBER','AMBUJACEM','ANGELONE','ANURAS','APARINDS','APOLLOHOSP','APOLLOTYRE','APTUS','ACI','ASAHIINDIA','ASHOKLEY','ASIANPAINT','ASTERDM','ASTRAL','ATUL','AUROPHARMA','AVANTIFEED','DMART','AXISBANK','BEML','BLS','BSE','BAJAJ-AUTO','BAJFINANCE','BAJAJFINSV','BAJAJHLDNG','BALAMINES','BALKRISIND','BALRAMCHIN','BANDHANBNK','BANKBARODA','BANKINDIA','MAHABANK','BATAINDIA','BAYERCROP','BERGEPAINT','BDL','BEL','BHARATFORG','BHEL','BPCL','BHARTIARTL','BIKAJI','BIOCON','BIRLACORPN','BSOFT','BLUEDART','BLUESTARCO','BBTC','BORORENEW','BOSCHLTD','BRIGADE','BCG','BRITANNIA','MAPMYINDIA','CCL','CESC','CGPOWER','CIEINDIA','CRISIL','CSBBANK','CAMPUS','CANFINHOME','CANBK','CGCL','CARBORUNIV','CASTROLIND','CEATLTD','CENTRALBK','CDSL','CENTURYPLY','CENTURYTEX','CERA','CHALET','CHAMBLFERT','CHEMPLASTS','CHOLAHLDNG','CHOLAFIN','CIPLA','CUB','CLEAN','COALINDIA','COCHINSHIP','COFORGE','COLPAL','CAMS','CONCORDBIO','CONCOR','COROMANDEL','CRAFTSMAN','CREDITACC','CROMPTON','CUMMINSIND','CYIENT','DCMSHRIRAM','DLF','DABUR','DALBHARAT','DATAPATTNS','DEEPAKFERT','DEEPAKNTR','DELHIVERY','DELTACORP','DEVYANI','DIVISLAB','DIXON','LALPATHLAB','DRREDDY','EIDPARRY','EIHOTEL','EPL','EASEMYTRIP','EICHERMOT','ELGIEQUIP','EMAMILTD','ENDURANCE','ENGINERSIN','EPIGRAL','EQUITASBNK','ERIS','ESCORTS','EXIDEIND','FDC','NYKAA','FEDERALBNK','FACT','FINEORG','FINCABLES','FINPIPE','FSL','FIVESTAR','FORTIS','GRINFRA','GAIL','GMMPFAUDLR','GMRINFRA','GALAXYSURF','GICRE','GILLETTE','GLAND','GLAXO','GLS','GLENMARK','MEDANTA','GOCOLORS','GPIL','GODFRYPHLP','GODREJCP','GODREJIND','GODREJPROP']
#
#         data_to_string = st.text_input("Enter data_to (2024-03-07 09:15:00.0):")
#
#         if st.button("Get Data"):
#             dataframes = []
#             with concurrent.futures.ThreadPoolExecutor() as executor:
#                 results = [executor.submit(process_symbol, symbol, data_to_string) for symbol in symbols]
#                 for result in concurrent.futures.as_completed(results):
#                     df = result.result()
#                     if not df.empty:
#                         dataframes.append(df)
#
#             if dataframes:
#                 combined_dataframe = pd.concat(dataframes, ignore_index=True)
#                 st.write(combined_dataframe)
#                 st.balloons()
#             else:
#                 st.warning("No data available for the selected symbols.")
#
#     else:
#         st.text("Please enter the password to continue.")
#
#
# if __name__ == '__main__':
#     main()


# Final-3

import pandas as pd
import streamlit as st
import requests
from datetime import datetime, timedelta
import concurrent.futures


class MControlAPI:
    def __init__(self, symbol, resolution=1, data_from=None, data_to=None):
        self.symbol = symbol
        self.resolution = resolution
        self.data_to = datetime.now() if data_to is None else datetime.strptime(data_to, '%Y-%m-%d %H:%M:%S.%f')
        self.data_to_str = self.data_to.strftime('%Y-%m-%d %H:%M:%S.%f')
        self.data_to_timestamp = int(self.data_to.timestamp())
        self.resolution_dt = {
            '1': 60, '3': 180, '5': 300, '15': 900, '30': 1800,
            '60': 3600, '300': 18000, 'D': 24 * 3600, 'W': 7 * 24 * 3600,
            'M': 30 * 24 * 3600, '45': 45 * 24 * 3600, '120': 120 * 24 * 3600, '240': 240 * 24 * 3600
        }
        self.delta_time = self.resolution_dt.get(str(self.resolution), 60)
        self.data_from = data_from if data_from else self.data_to - timedelta(seconds=self.delta_time * 1)
        self.session = requests.sessions.Session()
        self.session.headers[
            'User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
        self.session.get('https://www.moneycontrol.com/stocksmarketsindia/')
        self.symbol_meta = None
        self.dataframe = pd.DataFrame()

    def fetch_symbol_meta(self):
        if not self.symbol_meta:
            self.symbol_meta = self.session.get(
                f'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/symbol?symbol={self.symbol}')
        return self.symbol_meta

    def fetch_intraday_data(self, countback=None):
        try:
            if countback is None:
                countback = min(int((self.data_to_timestamp - self.data_from.timestamp()) / self.delta_time), 376)

            resp = self.session.get(
                f'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol={self.symbol}&resolution={self.resolution}&from={self.data_from.timestamp()}&to={self.data_to_timestamp}&countback={countback}')
            data = resp.json()
            if data['s'] == 'no_data':
                return pd.DataFrame()

            df = pd.DataFrame.from_dict(data)
            df['dt'] = pd.to_datetime(df['t'] + 19800, unit='s')
            df['symbol'] = self.symbol  # Adding symbols column
            return df

        except Exception as ex:
            st.error(ex)
            return pd.DataFrame()


def process_symbol(symbol, data_to_string):
    obj = MControlAPI(symbol, data_to=data_to_string)
    return obj.fetch_intraday_data()


def main():
    st.title("Welcome! Data Analysis World...")
    entered_password = st.text_input("Enter Password:", type="password")

    if entered_password == "///":
        st.success("Access granted! You are now logged in.")

        st.title("MControlAPI Data Fetcher")
        symbols = ['360ONE','3MINDIA','ABB','ACC','AIAENG','APLAPOLLO','AUBANK','AARTIDRUGS','AARTIIND','AAVAS','ABBOTINDIA','ADANIENSOL','ADANIENT','ADANIGREEN','ADANIPORTS','ADANIPOWER','ATGL','AWL','ABCAPITAL','ABFRL','AEGISCHEM','AETHER','AFFLE','AJANTPHARM','APLLTD','ALKEM','ALKYLAMINE','ALLCARGO','ALOKINDS','ARE&M','AMBER','AMBUJACEM','ANGELONE','ANURAS','APARINDS','APOLLOHOSP','APOLLOTYRE','APTUS','ACI','ASAHIINDIA','ASHOKLEY','ASIANPAINT','ASTERDM','ASTRAL','ATUL','AUROPHARMA','AVANTIFEED','DMART','AXISBANK','BEML','BLS','BSE','BAJAJ-AUTO','BAJFINANCE','BAJAJFINSV','BAJAJHLDNG','BALAMINES','BALKRISIND','BALRAMCHIN','BANDHANBNK','BANKBARODA','BANKINDIA','MAHABANK','BATAINDIA','BAYERCROP','BERGEPAINT','BDL','BEL','BHARATFORG','BHEL','BPCL','BHARTIARTL','BIKAJI','BIOCON','BIRLACORPN','BSOFT','BLUEDART','BLUESTARCO','BBTC','BORORENEW','BOSCHLTD','BRIGADE','BCG','BRITANNIA','MAPMYINDIA','CCL','CESC','CGPOWER','CIEINDIA','CRISIL','CSBBANK','CAMPUS','CANFINHOME','CANBK','CGCL','CARBORUNIV','CASTROLIND','CEATLTD','CENTRALBK','CDSL','CENTURYPLY','CENTURYTEX','CERA','CHALET','CHAMBLFERT','CHEMPLASTS','CHOLAHLDNG','CHOLAFIN','CIPLA','CUB','CLEAN','COALINDIA','COCHINSHIP','COFORGE','COLPAL','CAMS','CONCORDBIO','CONCOR','COROMANDEL','CRAFTSMAN','CREDITACC','CROMPTON','CUMMINSIND','CYIENT','DCMSHRIRAM','DLF','DABUR','DALBHARAT','DATAPATTNS','DEEPAKFERT','DEEPAKNTR','DELHIVERY','DELTACORP','DEVYANI','DIVISLAB','DIXON','LALPATHLAB','DRREDDY','EIDPARRY','EIHOTEL','EPL','EASEMYTRIP','EICHERMOT','ELGIEQUIP','EMAMILTD','ENDURANCE','ENGINERSIN','EPIGRAL','EQUITASBNK','ERIS','ESCORTS','EXIDEIND','FDC','NYKAA','FEDERALBNK','FACT','FINEORG','FINCABLES','FINPIPE','FSL','FIVESTAR','FORTIS','GRINFRA','GAIL','GMMPFAUDLR','GMRINFRA','GALAXYSURF','GICRE','GILLETTE','GLAND','GLAXO','GLS','GLENMARK','MEDANTA','GOCOLORS','GPIL','GODFRYPHLP','GODREJCP','GODREJIND','GODREJPROP','GRANULES','GRAPHITE','GRASIM','GESHIP','GRINDWELL','GUJALKALI','GAEL','FLUOROCHEM','GUJGASLTD','GNFC','GPPL','GSFC','GSPL','HEG','HCLTECH','HDFCAMC','HDFCBANK','HDFCLIFE','HFCL','HLEGLAS','HAPPSTMNDS','HAVELLS','HEROMOTOCO','HINDALCO','HAL','HINDCOPPER','HINDPETRO','HINDUNILVR','HINDZINC','POWERINDIA','HOMEFIRST','HONAUT','HUDCO','ICICIBANK','ICICIGI','ICICIPRULI','ISEC','IDBI','IDFCFIRSTB','IDFC','IIFL','IRB','IRCON','ITC','ITI','INDIACEM','IBULHSGFIN','INDIAMART','INDIANB','IEX','INDHOTEL','IOC','IOB','IRCTC','IRFC','INDIGOPNTS','IGL','INDUSTOWER','INDUSINDBK','INFIBEAM','NAUKRI','INFY','INGERRAND','INTELLECT','INDIGO','IPCALAB','JBCHEPHARM','JKCEMENT','JBMA','JKLAKSHMI','JKPAPER','JMFINANCIL','JSWENERGY','JSWSTEEL','JAMNAAUTO','JINDALSAW','JSL','JINDALSTEL','JUBLFOOD','JUBLINGREA','JUBLPHARMA','JUSTDIAL','JYOTHYLAB','KPRMILL','KEI','KNRCON','KPITTECH','KRBL','KSB','KAJARIACER','KPIL','KALYANKJIL','KANSAINER','KARURVYSYA','KAYNES','KEC','KFINTECH','KOTAKBANK','KIMS','L&TFH','LTTS','LICHSGFIN','LTIM','LAXMIMACH','LT','LATENTVIEW','LAURUSLABS','LXCHEM','LEMONTREE','LICI','LINDEINDIA','LUPIN','LUXIND','MMTC','MRF','MTARTECH','LODHA','MGL','M&MFIN','M&M','MHRIL','MAHLIFE','MANAPPURAM','MRPL','MANKIND','MARICO','MARUTI','MASTEK','MFSL','MAXHEALTH','MAZDOCK','MEDPLUS','METROBRAND','METROPOLIS','MINDACORP','MSUMI','MOTILALOFS','MCX','MUTHOOTFIN','NATCOPHARM','NBCC','NCC','NHPC','NLCINDIA','NMDC','NSLNISP','NTPC','NH','NATIONALUM','NAVINFLUOR','NAZARA','NESTLEIND','NETWORK18','NAM-INDIA','NUVOCO','OBEROIRLTY','ONGC','OIL','OLECTRA','PAYTM','OFSS','ORIENTELEC','POLICYBZR','PCBL','PIIND','PNBHOUSING','PNCINFRA','PVRINOX','PAGEIND','PATANJALI','PERSISTENT','PETRONET','PFIZER','PHOENIXLTD','PIDILITIND','PEL','PPLPHARMA','POLYMED','POLYCAB','POLYPLEX','POONAWALLA','PFC','POWERGRID','PRAJIND','PRESTIGE','PRINCEPIPE','PRSMJOHNSN','PGHL','PGHH','PNB','QUESS','RBLBANK','RECLTD','RHIM','RITES','RADICO','RVNL','RAIN','RAINBOW','RAJESHEXPO','RALLIS','RCF','RATNAMANI','RTNINDIA','RAYMOND','REDINGTON','RELAXO','RELIANCE','RBA','ROSSARI','ROUTE','SBICARD','SBILIFE','SJVN','SKFINDIA','SRF','SAFARI','MOTHERSON','SANOFI','SAPPHIRE','SAREGAMA','SCHAEFFLER','SHARDACROP','SFL','SHOPERSTOP','SHREECEM','RENUKA','SHRIRAMFIN','SHYAMMETL','SIEMENS','SOBHA','SOLARINDS','SONACOMS','SONATSOFTW','STARHEALTH','SBIN','SAIL','SWSOLAR','STLTECH','SUMICHEM','SPARC','SUNPHARMA','SUNTV','SUNDARMFIN','SUNDRMFAST','SUNTECK','SUPRAJIT','SUPREMEIND','SUVENPHAR','SUZLON','SWANENERGY','SYMPHONY','SYNGENE','SYRMA','TTKPRESTIG','TV18BRDCST','TVSMOTOR','TANLA','TATACHEM','TATACOMM','TCS','TATACONSUM','TATAELXSI','TATAINVEST','TATAMTRDVR','TATAMOTORS','TATAPOWER','TATASTEEL','TTML','TEAMLEASE','TECHM','TEJASNET','NIACL','RAMCOCEM','THERMAX','TIMKEN','TITAN','TORNTPHARM','TORNTPOWER','TRENT','TRIDENT','TRIVENI','TRITURBINE','TIINDIA','UCOBANK','UNOMINDA','UPL','UTIAMC','UJJIVANSFB','ULTRACEMCO','UNIONBANK','UBL','MCDOWELL-N','USHAMART','VGUARD','VMART','VIPIND','VAIBHAVGBL','VTL','VARROC','VBL','MANYAVAR','VEDL','VIJAYA','VINATIORGA','IDEA','VOLTAS','WELCORP','WELSPUNLIV','WESTLIFE','WHIRLPOOL','WIPRO','YESBANK','ZFCVINDIA','ZEEL','ZENSARTECH','ZOMATO','ZYDUSLIFE','ZYDUSWELL','ECLERX']

        data_to_string = st.text_input("Enter data_to (2024-03-07 09:15:00.0):")

        if st.button("Get Data"):
            dataframes = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = [executor.submit(process_symbol, symbol, data_to_string) for symbol in symbols]
                for result in concurrent.futures.as_completed(results):
                    df = result.result()
                    if not df.empty:
                        dataframes.append(df)

            if dataframes:
                combined_dataframe = pd.concat(dataframes, ignore_index=True)
                combined_dataframe = combined_dataframe[
                    ['symbol'] + [col for col in combined_dataframe if col != 'symbol']]  # Reordering columns
                p= combined_dataframe[['symbol', 'c', 'v', 'dt']]
                st.write(p)
                st.download_button("Download CSV File",p.to_csv(index=False),
                                                       file_name='Result.csv',
                                                        mime='text/csv'
                                                        )
                st.balloons()
            else:
                st.warning("No data available for the selected symbols.")

    else:
        st.text("Please enter the password to continue.")


if __name__ == '__main__':
    main()
