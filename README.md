# restutil
Rest server that provides utilities to my other projects
<p align="center">
    <a href="https://github.com/tjdaley/restutil/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/tjdaley/restutil"></a>
    <a href="https://github.com/tjdaley/restutil/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/tjdaley/restutil"></a>
    <a href="https://github.com/tjdaley/restutil/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/tjdaley/restutil"><a>
    <a href="https://github.com/tjdaley/restutil/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/tjdaley/restutil"></a>
    <img alt="Stage: Development" src="https://img.shields.io/badge/stage-Development-orange">
</p>
<p align="center">
    <a href="#installation">Installation</a> &bull;
    <a href="#services">Services</a> &bull;
    <a href="#author">Author</a>
</p>

<a href="#installation"></a>
# Installation

```
pip install https://github.com/tjdaley/restutil
```

<a href="#services"></a>
# Services

## Average Mortgage Interest Rate
*This service provides the average mortgage interest rate for residential property from a given year, month, and loan term (in years). The
source of data is the Federal Reserve Bank of St. Louis's FRED service.*

### URL

**Pattern**
```
http://username:username@host:port/fred/historical_rate/<int:year>/<int:month>/<int:term>/
```

**Example**

The following URL will retrieve the average interest rate for a 30 year loan in January of 2020.

```
http://br549:br549@localhost:8081/fred/historical_rate/2020/01/30/
```

**Result**
```json
{
  "code": "OK", 
  "data": {
    "params": {
      "month": 1, 
      "term": 30, 
      "year": 2020
    }, 
    "query": "historical_rate", 
    "response": 0.0362
  }, 
  "dataset": "FRED", 
  "message": "OK", 
  "success": true, 
  "version": "0.0.1"
}
```
## Zillow Home Value
*This service provides the Z-Estimate and branding links for a parcel of property given a street address and city+state+zip. The
source of data is Zillow.*

### URL

**Pattern**
```
http://username:username@host:port/zillow/value/<string:street>/<string:city_state_zip>/
```

**Example**

The following URL will retrieve information about the White House

```
http://br549:br549@localhost:8081/zillow/value/123+main+st/dallas+tx
```

**Result**
```json

  "code": "OK", 
  "data": {
    "params": {
      "city_state_zip": "dallas+tx", 
      "street": "123+main+st"
    }, 
    "query": "zillow/value", 
    "response": {
      "city": "Dallas", 
      "comps_link": "http://www.zillow.com/homes/comps/26662117_zpid/", 
      "details_link": "https://www.zillow.com/homedetails/123-Main-St-Dallas-TX-75000/26662117_zpid/", 
      "latitude": "34.172576", 
      "longitude": "-95.66564", 
      "state": "TX", 
      "street": "123 Main St", 
      "value": 302820.0, 
      "zbranding": "<a href=\"https://www.zillow.com/homedetails/123-Main-St-Dallas-TX-75000/26662117_zpid/\">See more details for 123 Main St on Zillow.</a>", 
      "zip": "75000"
    }
  }, 
  "dataset": "ZILLOW", 
  "message": "OK", 
  "success": true, 
  "version": "0.0.1"
}
```