import nodriver as uc
from utils.scraper import main

if __name__ == '__main__':
    ### arama (string): Arama yapılacak kelime.
    ### yıl_min (string, opsiyonel): Minimum yıl filtresi.
    ### yıl_max (string, opsiyonel): Maksimum yıl filtresi.
    ### motor_hacmi (string, opsiyonel): Motor hacmi filtresi.
    ### vites (string, opsiyonel): Vites tipi ("Manuel" veya "Otomatik").

    ## main(arama, yıl_min, yıl_max, motor_hacmi, vites)
    uc.loop().run_until_complete(main(
        arama="Renault Fluence",    
        vites="Manuel",
        yıl_min="2016",
        yıl_max="2016"
    ))
