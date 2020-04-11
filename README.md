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
git clone https://github.com/tjdaley/restutil.git
```

This service requires the following packages:

1. flask
  a.  ```pip install -U Flask```
2. redis  ```
  a.  ```sudo apt update && apt get install redis-server```
  b.  ```pip install -U redis```
3. whoosh
  a. ```pip install Whoosh``

<a href="#services"></a>
# Services

## Average Mortgage Interest Rate
*This service provides the average mortgage interest rate for residential property from a given year, month, and loan term (in years). The
source of data is the Federal Reserve Bank of St. Louis's FRED service.*

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

## Code Search
*This service searches codified laws in the State of Texas.*

### Retrieve List of Searchable Codes

**Pattern**
```
https://username:username@host:port//codesearch/list/
```

**Example**
```
https://br549:br549@localhost:8005//codesearch/list/
```

**Result**
```
[
  {
    "code": "cp", 
    "code_name": "Civil Practice & Remedy"
  }, 
  {
    "code": "es", 
    "code_name": "Estates"
  }, 
  {
    "code": "fa", 
    "code_name": "Family"
  }, 
  {
    "code": "hs", 
    "code_name": "Health & Safety"
  }, 
  {
    "code": "pe", 
    "code_name": "Penal"
  }
]
```

### Search Codified Laws

**Pattern**
```
http://username:username@host:port/codesearch/search/<string:query>/<string:codelist>/
```

**Example**

The following example will retrieve a reference to all codified laws referencing 'protective order'. The
'*' at the end of the query tells the search agent to search **ALL** codified laws in Texas (that have been indexed).

```
http://br549:br549@localhost:8081/codesearch/protective+order/*/
```

If you only wanted to search for the words 'interview', 'child', 'in', 'chambers' in the Family Code and Penal code, the query would be:

```
http://br549:br549@localhost:8081/codesearch/interview+child+in+chambers/fa+pe/
```

**Result**

```
[
  {
    "code": "FA", 
    "code_name": "FAMILY", 
    "chapter": "153. CONSERVATORSHIP", 
    "subchapter": "A. GENERAL PROVISIONS", 
    "title": "5. THE PARENT-CHILD RELATIONSHIP",
    "subtitle": "B. SUITS AFFECTING THE PARENT-CHILD RELATIONSHIP", 
    "section_number": "153.009", 
    "section_name": "INTERVIEW OF CHILD IN CHAMBERS", 
    "text": "(a)  In a nonjury trial or at a hearing, on the application of a party, the  amicus attorney, or the attorney ad litem for the child, the court shall interview in chambers a child 12 years of age or older and may interview in chambers a child under 12 years of age to determine the child's wishes as to conservatorship or as to the person who shall have the exclusive right to determine the child's primary residence.  The court may also interview a child in chambers on the court's own motion for a purpose specified by this subsection. (b)  In a nonjury trial or at a hearing, on the application of a party, the amicus attorney, or the attorney ad litem for the child or on the court's own motion, the court may interview the child in chambers to determine the child's wishes as to possession,  access, or any other issue in the suit affecting the parent-child relationship. (c)  Interviewing a child does not diminish the discretion of the court in determining the best interests of the child. (d)  In a jury trial, the court may not interview the child in chambers regarding an issue on which a party is entitled to a jury verdict. (e)  In any trial or hearing, the court may permit the attorney for a party, the amicus attorney, the guardian ad litem for the child, or the attorney ad litem for the child to be present at the interview. (f)  On the motion of a party, the amicus attorney, or the attorney ad litem for the child, or on the court's own motion, the court shall cause a record of the interview to be made when the child is 12 years of age or older.  A record of the interview shall be part of the record in the case.",
    "highlights": "attorney ad litem for the child, the court shall <b class=\"match term0\">interview</b> in <b class=\"match term1\">chambers</b> a child 12 years of age or older and may <b class=\"match term0\">interview</b> in <b class=\"match term1\">chambers</b> a child under 12 years of age to determine the child...the child's primary residence.  The court may also <b class=\"match term0\">interview</b> a child in <b class=\"match term1\">chambers</b> on the court's own motion for a purpose specified by...child or on the court's own motion, the court may <b class=\"match term0\">interview</b> the child in <b class=\"match term1\">chambers</b> to determine the child's wishes as to possession,  access", 
    "future_effective_date": "N/A"
  }
]
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

<a href="#author"></a>
# Author

Thomas J. Daley, J.D. is a practicing family law litigation attorney, occassional mediator, and software developer.
Thomas J. Daley practices family law in north Texas, particularly in Collin County, Dallas County, and Denton County.