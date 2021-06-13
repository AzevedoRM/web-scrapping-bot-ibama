import logging
import requests
import json
import time
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
from requests.exceptions import ConnectionError,HTTPError,ProxyError,SSLError
import sys
sys.path.append('/usr/src/app')

import bot_config as cfg
import gcp_connect as gcp


def download(uf):
    """ Captura os dados da pagina solicitada atraves de requests.get

    return: json data from the api request
    """
    url = 'http://dadosabertos.ibama.gov.br/dados/SICAFI/'+ uf +'/Volume/volumeJulgamentoAI.json'
    try:
        get_url = requests.get(url, headers=cfg.hdr, verify=cfg.certif)
        if get_url.status_code == 200:
            data = json.loads(get_url.text)

    except Exception as expt:
        logging.exception("Ocorreu uma exceção.")
        pass
    
    else:
        logging.info("Download finalizado. URL: {}: ".format(url))
        return data


def upload_data(data, bucket, blob_name, blob_log_name, blob_path, log=False):
    """ Carrega os dados no bucket GCP
    
    return: None
    """
    try:
        if log == False:
            blob = gcp.blob_open(bucket, blob_path, blob_name, 'w')
            json.dump(data, blob, ensure_ascii=False)
            logging.info("Arquivo salvo no BUCKET: {} e BLOB: {}".format(bucket, blob))
        else:
            blob_log = gcp.blob_create(bucket, blob_path, blob_log_name)
            blob_log.upload_from_filename('temp.log')
    
    except Exception as expt:
        logging.exception("Ocorreu uma exceção.")
        pass


if __name__ == "__main__":
    ini = time.time()

    # instancia de log
    logger = logging.basicConfig(filename='temp.log', format='%(asctime)s - %(levelname)s - %(message)s',filemode='w', level=logging.INFO)
    
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S_")

    blob_log_name = dt_string + cfg.log_filename
    
    try:
        bucket = gcp.bucket_obj(cfg.project, cfg.bucket_name)
        logging.info('Conectado com sucesso no Bucket: ' + cfg.bucket_name)
        
        try:
            # download dos dados da URL fornecida
            with ProcessPoolExecutor() as executor:
                data = [*executor.map(download, cfg.lista_uf)]

            # definicao de BLOBS
            blob_name = dt_string + cfg.filename

            # uplodad de dados para GCS
            upload_data(data, bucket, blob_name, None, cfg.blob_path1)

        except Exception as expt:
            logging.exception("Exception occurred.")
            pass
         
    except Exception as expt:
        logging.exception("Exception occurred.")
        pass

    finally:
        # uplodad de logs para GCS
        logging.info('Aplicação finalizada. Tempo de execução: ' + str(time.time()-ini) + 's')
        upload_data(None, bucket, None, blob_log_name, cfg.blob_path2, log=True)

    logging.shutdown()