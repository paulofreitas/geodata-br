
# dtb-ibge

Brazilian territorial distribution data. Updated. Always.

### Data source

All these data was compiled from XLS spreadsheets provided by IBGE through its FTP server. You can download them at `ftp://geoftp.ibge.gov.br/organizacao_territorial/divisao_territorial/`.

### Database records

| Table          | 2013   | 2012   | 2011   | 2010   | 2009   | 2008   | 2007   | 2006   |
| --------------:| ------:| ------:| ------:| ------:| ------:| ------:| ------:| ------:|
| `uf`           |     27 |     27 |     27 |     27 |     27 |     27 |     27 |     27 |
| `mesorregiao`  |    137 |    137 |    137 |    137 |    137 |    137 |    137 |    137 |
| `microrregiao` |    558 |    558 |    558 |    558 |    558 |    558 |    558 |    558 |
| `municipio`    |  5,570 |  5,565 |  5,565 |  5,565 |  5,565 |  5,564 |  5,564 |  5,564 |
| `distrito`     | 10,302 |      - |      - |      - | 10,155 | 10,104 | 10,090 | 10,031 |
| `subdistrito`  |    662 |      - |      - |      - |    489 |    471 |    471 |    449 |

### Database formats

Currently we provide databases into the following formats: CSV, JSON, p-list, Serialized PHP, SQL, SQLite 3, XML and YAML

### Get involved!

Report any mislead information, enhancement or feature request to [our bug tracker](https://github.com/paulofreitas/dtb-ibge/issues)!
