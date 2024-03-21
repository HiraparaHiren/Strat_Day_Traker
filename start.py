import pandas as pd
import streamlit as st
import requests
from datetime import datetime, timedelta
import streamlit.concurrent

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


@st.cache(suppress_st_warning=True)
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
            for symbol in symbols:
                dataframes.append(streamlit.concurrent.st_concurrent(process_symbol, symbol, data_to_string))

                dataframes = [result for result in dataframes if not result.empty]

            if dataframes:
                combined_dataframe = pd.concat(dataframes, ignore_index=True)
                combined_dataframe = combined_dataframe[
                    ['symbol'] + [col for col in combined_dataframe if col != 'symbol']]  # Reordering columns
                p = combined_dataframe[['symbol', 'c', 'v', 'dt']]
                st.write(p)
                st.download_button("Download CSV File", p.to_csv(index=False),
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
