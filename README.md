# Project 3 - Search Engine

## Overview

**Skill:** Advanced

**Main Challenges:**

- Design efficient data structures

- Devise efficient file access

- Balance memory usage and response time
  

**Corpus:** All ICS web pages (developer.zip)

**Index:** Index should be stored in one or more files in the system (no databases)

**Search Interface:** The response to search queries should be less than 300ms. Ideally, close to 100ms, or less, but you won’t be penalized if it’s higher (as long as it’s under 300ms)

**Operational constraints:** Typically, the cloud servers/containers that run search engines don’t have a lot of memory. As such, you must design and implement your programs under the assumption of 256M RAM of available memory.

  
  

## Milestone 1

**Given:** HTML files to index

**Goal:** Build an inverted index off of the files

**Deliverable:** A report (pdf) with the following content: a table with assorted numbers pertaining to your index. It should have, at least the number of documents, the number of [unique] tokens, and the total size (in KB) of your index on disk.

**Inverted Index:**

- A map with the token as a key and a list of its corresponding postings.

**Posting:**

- Representation of the token's occurrence in a document. The Posting typically (not limited to) contains the following information:

		1. The document name/id the token was found in

		2. The tf-idf score for that document


**Tips:**

- Think about the structure of your posting first when designing the inverted index

- Begin by implementing the code to calculate/fetch the elements which will constitute your posting

- Modularize: Use scripts/classes that will perform a function or a set of closely related functions. Helps in keeping track of your progress, debugging, etc.