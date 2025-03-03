---
status: accepted
date: 2024-12-18
---

# Partition TLE table

## Context and Problem Statement

The TLE table contains a large number of rows (45M+ as of Dec 2024), and querying it to get the latest TLE set
to use with FOV or related requests is slow. The current version took 2-4 seconds to return results, which is
too slow for the FOV API  since it needs to be more responsive. Even if the propagation time reduces, which it
will, the overall query time will still be 2-4 seconds at a minimum and ideally it should be as low as possible.


## Considered Options

* Partition TLE table by date ranges
* Improve query efficiency with existing schema
* Use a different database (AWS Aurora DynamoDB or similar)
* Improve caching

## Decision Outcome

Chosen option: "Partition TLE table by date ranges", because it will improve query performance and should reduce the
overall query time to less than 1 second (not including any additional overhead).


### Consequences

* Good, because it will improve query performance and should reduce the
overall query time to less than 1 second.
* Bad, because it will require more maintenance - the partitions will need to be managed on a monthly basis, not a significant amount of overhead, but necessary in order to keep the original partition schema.



### Confirmation

Specific queries have been benchmarked with the prior approach and will be tested with the new approach to confirm the performance improvement.


## Pros and Cons of the Options

### Query Optimization

* Good, because it doens't need any addtional database changes or maintenance.
* Good, because it can reduce the query time
* Bad, because it can't optimize the longest running query enough to be useful.

### Partition TLE table by date ranges

* Good, because it will improve query performance and should reduce the
overall query time to less than 1 second.
* Good, because it doesn't require any code changes or maintenance
* Bad, because it will require more database maintenance - the partitions will need to be managed on a monthly basis, not a significant amount of overhead, but necessary in order to keep the original partition schema. (Can be mitigated with pg_partman)

### Use a different database (AWS Aurora DynamoDB or similar)

* Good, because it will long termimprove query performance and should reduce the
overall query time to less than 1 second.
* Bad, because it will require a decent amount of rework to the current codebase and a migration to a new database.

### Improve caching

* Good, because it is a good practice to use caching anyway for recent/frequently requested data.
* Bad, because the case where the same query is made multiple times in a short period of time is rare and the original issue of long initial query time is not addressed.

## More Information
Need support for pg_partman to manage the partitions in order to make maintenance easier, since queries up to a year ago need to be able to be run quickly. Originally the idea was that queries up to a month ago would be the primary use case for needing performance improvements, but upon further investigation, we need to have faster access to data up to a year back in order to support cases where researchers don't immediately analyze their data.
