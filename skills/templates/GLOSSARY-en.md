# GLOSSARY - Centralized Terms Dictionary

**Project/Projects**: [All | multi-project]  
**Language**: {language} (English/Español)  
**Last Updated**: {date}  

---

## How to Use This Glossary

- This glossary is the **single source of truth** for terminology across all requirements
- All terms defined here MUST be used consistently in all REQ-NNN.md files
- If a term is not defined here, it is **ambiguous** and must be rejected
- Each entry includes: Definition, Context, Related Terms, Examples

---

## Centralized Terms

### Search_System

**Definition**: System component responsible for indexing, storing, and retrieving documented information according to search criteria specified by the user.

**Context**: Used in requirements for search, indexing, and data retrieval.

**Related Terms**: 
- Search_Query
- Search_Index
- Search_Results

**Example**: "The Search_System must process 100k documents without exceeding 3 seconds latency."

**Additional Notes**: Also known as "Search Engine" in business contexts. Do not confuse with "Advanced Search" which is a feature.

---

### Search_Query

**Definition**: Structured user request to the Search_System that specifies search criteria using operators (AND, OR, NOT) and filters (date range, document type, author).

**Context**: User input that initiates the search process.

**Related Terms**:
- Search_System
- Search_Operator
- Search_Filter

**Example**: "The user sends a Search_Query: 'python AND framework AND 2023:2024' with author filter='Guido'"

**Additional Notes**: A Search_Query can be simple (keyword) or complex (Boolean operators + filters).

---

### Search_Results

**Definition**: Ordered set of documents matching a Search_Query criteria, presented to the user with relevance score and associated metadata.

**Context**: Output from the Search_System after processing a Search_Query.

**Related Terms**:
- Search_System
- Search_Query
- Relevance
- Ranking

**Example**: "Search_Results are displayed in descending relevance order with 150-character snippet."

**Additional Notes**: A single Search_Result is one item; Search_Results (plural) is the complete collection.

---

### Search_Index

**Definition**: Optimized data structure that maps key terms to documents, enabling fast retrieval without sequential scanning.

**Context**: Internal Search_System component for optimizing performance.

**Related Terms**:
- Search_System
- Indexing
- Token

**Example**: "The Search_Index is built during the indexing phase using standard tokenization."

**Additional Notes**: Can be inverted index, full-text index, or other type depending on implementation.

---

### Search_Latency

**Definition**: Time elapsed from when the Search_System receives a Search_Query to when it returns Search_Results to the user.

**Context**: Critical performance metric in search requirements.

**Related Terms**:
- Search_System
- Search_Query
- SLA

**Example**: "Search_Latency must not exceed 3 seconds for 99.9% of queries."

**Additional Notes**: Includes processing time + network transmission. Does not include UI rendering.

---

### Relevance

**Definition**: Quantitative measure of how well a document matches a Search_Query criteria, calculated using scoring algorithms.

**Context**: Ranking criterion in Search_Results.

**Related Terms**:
- Search_Results
- Ranking
- Scoring

**Example**: "Documents are ranked by Relevance using BM25 algorithm with boosts for title fields."

**Additional Notes**: Relevance is subjective; must be validated against user expectations.

---

### [Add more terms as project requires...]

---

## Consistency Validation

**Total terms defined**: {count}

**Terms verified in requirements**: ✅ Yes / ❌ No

**Recent Actions**:
- [Terminology added in REQ-001]
- [Clarification of "Advanced Search" vs "Search_System"]
- [New term: "Search_Latency" for SLA]

---

## Change History

| Date | Action | Term | Version |
|------|--------|------|---------|
| 2026-08-10 | Added | Search_System | 1.0 |
| 2026-08-10 | Added | Search_Query | 1.0 |
| 2026-08-10 | Added | Search_Results | 1.0 |

---

**Status**: ✅ Active  
**Maintained by**: [team name]
