from datetime import datetime
now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")

### Configuration IBAMA Julgamento de Autos de Infração

## GCP pointing ------------

# GCP project name
project = 'dev-data'

# GCP bucket name
bucket_name = 'bvs-bigdata-datalake-stage-external-cadastral-rf-dev'

# Blob path
blob_path1 = 'datalake/stage/external/cadastral/rf/data/ibama_jai/partitions/monthly/' + str(year) + '/' + str(month) + '/'
blob_path2 = 'datalake/stage/external/cadastral/rf/data/ibama_jai_log/partitions/monthly/' + str(year) + '/' + str(month) + '/'



## File Names ------------

# file name to save logging information
log_filename = "ibama_jai.log'"

# File name to save scrapped data 
filename = 'ibama_jai.json'



## Scrap definitions ------------

# Lista de estados para baixar os dados
#["AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT","PA","PB","PE","PI","PR","RJ","RN","RO","RS","SC","SE","SP","TO"]
lista_uf = ["AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT","PA","PB","PE","PI","PR","RJ","RN","RO","RS","SC","SE","SP","TO"]

# Download URL 
url='http://dadosabertos.ibama.gov.br/dados/SICAFI/AC/Volume/volumeJulgamentoAI.json'

# Headers necessarry to request the data from Processos api webpage
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'} 

# Boolean for request certification on data request
certif = True