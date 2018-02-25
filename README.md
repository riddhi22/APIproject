# Twitter API
Twitter streaming API for streaming data and store in curated form and adding some filters.The task was divided in three parts
## Twitter Streaming API
   Streamed data from twitter based on a particular keyword "modi" and curate the data and store in Pymongo in two collections
 namely "User" and "Tweet".
## Filter and search stored tweets
    Filtered tweets based on name,screenname,text,favcount,retweet count,tweet mentions,language,created_date.
 ## Filter data in CSV 
    Returned API response in CSV format based on selected columns like name,screenname,language,counts etc.
    
### Technologies Used
* Python/Flask Framework
* Pymongo(Mlab)
* Tweepy library

### Installation instructions
1. Clone the project
2. cd into the current project directory
3. Create virtual environment by ``` virtualenv venv ``` and activate it by ``` source venv/bin/activate ```
4. Install the requirements by ``` pip install -r requirements.txt ```
5. Run ``` python mongo.py ```

# API to trigger twitter stream and store it in curated form
   To trigger stream and store the result in mongoDB based on a keyword
   
  API = ``` http://localhost:8000/firstapi/<string:keyword> ```
  
  This API runs for time 60 sec as the time_limit = 60
  
# API to filter tweets based on parameters and sort the tweets and paginate the result.
## Filtering tweets
```
    sw = starts with
    ew = ends with
    co = contains
    lt = less than
    gt = greater than
    eq = equal to
```
  
  | Filter Keyword | Filter Parameters |
  | -------------- | ----------------- |
  | name           | sw,ew,co          |
  | text           | sw,ew,co          |
  | scrname        | sw,ew,co          |
  | mention        | sw,ew,co          |
  | rtcount        | lt,gt,eq          |
  | favcount       | lt,gt,eq          |
  | lang           |                   |
  | datestart      | yyyy-mm-dd        |
  | dateend        | yyyy-mm-dd        |
  
  ### Some examples
  
  ```
      API = "http://localhost:8000/secondapi/?text=covisit&scrname=swDev&rtcount=lt5"
  ```
  Returns tweets which contains visit in text and screenname starts with dev and retweet count is less than 5
  
  ```
     API = "http://localhost:8000/secondapi/?datestart=2018-02-28"
  ```
  Returns tweets whose created date is greater than 28th Feb,2018
  
  ## Sorting Tweets
  
  | Sort By    |  Parameter   |
  | ---------- | ------------ |
  | name       | sort=name    |
  | screenname | sort=scrname |
  | text       | sort=text    |
  
  ### Example
  
  ```
      API = "http://localhost:8000/secondapi/?rtcount=lt4&sort=name"
  ```
  ## Paginate tweets
  
  ```
      API = "http://localhost:8000/secondapi/?rtcount=lt4&sort=name&page=2"
  ```
      By default page=1 is returned.
      
 # API to Return CSV response of filtered tweets
   Returns a CSV response of the filtered tweets.Filters are same as in second API.
   
   Example
   ```
      API = "http://localhost:8000/firstCSVfile/?rtcount=lt4&sort=name"
   ```
   
 
 
  
  
  
