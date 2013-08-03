# dtb-ibge

Brazilian territorial distribution data. Updated. Always.

### Data source

All these data was compiled from XLS spreadsheets provided by IBGE through its FTP server. You can download them at `ftp://geoftp.ibge.gov.br/organizacao_territorial/divisao_territorial/`.

### Raw databases

| File                    | Format         | Size      |
| ----------------------- |:--------------:| ---------:|
| `data/2013/dtb.csv`     | CSV            | 1,250,541 |
| `data/2013/dtb.json`    | JSON           | 2,785,758 |
| `data/2013/dtb.phpd`    | Serialized PHP | 2,481,458 |
| `data/2013 dtb.plist`   | p-list         | 4,969,493 |
| `data/2013/dtb.sql`     | SQL            | 1,384,309 |
| `data/2013/dtb.sqlite3` | SQLite 3       | 1,605,632 |
| `data/2013/dtb.xml`     | XML            | 4,711,274 |
| `data/2013/dtb.yaml`    | YAML           | 2,062,935 |

### Minified databases

| File                             | Format         | Size      | Savings |
| -------------------------------- |:--------------:| ---------:| -------:|
| `data/minified/2013/dtb.csv`     | CSV            | 1,139,573 |    8.9% |
| `data/minified/2013/dtb.json`    | JSON           | 1,878,267 |   32.6% |
| `data/minified/2013 dtb.plist`   | p-list         | 4,176,251 |   16.0% |
| `data/minified/2013/dtb.sql`     | SQL            | 1,286,038 |    7.1% |
| `data/minified/2013/dtb.xml`     | XML            | 3,859,564 |   18.1% |
| `data/minified/2013/dtb.yaml`    | YAML           | 1,806,482 |   12.4% |

### Database records

| Table          | 2013   |
| --------------:| ------:|
| `uf`           |     27 |
| `mesorregiao`  |    137 |
| `microrregiao` |    558 |
| `municipio`    |  5,570 |
| `distrito`     | 10,302 |
| `subdistrito`  |    662 |

### Get involved!

Report any mislead information, enhancement or feature request to [our bug tracker](https://github.com/paulofreitas/dtb-ibge/issues)!