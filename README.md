# restutil
Rest server that provides utilities to my other projects
<p align="center">
    <a href="https://github.com/tjdaley/restutil/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/tjdaley/restutil"></a>
    <a href="https://github.com/tjdaley/restutil/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/tjdaley/restutil"></a>
    <a href="https://github.com/tjdaley/restutil/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/tjdaley/restutil"><a>
    <a href="https://github.com/tjdaley/restutil/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/tjdaley/restutil"></a>
    <a href="https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Ftjdaley%2Frestutil"><img alt="Twitter" src="https://img.shields.io/twitter/url?style=social"></a>
</p>
<p align="center">
    <a href="#installation">Installation</a> &bull;
    <a href="#services">Services</a> &bull;
    <a href="#author">Author</a>
</p>

<a href="#installation></a>
# Installation

```
pip install https://github.com/tjdaley/restutil
```
<small>, default='X1-ZWz1h8ok2gzpqj_3qukz'</small>

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
http://br549:br549@localhost:8081/zillow/value/2100+pennsylvania+avenue/washington+dc
```

**Result**
