# API
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Findings : 
  ->**Rate limiting factor** of all the three versions (v1 - 100 req per minute, v2 - 50 req per minute and v3 - 80 req per minute).
  I used a simple python code which was requesting data using different queries (a set of alphabetic strings) and then analysed in which query am I receiving error and then used that query manually on given endpoints and found out the given rate limiting factors in each of the versions. Then I used that to calculate the rate limit delay for my code.  
  ->**Pagination** Recursively fetches all pages if nextPage exists, Prevents duplicate requests by tracking discovered names, automatically stops when "nextPage" is missing or null.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Approach :
  Went for a brute force approach (Recursive Alphabetic Expansion) at first and tried to retrieve all the names from all the queries present in the database. But it would take an eternity as processing 26 alphabets for so many different variation of strings is very time consuming. Recursively explores all prefixes
  limitations ->
    Inefficient query expansion → Many redundant queries.
    No smart error handling → Does not handle API rate limits (429).
    No adaptive rate limiting → Fixed delay, even if unnecessary.
    Recursive calls → May lead to excessive API calls.

  Optimised Approach 
  This approach uses a queue-based breadth-first search (BFS) strategy for efficient name discovery while handling API limits dynamically
  Improvements Over Approach 1:
    Efficient query expansion → Only expands valid prefixes.
    Handles API rate limits (429 Too Many Requests).
    Adaptive rate limiting → Increases delay when needed.
    No recursion → Uses BFS queue for controlled expansion.
    Saves results → Extracted names are stored in a JSON file.
    Performance tracking → Tracks API requests, execution time, and request rate.
